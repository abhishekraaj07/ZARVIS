"""
Comprehensive Automated Test Suite for All 51 ZARVIS / Ultron Actions.
Verifies discovery, schemas, handler signatures, and executes safe non-destructive calls.
"""
import sys
import os
import unittest
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from core.action_loader import discover_actions, _call_handler

class MockUI:
    def __init__(self):
        self.played = []
        self.logs = []
    def play(self, *args, **kwargs):
        pass
    def write_log(self, text, *args, **kwargs):
        self.logs.append(text)
    def show_confirm(self, *args, **kwargs):
        pass
    def hide_confirm(self, *args, **kwargs):
        pass

class TestAllActions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        actions_dir = ROOT_DIR / "actions"
        cls.registry = discover_actions(actions_dir, logger=lambda x: None)
        cls.ui = MockUI()
        cls.context = {
            "player": cls.ui,
            "speak": lambda *args, **kwargs: None,
            "response": "Acknowledged.",
            "session_memory": {}
        }

    def test_total_action_count(self):
        """Verify that all 51 actions are discovered and valid."""
        self.assertGreaterEqual(len(self.registry._actions), 51, f"Found only {len(self.registry._actions)} actions")

    def test_all_actions_have_valid_schemas(self):
        """Verify parameters schema conforms to Gemini expectations."""
        for name, record in self.registry._actions.items():
            self.assertTrue(record.valid, f"Action {name} is marked invalid: {record.error}")
            self.assertIsNotNone(record.handler, f"Action {name} has no handler")
            self.assertIsInstance(record.parameters, dict)
            self.assertEqual(record.parameters.get("type"), "OBJECT", f"Action {name} schema not OBJECT")

    def test_safe_execution_of_each_action(self):
        """Invoke safe non-destructive commands on every single action."""
        safe_params_map = {
            "airspace_sentinel": {"action": "status"},
            "android_bridge": {"action": "status"},
            "audio_matrix": {"action": "status"},
            "biometric_sentinel": {"action": "status"},
            "bounty_hunter": {"action": "status"},
            "browser_control": {"action": "status"},
            "cerebro_memory": {"action": "stats"},
            "chronos_predictive": {"action": "status"},
            "clipboard_control": {"action": "read"},
            "cloud_watchtower": {"action": "status"},
            "code_helper": {"action": "status"},
            "computer_control": {"action": "status"},
            "computer_settings": {"action": "status"},
            "desktop_control": {"action": "status"},
            "dev_agent": {"description": "Write a test function"},
            "drone_swarm": {"action": "status"},
            "file_controller": {"action": "list", "path": "."},
            "file_processor": {"action": "status"},
            "flight_finder": {"origin": "DEL", "destination": "BOM", "date": "2026-11-01"},
            "game_updater": {"action": "status"},
            "gesture_control": {"action": "status"},
            "ghost_pilot": {"action": "status"},
            "git_sentinel": {"action": "status"},
            "iot_overlord": {"action": "status"},
            "macro_protocol": {"action": "list"},
            "media_controller": {"action": "status"},
            "meeting_scribe": {"action": "status"},
            "network_auditor": {"action": "status"},
            "network_scanner": {"action": "status"},
            "omni_telepathy": {"action": "status"},
            "open_app": {"app_name": "notepad"},
            "optical_hud": {"action": "status"},
            "process_manager": {"action": "list"},
            "purge_protocol": {"action": "status"},
            "quick_timer": {"minutes": 1, "message": "Test"},
            "reminder": {"date": "today", "time": "23:59", "message": "Test reminder"},
            "screen_mind_read": {"prompt": "status"},
            "self_evolution": {"action": "list"},
            "send_message": {"receiver": "Boss", "message_text": "Status test", "platform": "telegram"},
            "sentry_protocol": {"action": "status"},
            "system_command": {"command": "echo test"},
            "system_utility": {"action": "status"},
            "video_player": {"action": "status"},
            "voice_matrix": {"action": "status"},
            "war_room": {"action": "status"},
            "weather_report": {"city": "New Delhi"},
            "web_autopilot": {"action": "status"},
            "web_search": {"query": "python unittest"},
            "workspace_matrix": {"action": "status"},
            "workspace_recall": {"action": "list"},
            "youtube_video": {"action": "search", "query": "Ultron AI"}
        }

        results = {}
        for name, record in sorted(self.registry._actions.items()):
            params = safe_params_map.get(name, {"action": "status"})
            try:
                res = _call_handler(record.handler, params, self.context)
                results[name] = {"success": True, "output": str(res)[:80]}
            except Exception as ex:
                results[name] = {"success": False, "error": str(ex)}

        failed = [k for k, v in results.items() if not v["success"]]
        for name, res in sorted(results.items()):
            status_icon = "✓" if res["success"] else "✗"
            print(f"[{status_icon}] {name:22}: {res.get('output', res.get('error'))}")

        self.assertEqual(len(failed), 0, f"The following actions failed safe execution: {failed}")

if __name__ == "__main__":
    unittest.main()
