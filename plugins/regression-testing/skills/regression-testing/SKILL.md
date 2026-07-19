---
name: Universal Regression Testing
description: Ensures that every codebase modification is backed by a corresponding regression test to prevent breakages and maintain invariant stability.
---

# Regression Testing Protocol

This skill defines the mandatory testing standards for any agent contributing to a repository. Its primary goal is to maintain a stable, reliable codebase by enforcing strict test coverage for all logic changes, regardless of the underlying language or framework.

## The Protocol

### 1. Mandatory Pre-Flight

Before starting any implementation (feature, refactor, or bug fix), the agent MUST:

- **Analyze the Testing Environment:** Identify the project's test framework, test runner commands, and directory structure.
- **Review Existing Specs:** Examine current test files to understand established invariants, mocking strategies, and coding patterns.
- **Establish Baseline:** Run the full existing test suite to confirm a "Green" (passing) baseline before making _any_ codebase changes.

### 2. Test-First Contribution (TDD)

For any modification to the project's logic:

- **Write the Test:** Add a new test file or update an existing one in the designated test directory targeting the specific behavior.
- **Verify Failure:** Execute the test suite and ensure the new test fails _before_ the actual logic is implemented.

### 3. Verification & Cleanup

After completing the code implementation:

- **Full Suite Pass:** Run the entire test suite again. The new test must pass, and no existing tests can fail. Any regressions must be resolved before the task is considered "complete".
- **Artifact Cleanup:** Delete any temporary test artifacts, mock files, or dummy data generated during the testing process.

## Tooling & Discovery

The agent must automatically adapt to the repository's native tooling. Upon initializing a task, the agent should identify:

- **Test Framework:** The library used for assertions and structuring (e.g., `Pytest`, `Jest`, `JUnit`, `RSpec`, `cargo test`).
- **Test Runner:** The CLI command used to execute tests (e.g., `npm run test`, `make test`, `go test ./...`, or custom bash scripts).
- **Directory Mapping:**
  - **Source:** The directory containing core logic (e.g., `src/`, `lib/`, `app/`).
  - **Tests:** The directory containing specifications (e.g., `tests/`, `spec/`, `__tests__/`).

## Dynamic Test Targets

When applying this skill to a specific PR or task, the agent should dynamically identify and test the following layers of the application:

- [ ] **Core Logic:** Unit tests for algorithmic processing, data parsing, and domain rules.
- [ ] **State / Integration:** Lifecycle tests for database queries, API connections, or process management.
- [ ] **Boundary / UI:** Mocked tests for user interface rendering, CLI outputs, or API endpoints.
