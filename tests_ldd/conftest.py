# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): AntiLoop, SessionTracking; TECH(8): pytest, hooks]
## @modulecontract
## @purpose Prevent agent looping by tracking test attempt count. Escalates when failures exceed threshold.
## @scope pytest session lifecycle hooks, attempt counter persistence.
## @input .test_counter.json (persisted counter file).
## @output Console warnings on repeated failures; persisted counter state.
## @links [USES_API(8): pytest.hookimpl]
## @invariants
## - Counter resets to 0 only at 100% PASS.
## - At 5+ consecutive failures, CRITICAL loop detected.
## @rationale
## Q: Why track attempts in conftest.py?
## A: Autonomous agents may retry failing tests without fixing the root cause. The counter provides a circuit breaker.
## @changes
## LAST_CHANGE: [v1.0.0 – Initial Anti-Loop protocol implementation.]
## @modulemap
## FUNC 8[Loads counter from JSON file] => _load_counter
## FUNC 8[Saves counter to JSON file] => _save_counter
## FUNC 9[Session finish hook with loop detection] => pytest_sessionfinish
## @usecases
## - [pytest_sessionfinish]: QA Agent (Verify) => RunTests => LoopDetectionOnRepeatedFailures => AgentEscalation
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: AntiLoop, attempt_counter, conftest, pytest, sessionfinish, circuit_breaker, agent_looping
# STRUCTURE: ▶ ┌.test_counter.json┐ → ◇ pytest_sessionfinish → ⊕ pass? reset : ++attempts → ∑ check threshold → ⚡ ≥5? CRITICAL → ⎋

import json
import os
import pytest

COUNTER_FILE = os.path.join(os.path.dirname(__file__), ".test_counter.json")


def _load_counter():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE) as f:
            return json.load(f)
    return {"attempts": 0, "last_result": "unknown"}


def _save_counter(data):
    with open(COUNTER_FILE, "w") as f:
        json.dump(data, f)


@pytest.hookimpl(hookwrapper=True)
def pytest_sessionfinish(session, exitstatus):
    yield
    counter = _load_counter()
    if exitstatus == 0:
        counter["attempts"] = 0
        counter["last_result"] = "PASS"
    else:
        counter["attempts"] += 1
        counter["last_result"] = "FAIL"
    _save_counter(counter)
    if counter["attempts"] > 0:
        print(f"\n[ANTI-LOOP] Attempt: {counter['attempts']}")
        if counter["attempts"] == 1:
            print("CHECKLIST: Verify test logic, check test data paths, review recent changes.")
        elif counter["attempts"] == 2:
            print("CHECKLIST: Check imports, module availability, environment variables, file permissions.")
        elif counter["attempts"] == 3:
            print("Use external search (tavily/Context7) to find similar issues online.")
        elif counter["attempts"] == 4:
            print("WARNING: Looping risk! Pause and reflect. Are you repeating a failed strategy?")
        elif counter["attempts"] >= 5:
            print("CRITICAL: Looping detected! STOP and request human help.")
