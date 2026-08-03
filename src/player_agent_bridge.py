"""
glass-bead-game-v26 — Player Agent Bridge
Links a player's actual Hermes agent to the Glass Bead Game server.

The player runs their own Hermes agent locally (or anywhere) and connects
it to the Game server via a simple API bridge. The player's agent executes
moves, refractions, and skill invocations — the player pays the token cost,
not the server host.

This is the "bring your own agent" model:
  - Game server: hosts the knowledge graph, transformers, skill tree,
    dashboards, and game state — NO LLM calls
  - Player's Hermes agent: connects via API, receives move requests,
    executes LLM-backed refractions, returns results — pays token cost

Connection protocol:
  1. Player registers their agent with a name + endpoint URL
  2. Server issues an agent_token for authentication
  3. Player's agent polls /api/bridge/tasks or receives webhook
  4. Agent executes the task (refraction, skill, transform)
  5. Agent POSTs the result back to the server

Hesse: "The player proceeds by making deep connections..."
       — the agent makes those connections, the player directs them.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import json
import secrets


class AgentStatus(Enum):
    OFFLINE = "offline"
    ONLINE = "online"
    BUSY = "busy"
    ERROR = "error"


class TaskStatus(Enum):
    PENDING = "pending"
    CLAIMED = "claimed"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class PlayerAgent:
    """A player's linked Hermes agent."""
    agent_id: str
    player_name: str
    agent_name: str
    endpoint_url: str               # where the agent can be reached
    agent_token: str                 # auth token
    status: AgentStatus = AgentStatus.OFFLINE
    connected_at: Optional[str] = None
    last_heartbeat: Optional[str] = None
    tasks_completed: int = 0
    tasks_failed: int = 0
    domains: List[str] = field(default_factory=list)  # domains this agent can handle

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "player_name": self.player_name,
            "agent_name": self.agent_name,
            "endpoint_url": self.endpoint_url,
            "status": self.status.value,
            "connected_at": self.connected_at,
            "last_heartbeat": self.last_heartbeat,
            "tasks_completed": self.tasks_completed,
            "tasks_failed": self.tasks_failed,
            "domains": self.domains,
        }


@dataclass
class BridgeTask:
    """A task dispatched to a player's agent for execution."""
    task_id: str
    agent_id: str
    task_type: str                   # "refract", "skill", "transform", "move"
    payload: Dict[str, Any]          # the inputs for the task
    status: TaskStatus = TaskStatus.PENDING
    created_at: str = ""
    claimed_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "task_type": self.task_type,
            "payload": self.payload,
            "status": self.status.value,
            "created_at": self.created_at,
            "claimed_at": self.claimed_at,
            "completed_at": self.completed_at,
            "result": self.result,
            "error": self.error,
        }


