from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from agents import AgentRunRequest, BoundedAgentExecutor
from benchmarks import run_suite
from books import BOOK_STAGES, BookProductionCore, ContinuityChecker
from business import BusinessQuoteService
from core.bootstrap import bootstrap
from memory.store import MemoryStore
from projects.artifact_completion import complete_task_with_artifact_gate
from projects.manager import ProjectStateManager
from providers import ProviderRequest, ProviderUnavailableError, default_registry


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="IVDIVO Personal AI Production System")
    parser.add_argument(
        "--home",
        default=os.environ.get("PERSONAL_AI_HOME"),
        help="Persistent home directory; defaults to the personal-ai directory.",
    )
    sub = parser.add_subparsers(dest="command")

    project = sub.add_parser("project", help="Project state operations")
    project_sub = project.add_subparsers(dest="project_command", required=True)

    create = project_sub.add_parser("create", help="Create a persisted project")
    create.add_argument("project_id")
    create.add_argument("--name")

    status = project_sub.add_parser("status", help="Read project state")
    status.add_argument("project_id")

    next_task = project_sub.add_parser("next", help="Return the next actionable task")
    next_task.add_argument("project_id")

    complete_artifact = project_sub.add_parser(
        "complete-artifact",
        help="Complete an artifact-producing task using a provider-backed placement receipt JSON",
    )
    complete_artifact.add_argument("project_id")
    complete_artifact.add_argument("task_id")
    complete_artifact.add_argument("receipt_json", help="Path to ArtifactPlacementReceipt JSON")

    memory = sub.add_parser("memory", help="Auditable local memory operations")
    memory_sub = memory.add_subparsers(dest="memory_command", required=True)

    put = memory_sub.add_parser("put", help="Persist a memory record")
    put.add_argument("content")
    put.add_argument("--kind", default="NOTE")
    put.add_argument("--source")
    put.add_argument("--id", dest="record_id")
    put.add_argument("--metadata", default="{}", help="JSON object")
    put.add_argument("--project-id")
    put.add_argument("--source-id")
    put.add_argument("--confidence", type=float)

    search = memory_sub.add_parser("search", help="Search local memory")
    search.add_argument("query")
    search.add_argument("--kind")
    search.add_argument("--project-id")
    search.add_argument("--include-invalid", action="store_true")
    search.add_argument("--limit", type=int, default=20)

    update = memory_sub.add_parser("update", help="Create a new memory version")
    update.add_argument("record_id")
    update.add_argument("content")
    update.add_argument("--source")
    update.add_argument("--metadata", help="replacement JSON object")
    update.add_argument("--project-id")
    update.add_argument("--source-id")
    update.add_argument("--confidence", type=float)

    invalidate = memory_sub.add_parser("invalidate", help="Invalidate a memory record")
    invalidate.add_argument("record_id")
    invalidate.add_argument("--reason", required=True)

    trace = memory_sub.add_parser("trace", help="Show a memory record audit-event trail")
    trace.add_argument("record_id")

    versions = memory_sub.add_parser("versions", help="Show immutable memory versions")
    versions.add_argument("record_id")

    source_trace = memory_sub.add_parser(
        "source-trace", help="Trace a memory record through source_id provenance"
    )
    source_trace.add_argument("record_id")
    source_trace.add_argument("--max-depth", type=int, default=20)

    provider = sub.add_parser("provider", help="AI provider abstraction operations")
    provider_sub = provider.add_subparsers(dest="provider_command", required=True)

    provider_sub.add_parser("list", help="List provider configuration without exposing secrets")

    provider_run = provider_sub.add_parser("run", help="Run one provider request")
    provider_run.add_argument("provider_name")
    provider_run.add_argument("prompt")
    provider_run.add_argument("--model")
    provider_run.add_argument("--system")
    provider_run.add_argument("--max-output-tokens", type=int, default=512)
    provider_run.add_argument("--temperature", type=float)
    provider_run.add_argument(
        "--allow-network",
        action="store_true",
        help="Explicitly authorize a network/provider call for this invocation.",
    )

    agent = sub.add_parser("agent", help="Bounded project-agent execution")
    agent_sub = agent.add_subparsers(dest="agent_command", required=True)
    agent_run = agent_sub.add_parser("run", help="Run one bounded agent task")
    agent_run.add_argument("project_id")
    agent_run.add_argument("prompt")
    agent_run.add_argument("--provider", default="mock")
    agent_run.add_argument("--model")
    agent_run.add_argument("--max-steps", type=int, default=3)
    agent_run.add_argument("--task-id")
    agent_run.add_argument(
        "--allow-network",
        action="store_true",
        help="Explicitly authorize network-backed provider use for this agent run.",
    )
    agent_run.add_argument(
        "--require-artifact-placement-receipt",
        action="store_true",
        help="Mark this task as artifact-producing; FINISH cannot become DONE without a verified placement receipt.",
    )
    agent_run.add_argument(
        "--artifact-placement-receipt",
        help="Optional path to provider-backed ArtifactPlacementReceipt JSON available at run completion.",
    )

    benchmark = sub.add_parser("benchmark", help="Baseline/candidate benchmark operations")
    benchmark_sub = benchmark.add_subparsers(dest="benchmark_command", required=True)
    benchmark_run = benchmark_sub.add_parser("run", help="Evaluate and persist one benchmark suite")
    benchmark_run.add_argument("suite", help="Path to benchmark suite JSON")
    benchmark_run.add_argument(
        "--enforce",
        action="store_true",
        help="Return non-zero exit status when the benchmark decision is FAIL.",
    )

    business = sub.add_parser("business", help="Business operations")
    business_sub = business.add_subparsers(dest="business_command", required=True)
    business_quote = business_sub.add_parser(
        "quote", help="Create a persisted fail-closed quote from explicit JSON inputs"
    )
    business_quote.add_argument("project_id")
    business_quote.add_argument("request_json", help="Path to quote request JSON")

    book = sub.add_parser("book", help="Book production state operations")
    book_sub = book.add_subparsers(dest="book_command", required=True)

    book_init = book_sub.add_parser("init", help="Initialize the persisted PL-08 book structure")
    book_init.add_argument("project_id")
    book_init.add_argument("--title")

    book_status = book_sub.add_parser("status", help="Read the persisted book production state")
    book_status.add_argument("project_id")

    book_advance = book_sub.add_parser("advance", help="Advance exactly one production stage")
    book_advance.add_argument("project_id")
    book_advance.add_argument("--to", dest="to_stage", choices=BOOK_STAGES)

    book_check = book_sub.add_parser(
        "check-continuity",
        help="Run the PL-09 deterministic checker over structured continuity evidence",
    )
    book_check.add_argument("project_id")
    book_check.add_argument("input_json", help="Path to normalized continuity input JSON")
    book_check.add_argument(
        "--enforce",
        action="store_true",
        help="Return non-zero exit status when FATAL/MAJOR issues are detected.",
    )

    book_continuity = book_sub.add_parser(
        "continuity", help="Record the explicit continuity gate at CONTINUITY stage"
    )
    book_continuity.add_argument("project_id")
    gate = book_continuity.add_mutually_exclusive_group(required=True)
    gate.add_argument("--pass-gate", action="store_true")
    gate.add_argument("--fail-gate", action="store_true")
    book_continuity.add_argument("--evidence", required=True)

    return parser


