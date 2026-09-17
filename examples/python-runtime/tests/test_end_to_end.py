from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from agent_runtime.application import AgentPlatformApplication
from agent_runtime.models import AttemptResultStatus, OutcomeStatus, RunStatus


class EndToEndCaseTest(unittest.TestCase):
    def test_recovers_and_reconciles_timeout_without_duplicate_attempt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            app = AgentPlatformApplication(directory)
            app.seed_source("# 测试架构\n\nRuntime、Harness、Environment 分层。\n")

            result = app.run_case(simulate_restart=True)

            self.assertEqual(result.run.status, RunStatus.COMPLETED)
            self.assertEqual(result.business_task.status, "accepted")
            self.assertTrue(result.evaluation.passed)
            self.assertEqual(len(result.actions), 2)
            self.assertEqual(len(result.attempts), 2)

            write_action = next(action for action in result.actions if action.name == "write_text")
            write_attempts = [attempt for attempt in result.attempts if attempt.action_id == write_action.action_id]
            self.assertEqual(len(write_attempts), 1, "timeout must be reconciled before any retry")

            statuses = [item.status for item in result.attempt_results]
            self.assertIn(AttemptResultStatus.TIMEOUT, statuses)
            write_outcome = next(item for item in result.outcomes if item.action_id == write_action.action_id)
            self.assertEqual(write_outcome.status, OutcomeStatus.SUCCEEDED)
            self.assertEqual(write_outcome.resolution, "external_state_reconciliation")

            event_types = [event.event_type for event in result.events]
            self.assertIn("RecoveryStarted", event_types)
            self.assertIn("RecoveryCompleted", event_types)
            self.assertIn("ActionOutcomeUnknown", event_types)
            self.assertIn("ActionReconciled", event_types)
            self.assertLess(event_types.index("RunCompleted"), event_types.index("WorkCompleted"))
            self.assertEqual(event_types[-1], "WorkCompleted")

            report = Path(directory, "workspace", "output", "report.md").read_text(encoding="utf-8")
            self.assertIn("Runtime 管事实，Harness 管策略", report)
            self.assertEqual(result.checkpoint.cursor, "terminal")
            self.assertEqual(result.state_view.run_status, "completed")


if __name__ == "__main__":
    unittest.main()