class PlayerAgentBridge:
    """
    Manages player agent connections, task dispatch, and result collection.

    The bridge is the middleware between the Game server (which holds state)
    and the player's Hermes agent (which holds the LLM).
    """

    def __init__(self):
        self._agents: Dict[str, PlayerAgent] = {}
        self._tasks: Dict[str, BridgeTask] = {}
        self._pending_queue: List[str] = []  # task_ids waiting to be claimed
        self._tokens: Dict[str, str] = {}    # agent_id -> token

    # ─── Agent Registration ─────────────────────────────────

    def register_agent(
        self,
        player_name: str,
        agent_name: str,
        endpoint_url: str,
        domains: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Register a new player agent. Returns agent_id and token.
        The player must provide their agent's endpoint URL where it
        can receive task notifications.
        """
        agent_id = f"agent_{secrets.token_hex(8)}"
        token = secrets.token_hex(32)

        agent = PlayerAgent(
            agent_id=agent_id,
            player_name=player_name,
            agent_name=agent_name,
            endpoint_url=endpoint_url,
            agent_token=token,
            status=AgentStatus.ONLINE,
            connected_at=datetime.utcnow().isoformat(),
            last_heartbeat=datetime.utcnow().isoformat(),
            domains=domains or [],
        )
        self._agents[agent_id] = agent
        self._tokens[agent_id] = token

        return {
            "agent_id": agent_id,
            "agent_token": token,
            "status": "registered",
            "message": f"Agent '{agent_name}' registered for player '{player_name}'. "
                       f"Use the token to authenticate task polling and submissions.",
        }

    def authenticate(self, agent_id: str, token: str) -> bool:
        """Verify an agent's auth token."""
        stored = self._tokens.get(agent_id)
        return stored is not None and stored == token

    def disconnect_agent(self, agent_id: str) -> bool:
        """Mark an agent as offline."""
        agent = self._agents.get(agent_id)
        if not agent:
            return False
        agent.status = AgentStatus.OFFLINE
        return True

    def heartbeat(self, agent_id: str) -> bool:
        """Update an agent's heartbeat timestamp."""
        agent = self._agents.get(agent_id)
        if not agent:
            return False
        agent.last_heartbeat = datetime.utcnow().isoformat()
        agent.status = AgentStatus.ONLINE
        return True

    # ─── Task Dispatch ───────────────────────────────────────

    def create_task(
        self,
        agent_id: str,
        task_type: str,
        payload: Dict[str, Any],
    ) -> BridgeTask:
        """
        Create a task for a player's agent to execute.
        task_type: "refract", "skill", "transform", "move"
        """
        task_id = f"task_{secrets.token_hex(8)}"
        task = BridgeTask(
            task_id=task_id,
            agent_id=agent_id,
            task_type=task_type,
            payload=payload,
            created_at=datetime.utcnow().isoformat(),
        )
        self._tasks[task_id] = task
        self._pending_queue.append(task_id)

        # Mark agent as busy
        agent = self._agents.get(agent_id)
        if agent:
            agent.status = AgentStatus.BUSY

        return task

    def get_pending_task(self, agent_id: str) -> Optional[BridgeTask]:
        """Get the next pending task for an agent."""
        for task_id in list(self._pending_queue):
            task = self._tasks.get(task_id)
            if task and task.agent_id == agent_id and task.status == TaskStatus.PENDING:
                task.status = TaskStatus.CLAIMED
                task.claimed_at = datetime.utcnow().isoformat()
                return task
        return None

    def submit_result(
        self,
        task_id: str,
        result: Dict[str, Any],
        agent_id: str,
    ) -> bool:
        """Submit a completed task result from the player's agent."""
        task = self._tasks.get(task_id)
        if not task or task.agent_id != agent_id:
            return False

        task.status = TaskStatus.COMPLETED
        task.result = result
        task.completed_at = datetime.utcnow().isoformat()

        # Update agent stats
        agent = self._agents.get(agent_id)
        if agent:
            agent.tasks_completed += 1
            agent.status = AgentStatus.ONLINE

        # Remove from pending
        if task_id in self._pending_queue:
            self._pending_queue.remove(task_id)

        return True

    def fail_task(
        self,
        task_id: str,
        error: str,
        agent_id: str,
    ) -> bool:
        """Mark a task as failed."""
        task = self._tasks.get(task_id)
        if not task or task.agent_id != agent_id:
            return False

        task.status = TaskStatus.FAILED
        task.error = error
        task.completed_at = datetime.utcnow().isoformat()

        agent = self._agents.get(agent_id)
        if agent:
            agent.tasks_failed += 1
            agent.status = AgentStatus.ONLINE

        if task_id in self._pending_queue:
            self._pending_queue.remove(task_id)

        return True

    # ─── Query Methods ──────────────────────────────────────

    def get_agent(self, agent_id: str) -> Optional[PlayerAgent]:
        return self._agents.get(agent_id)

    def list_agents(self) -> List[PlayerAgent]:
        return list(self._agents.values())

    def get_task(self, task_id: str) -> Optional[BridgeTask]:
        return self._tasks.get(task_id)

    def get_agent_tasks(self, agent_id: str) -> List[BridgeTask]:
        return [t for t in self._tasks.values() if t.agent_id == agent_id]

    def get_online_agents(self) -> List[PlayerAgent]:
        return [a for a in self._agents.values() if a.status == AgentStatus.ONLINE]

    # ─── Move Delegation ─────────────────────────────────────

    def delegate_move(
        self,
        agent_id: str,
        from_concept: str,
        from_domain: str,
        to_domain: str,
        via: str = "",
        resonance: str = "",
    ) -> BridgeTask:
        """
        Delegate a full Glass Bead Game move to the player's agent.
        The agent will use its LLM to generate the cross-domain correspondence.
        """
        return self.create_task(
            agent_id=agent_id,
            task_type="move",
            payload={
                "from_concept": from_concept,
                "from_domain": from_domain,
                "to_domain": to_domain,
                "via": via,
                "resonance": resonance,
                "instruction": (
                    f"You are a Glass Bead Game agent. Create a move from "
                    f"'{from_concept}' in {from_domain} to {to_domain}. "
                    f"Find the deepest structural correspondence. "
                    f"Return JSON: {{to_concept, structural_property, resonance_sentence, confidence}}"
                ),
            },
        )

    def delegate_refraction(
        self,
        agent_id: str,
        domain: str,
        concept: str,
        source_domain: str = "",
    ) -> BridgeTask:
        """Delegate a bead agent refraction to the player's agent."""
        return self.create_task(
            agent_id=agent_id,
            task_type="refract",
            payload={
                "domain": domain,
                "concept": concept,
                "source_domain": source_domain,
                "instruction": (
                    f"You are the {domain} bead agent in the Glass Bead Game. "
                    f"Refract '{concept}' from {source_domain} through your native "
                    f"disciplinary lens. Return JSON: "
                    f"{{translation, analogy, interval, confidence, austerity}}"
                ),
            },
        )

    def delegate_skill(
        self,
        agent_id: str,
        skill_id: str,
        inputs: Dict[str, Any],
    ) -> BridgeTask:
        """Delegate a skill execution to the player's agent."""
        return self.create_task(
            agent_id=agent_id,
            task_type="skill",
            payload={
                "skill_id": skill_id,
                "inputs": inputs,
                "instruction": (
                    f"Execute skill '{skill_id}' with the provided inputs. "
                    f"Return the result as JSON."
                ),
            },
        )

    # ─── Serialization ──────────────────────────────────────

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_agents": len(self._agents),
            "online_agents": len(self.get_online_agents()),
            "pending_tasks": len(self._pending_queue),
            "total_tasks": len(self._tasks),
            "agents": [a.to_dict() for a in self._agents.values()],
        }


# ─── Convenience singleton ────────────────────────────────────

_default_bridge: Optional[PlayerAgentBridge] = None


def get_bridge() -> PlayerAgentBridge:
    """Get or create the default PlayerAgentBridge instance."""
    global _default_bridge
    if _default_bridge is None:
        _default_bridge = PlayerAgentBridge()
    return _default_bridge