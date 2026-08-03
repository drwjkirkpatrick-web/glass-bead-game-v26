"""
Tests for the Player Agent Bridge module.
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from player_agent_bridge import (
    PlayerAgentBridge, PlayerAgent, BridgeTask,
    AgentStatus, TaskStatus, get_bridge,
)


@pytest.fixture
def bridge():
    return PlayerAgentBridge()


@pytest.fixture
def registered_bridge():
    b = PlayerAgentBridge()
    result = b.register_agent(
        player_name="Walker",
        agent_name="Hermes-1",
        endpoint_url="http://localhost:8080",
        domains=["musica", "mathematica"],
    )
    return b, result


class TestRegistration:
    def test_register_agent_returns_id_and_token(self, bridge):
        result = bridge.register_agent(
            player_name="Walker",
            agent_name="Hermes-1",
            endpoint_url="http://localhost:8080",
        )
        assert "agent_id" in result
        assert "agent_token" in result
        assert result["status"] == "registered"
        assert result["agent_id"].startswith("agent_")

    def test_registered_agent_is_online(self, bridge):
        result = bridge.register_agent("Walker", "Hermes-1", "http://localhost:8080")
        agent = bridge.get_agent(result["agent_id"])
        assert agent is not None
        assert agent.status == AgentStatus.ONLINE
        assert agent.player_name == "Walker"
        assert agent.agent_name == "Hermes-1"

    def test_authenticate_valid_token(self, registered_bridge):
        b, result = registered_bridge
        assert b.authenticate(result["agent_id"], result["agent_token"]) is True

    def test_authenticate_invalid_token(self, registered_bridge):
        b, result = registered_bridge
        assert b.authenticate(result["agent_id"], "wrong_token") is False

    def test_authenticate_unknown_agent(self, bridge):
        assert bridge.authenticate("unknown", "token") is False


class TestDisconnectAndHeartbeat:
    def test_disconnect_sets_offline(self, registered_bridge):
        b, result = registered_bridge
        assert b.disconnect_agent(result["agent_id"]) is True
        agent = b.get_agent(result["agent_id"])
        assert agent.status == AgentStatus.OFFLINE

    def test_disconnect_unknown_returns_false(self, bridge):
        assert bridge.disconnect_agent("unknown") is False

    def test_heartbeat_updates_timestamp(self, registered_bridge):
        b, result = registered_bridge
        original = b.get_agent(result["agent_id"]).last_heartbeat
        assert b.heartbeat(result["agent_id"]) is True
        updated = b.get_agent(result["agent_id"]).last_heartbeat
        assert updated != original

    def test_heartbeat_unknown_returns_false(self, bridge):
        assert bridge.heartbeat("unknown") is False


class TestTaskDispatch:
    def test_create_task(self, registered_bridge):
        b, result = registered_bridge
        task = b.create_task(result["agent_id"], "refract", {"concept": "fugue"})
        assert task.task_id.startswith("task_")
        assert task.task_type == "refract"
        assert task.status == TaskStatus.PENDING
        assert task.payload["concept"] == "fugue"

    def test_get_pending_task(self, registered_bridge):
        b, result = registered_bridge
        b.create_task(result["agent_id"], "refract", {"concept": "fugue"})
        task = b.get_pending_task(result["agent_id"])
        assert task is not None
        assert task.status == TaskStatus.CLAIMED

    def test_no_pending_task_returns_none(self, registered_bridge):
        b, result = registered_bridge
        assert b.get_pending_task(result["agent_id"]) is None

    def test_submit_result(self, registered_bridge):
        b, result = registered_bridge
        task = b.create_task(result["agent_id"], "refract", {"concept": "fugue"})
        b.get_pending_task(result["agent_id"])  # claim it
        success = b.submit_result(task.task_id, {"translation": "result"}, result["agent_id"])
        assert success is True
        completed = b.get_task(task.task_id)
        assert completed.status == TaskStatus.COMPLETED
        assert completed.result == {"translation": "result"}

    def test_submit_result_wrong_agent(self, registered_bridge):
        b, result = registered_bridge
        task = b.create_task(result["agent_id"], "refract", {"concept": "fugue"})
        assert b.submit_result(task.task_id, {}, "wrong_agent") is False

    def test_fail_task(self, registered_bridge):
        b, result = registered_bridge
        task = b.create_task(result["agent_id"], "refract", {"concept": "fugue"})
        b.get_pending_task(result["agent_id"])
        assert b.fail_task(task.task_id, "LLM error", result["agent_id"]) is True
        failed = b.get_task(task.task_id)
        assert failed.status == TaskStatus.FAILED
        assert failed.error == "LLM error"

    def test_agent_becomes_busy_on_task(self, registered_bridge):
        b, result = registered_bridge
        agent = b.get_agent(result["agent_id"])
        assert agent.status == AgentStatus.ONLINE
        b.create_task(result["agent_id"], "refract", {"concept": "fugue"})
        agent = b.get_agent(result["agent_id"])
        assert agent.status == AgentStatus.BUSY

    def test_agent_back_online_after_result(self, registered_bridge):
        b, result = registered_bridge
        task = b.create_task(result["agent_id"], "refract", {"concept": "fugue"})
        b.get_pending_task(result["agent_id"])
        b.submit_result(task.task_id, {"ok": True}, result["agent_id"])
        agent = b.get_agent(result["agent_id"])
        assert agent.status == AgentStatus.ONLINE
        assert agent.tasks_completed == 1


class TestMoveDelegation:
    def test_delegate_move(self, registered_bridge):
        b, result = registered_bridge
        task = b.delegate_move(
            agent_id=result["agent_id"],
            from_concept="fugue",
            from_domain="musica",
            to_domain="mathematica",
            via="self-referential structure",
        )
        assert task.task_type == "move"
        assert task.payload["from_concept"] == "fugue"
        assert task.payload["from_domain"] == "musica"
        assert task.payload["to_domain"] == "mathematica"
        assert "instruction" in task.payload

    def test_delegate_refraction(self, registered_bridge):
        b, result = registered_bridge
        task = b.delegate_refraction(
            agent_id=result["agent_id"],
            domain="mathematica",
            concept="fugue",
            source_domain="musica",
        )
        assert task.task_type == "refract"
        assert task.payload["domain"] == "mathematica"
        assert task.payload["concept"] == "fugue"

    def test_delegate_skill(self, registered_bridge):
        b, result = registered_bridge
        task = b.delegate_skill(
            agent_id=result["agent_id"],
            skill_id="musica.refract",
            inputs={"concept": "fugue", "source_domain": "mathematica"},
        )
        assert task.task_type == "skill"
        assert task.payload["skill_id"] == "musica.refract"
        assert task.payload["inputs"]["concept"] == "fugue"


class TestQueries:
    def test_list_agents(self, registered_bridge):
        b, _ = registered_bridge
        agents = b.list_agents()
        assert len(agents) == 1

    def test_get_agent_tasks(self, registered_bridge):
        b, result = registered_bridge
        b.create_task(result["agent_id"], "refract", {})
        b.create_task(result["agent_id"], "move", {})
        tasks = b.get_agent_tasks(result["agent_id"])
        assert len(tasks) == 2

    def test_get_online_agents(self, registered_bridge):
        b, _ = registered_bridge
        assert len(b.get_online_agents()) == 1

    def test_get_unknown_agent(self, bridge):
        assert bridge.get_agent("unknown") is None

    def test_get_unknown_task(self, bridge):
        assert bridge.get_task("unknown") is None


class TestSerialization:
    def test_to_dict(self, registered_bridge):
        b, _ = registered_bridge
        d = b.to_dict()
        assert "total_agents" in d
        assert "online_agents" in d
        assert "pending_tasks" in d
        assert "total_tasks" in d
        assert "agents" in d
        assert d["total_agents"] == 1


class TestSingleton:
    def test_get_bridge_returns_same_instance(self):
        b1 = get_bridge()
        b2 = get_bridge()
        assert b1 is b2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])