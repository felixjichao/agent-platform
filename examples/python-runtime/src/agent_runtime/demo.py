from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from .application import AgentPlatformApplication


DEFAULT_SOURCE = """# Agent Platform

七层软件栈把业务目标、能力契约、能力工程、执行策略、统一运行时、
智能体工作环境和真实资源分开。稳定边界是 Runtime 管事实，Harness
管策略，Environment 管执行机制。
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Agent Platform Python reference case")
    parser.add_argument("--case-root", help="Directory for SQLite, workspace and output")
    parser.add_argument("--no-restart", action="store_true", help="Do not simulate a process restart")
    args = parser.parse_args()

    case_root = Path(args.case_root) if args.case_root else Path(tempfile.mkdtemp(prefix="agent-platform-case-"))
    app = AgentPlatformApplication(case_root)
    app.seed_source(DEFAULT_SOURCE)
    result = app.run_case(simulate_restart=not args.no_restart)

    trace_path = case_root / "case_result.json"
    trace_path.write_text(json.dumps(result.as_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"case_root: {case_root}")
    print(f"business_task: {result.business_task.status}")
    print(f"run: {result.run.status.value}")
    print(f"evaluation: {'passed' if result.evaluation.passed else 'failed'}")
    print(f"artifact: {case_root / 'workspace' / result.artifact.uri}")
    print(f"trace: {trace_path}")
    print("events:")
    for event in result.events:
        print(f"  {event.sequence:02d} {event.event_type}")


if __name__ == "__main__":
    main()