def _resolve_home(raw: str | None) -> Path:
    default_home = Path(__file__).resolve().parent
    return Path(raw).expanduser().resolve() if raw else default_home


def _json_object(raw: str) -> dict:
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError("metadata must decode to a JSON object")
    return value


def _json_file(path: str) -> dict:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("JSON input file must contain an object")
    return value


def _require_artifact_task(manager: ProjectStateManager, project_id: str, task_id: str) -> dict:
    for task in manager.load_project(project_id)["tasks"]:
        if task.get("id") == task_id:
            if not bool(task.get("requires_artifact_placement_receipt", False)):
                raise RuntimeError(
                    "complete-artifact requires a task declared with requires_artifact_placement_receipt=true"
                )
            return task
    raise KeyError(f"task not found: {task_id}")


def main() -> int:
    args = build_parser().parse_args()
    home = _resolve_home(args.home)
    exit_code = 0

    if args.command is None:
        result = bootstrap(home)
    elif args.command == "project":
        manager = ProjectStateManager(home)
        if args.project_command == "create":
            result = manager.create_project(args.project_id, args.name)
        elif args.project_command == "status":
            result = manager.load_project(args.project_id)
        elif args.project_command == "next":
            result = {"project_id": args.project_id, "next_task": manager.get_next_task(args.project_id)}
        elif args.project_command == "complete-artifact":
            _require_artifact_task(manager, args.project_id, args.task_id)
            result = complete_task_with_artifact_gate(
                manager,
                args.project_id,
                args.task_id,
                _json_file(args.receipt_json),
            )
            if result["status"] != "DONE":
                exit_code = 2
        else:  # pragma: no cover - argparse enforces choices
            raise RuntimeError("unsupported project command")
    elif args.command == "memory":
        store = MemoryStore(home / "runtime" / "state.db")
        if args.memory_command == "put":
            result = store.store(
                args.content,
                kind=args.kind,
                source=args.source,
                metadata=_json_object(args.metadata),
                record_id=args.record_id,
                project_id=args.project_id,
                source_id=args.source_id,
                confidence=args.confidence,
            )
        elif args.memory_command == "search":
            result = {
                "query": args.query,
                "results": store.search(
                    args.query,
                    kind=args.kind,
                    project_id=args.project_id,
                    include_invalid=args.include_invalid,
                    limit=args.limit,
                ),
            }
        elif args.memory_command == "update":
            metadata = None if args.metadata is None else _json_object(args.metadata)
            result = store.update(
                args.record_id,
                content=args.content,
                source=args.source,
                metadata=metadata,
                project_id=args.project_id,
                source_id=args.source_id,
                confidence=args.confidence,
            )
        elif args.memory_command == "invalidate":
            result = store.invalidate(args.record_id, args.reason)
        elif args.memory_command == "trace":
            result = {"memory_id": args.record_id, "events": store.trace(args.record_id)}
        elif args.memory_command == "versions":
            result = {"memory_id": args.record_id, "versions": store.versions(args.record_id)}
        elif args.memory_command == "source-trace":
            result = store.trace_source(args.record_id, max_depth=args.max_depth)
        else:  # pragma: no cover - argparse enforces choices
            raise RuntimeError("unsupported memory command")
    elif args.command == "provider":
        registry = default_registry()
        if args.provider_command == "list":
            result = {"providers": registry.describe_all()}
        elif args.provider_command == "run":
            selected = registry.get(args.provider_name)
            descriptor = selected.describe()
            if descriptor.network_required and not args.allow_network:
                raise ProviderUnavailableError(
                    f"{descriptor.name} requires explicit --allow-network for this invocation"
                )
            response = selected.generate(
                ProviderRequest(
                    prompt=args.prompt,
                    model=args.model,
                    system=args.system,
                    max_output_tokens=args.max_output_tokens,
                    temperature=args.temperature,
                )
            )
            result = response.to_dict()
        else:  # pragma: no cover - argparse enforces choices
            raise RuntimeError("unsupported provider command")
    elif args.command == "agent":
        if args.agent_command == "run":
            receipt = (
                _json_file(args.artifact_placement_receipt)
                if args.artifact_placement_receipt is not None
                else None
            )
            executor = BoundedAgentExecutor(home)
            result = executor.run(
                AgentRunRequest(
                    project_id=args.project_id,
                    prompt=args.prompt,
                    provider=args.provider,
                    model=args.model,
                    max_steps=args.max_steps,
                    allow_network=args.allow_network,
                    task_id=args.task_id,
                    requires_artifact_placement_receipt=args.require_artifact_placement_receipt,
                    artifact_placement_receipt=receipt,
                )
            ).to_dict()
            if result["status"] == "BLOCKED":
                exit_code = 2
        else:  # pragma: no cover - argparse enforces choices
            raise RuntimeError("unsupported agent command")
    elif args.command == "benchmark":
        if args.benchmark_command == "run":
            result = run_suite(Path(args.suite), home)
            if args.enforce and result["status"] != "PASS":
                exit_code = 2
        else:  # pragma: no cover - argparse enforces choices
            raise RuntimeError("unsupported benchmark command")
    elif args.command == "business":
        if args.business_command == "quote":
            result = BusinessQuoteService(home).create_quote(
                args.project_id, _json_file(args.request_json)
            )
        else:  # pragma: no cover - argparse enforces choices
            raise RuntimeError("unsupported business command")
    elif args.command == "book":
        core = BookProductionCore(home)
        if args.book_command == "init":
            result = core.initialize(args.project_id, args.title)
        elif args.book_command == "status":
            result = core.load(args.project_id)
        elif args.book_command == "advance":
            result = core.advance(args.project_id, args.to_stage)
        elif args.book_command == "check-continuity":
            result = ContinuityChecker(home).check(
                args.project_id,
                _json_file(args.input_json),
            )
            if args.enforce and result["blocking_issue_count"] > 0:
                exit_code = 2
        elif args.book_command == "continuity":
            result = core.set_continuity_gate(
                args.project_id,
                passed=args.pass_gate,
                evidence=args.evidence,
            )
        else:  # pragma: no cover - argparse enforces choices
            raise RuntimeError("unsupported book command")
    else:  # pragma: no cover - argparse enforces choices
        raise RuntimeError("unsupported command")

    print(json.dumps(result, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
