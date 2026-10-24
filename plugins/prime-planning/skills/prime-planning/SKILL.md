---
name: prime-planning
description: Enforces test-first planning for new features — every planned feature must state how it will be verified, and tests are written before implementation. Use at the start of feature work.
---
## Planning
* whenever you plan a new feature you must include how you will test it
* test creation should happen before the feature is created, prove that it fails, and then creation of the feature should make the test pass
* tests should cover UI behavior via Playwright end-to-end where applicable; core logic and integration layers are tested with unit/integration tests (see the regression-testing skill). Not every test must be e2e — match the test layer to the change.
* for the test-execution protocol (framework discovery, baseline, full-suite pass), see the regression-testing skill.
