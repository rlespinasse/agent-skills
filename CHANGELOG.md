# Changelog

All notable changes to this project will be documented in this file.

## [1.12.2](https://github.com/rlespinasse/agent-skills/compare/v1.12.1...v1.12.2) (2026-04-20)

### Bug Fixes

* **claude-code-usage-report:** update pricing data only on meaningful changes ([#27](https://github.com/rlespinasse/agent-skills/issues/27)) ([0f3946d](https://github.com/rlespinasse/agent-skills/commit/0f3946df5475528c6e9e1f77f4d17f21cd20b723))

## [1.12.1](https://github.com/rlespinasse/agent-skills/compare/v1.12.0...v1.12.1) (2026-04-20)

### Build System

* **deps:** bump the dependencies group across 1 directory with 3 updates ([7667dcd](https://github.com/rlespinasse/agent-skills/commit/7667dcd2cde51582224315cb237bda8fcbb7c092))

### Continuous Integration

* skip autofix on dependabot prs ([080592d](https://github.com/rlespinasse/agent-skills/commit/080592dbfbe723c621b601135718a45c94f2d076))

## [1.12.0](https://github.com/rlespinasse/agent-skills/compare/v1.11.1...v1.12.0) (2026-04-05)

### Features

* add promptfoo eval integration with Claude Code CLI ([216487d](https://github.com/rlespinasse/agent-skills/commit/216487d8eeb364a285c822a6c6576568a958c60b))
* **claude-code-usage-report:** support dual cache tiers and improve pricing workflow ([a659040](https://github.com/rlespinasse/agent-skills/commit/a659040811f3b9bcfbb791e8232bdead3162355a))
* **conventional-commit:** add fixup commit workflow ([4860427](https://github.com/rlespinasse/agent-skills/commit/4860427daef2924c654a5891b9ba094d410fa355))
* **diataxis:** add boundary cases and prior reclassification guidance ([f24afe7](https://github.com/rlespinasse/agent-skills/commit/f24afe76b96f4f41748c3f4b7bc33c90000aa6dd))
* **pin-github-actions:** add batch resolution and already-pinned handling ([95ff2ac](https://github.com/rlespinasse/agent-skills/commit/95ff2ac84c2cf5ec1b87e7b0ca9309d0ee951ca7))

### Bug Fixes

* **local-branches-status:** validate upstream ref exists before reporting sync state ([2870cb3](https://github.com/rlespinasse/agent-skills/commit/2870cb355d89d51f9e058dde0d0992053b5f4833))

### Documentation

* add tutorial for creating a first skill ([a00c450](https://github.com/rlespinasse/agent-skills/commit/a00c450dc06dfde4b28d9bf66edc6dba30bcccb8))
* fix overstated claims in README ([60e50d7](https://github.com/rlespinasse/agent-skills/commit/60e50d7c9fc84c6ade74d2caeee08ea92f703e2a))
* update npx skills install command to correct URL format ([fc2cf75](https://github.com/rlespinasse/agent-skills/commit/fc2cf75c7197a0ce9cd9bfdf84568d97c04774e4))

### Code Refactoring

* extract validate-skill recipe and reorganize just tasks ([0dad316](https://github.com/rlespinasse/agent-skills/commit/0dad316e9dc9b8f7fba3e44711e24975f175e941))

### Build System

* **deps:** bump taiki-e/install-action in the dependencies group ([75e64a1](https://github.com/rlespinasse/agent-skills/commit/75e64a1f09a3f7d406fb48c9513f8fbddc8f1583))

## [1.11.1](https://github.com/rlespinasse/agent-skills/compare/v1.11.0...v1.11.1) (2026-03-26)

### Build System

* **deps:** bump the dependencies group with 2 updates ([#19](https://github.com/rlespinasse/agent-skills/issues/19)) ([e7ca963](https://github.com/rlespinasse/agent-skills/commit/e7ca9631f15e1b77cf67175bf3f38843c99a8ac5))

## [1.11.0](https://github.com/rlespinasse/agent-skills/compare/v1.10.0...v1.11.0) (2026-03-23)

### Features

* **conventional-commit:** add scope-inherent type guidance ([#21](https://github.com/rlespinasse/agent-skills/issues/21)) ([1097427](https://github.com/rlespinasse/agent-skills/commit/1097427498580dfcdbbcb706356e041ea1490f1f))

### Documentation

* add security policy ([#17](https://github.com/rlespinasse/agent-skills/issues/17)) ([1aa1bbf](https://github.com/rlespinasse/agent-skills/commit/1aa1bbf1eb8319e8d7cd5f2c04a0cefdf5211642))

### Continuous Integration

* replace pre-commit hook with autofix workflow on PRs ([#20](https://github.com/rlespinasse/agent-skills/issues/20)) ([95f3cfc](https://github.com/rlespinasse/agent-skills/commit/95f3cfcc85eaebd3f46a26f36d9a4a051de3293f))

## [1.10.0](https://github.com/rlespinasse/agent-skills/compare/v1.9.0...v1.10.0) (2026-03-22)

### Features

* add claude-code-usage-report skill ([#18](https://github.com/rlespinasse/agent-skills/issues/18)) ([3b22b9f](https://github.com/rlespinasse/agent-skills/commit/3b22b9f6e6cfa1a009df57644d4874ef3ecc579e))

## [1.9.0](https://github.com/rlespinasse/agent-skills/compare/v1.8.1...v1.9.0) (2026-03-21)

### Features

* add french-language skill ([#12](https://github.com/rlespinasse/agent-skills/issues/12)) ([5fdccc7](https://github.com/rlespinasse/agent-skills/commit/5fdccc70e17d80af0055cf2f78e86b0dc4050f3c))
* **diataxis:** improve skill with references and expanded evals ([#15](https://github.com/rlespinasse/agent-skills/issues/15)) ([c739eb7](https://github.com/rlespinasse/agent-skills/commit/c739eb7492e8ce1133bd20887644171c0ab8d429))

## [1.8.1](https://github.com/rlespinasse/agent-skills/compare/v1.8.0...v1.8.1) (2026-03-21)

### Bug Fixes

* **pin-github-actions:** add prompt injection mitigations ([#13](https://github.com/rlespinasse/agent-skills/issues/13)) ([cad3090](https://github.com/rlespinasse/agent-skills/commit/cad309016984bbe7298efd5dca000d49cc5fb4cd))
* **verify-pr-logs:** add prompt injection mitigations ([#14](https://github.com/rlespinasse/agent-skills/issues/14)) ([3fdbfc0](https://github.com/rlespinasse/agent-skills/commit/3fdbfc0f97ea3e909604c6461d796ed1fdec74fc))

## [1.8.0](https://github.com/rlespinasse/agent-skills/compare/v1.7.0...v1.8.0) (2026-03-18)

### Features

* add local-branches-status skill ([#10](https://github.com/rlespinasse/agent-skills/issues/10)) ([662383f](https://github.com/rlespinasse/agent-skills/commit/662383f46821e9fcff1c9c5db490e901836ffcdd))

## [1.7.0](https://github.com/rlespinasse/agent-skills/compare/v1.6.0...v1.7.0) (2026-03-16)

### Features

* add verify-pr-logs skill for diagnosing CI failures on PRs ([#8](https://github.com/rlespinasse/agent-skills/issues/8)) ([5789245](https://github.com/rlespinasse/agent-skills/commit/578924548e978d837d23f57ce3145440ef714a2f))

## [1.6.0](https://github.com/rlespinasse/agent-skills/compare/v1.5.0...v1.6.0) (2026-03-16)

### Features

* **validate:** add spec references and compatibility validation ([#9](https://github.com/rlespinasse/agent-skills/issues/9)) ([019de1e](https://github.com/rlespinasse/agent-skills/commit/019de1ed5d163c608ce26ff18de9a5b77ec6b60d))

## [1.5.0](https://github.com/rlespinasse/agent-skills/compare/v1.4.0...v1.5.0) (2026-03-15)

### Features

* add pin-github-actions skill ([481a48e](https://github.com/rlespinasse/agent-skills/commit/481a48e3a488327af7f53af12c161f2e9c1b48f2))

## [1.4.0](https://github.com/rlespinasse/agent-skills/compare/v1.3.0...v1.4.0) (2026-03-15)

### Features

* add verify-readme-features skill ([#7](https://github.com/rlespinasse/agent-skills/issues/7)) ([ccf5f63](https://github.com/rlespinasse/agent-skills/commit/ccf5f63d8e185503751df678bf486aee52c9e68f))

## [1.3.0](https://github.com/rlespinasse/agent-skills/compare/v1.2.0...v1.3.0) (2026-03-12)

### Features

* Enhance conventional commit guidance for complex scenarios ([#5](https://github.com/rlespinasse/agent-skills/issues/5)) ([ce85e5a](https://github.com/rlespinasse/agent-skills/commit/ce85e5aeaf4e0913ca2e982dc60af1c329e172fa))

## [1.2.0](https://github.com/rlespinasse/agent-skills/compare/v1.1.0...v1.2.0) (2026-03-10)

### Features

* add conventional-commit skill ([403539f](https://github.com/rlespinasse/agent-skills/commit/403539f9645025b1fdb7804d9dae87b0637a1a5d))

### Documentation

* sync generated files for conventional-commit skill ([b346999](https://github.com/rlespinasse/agent-skills/commit/b346999fc74ea47f46e89d3a2411715dbc5de4c0))

## [1.1.0](https://github.com/rlespinasse/agent-skills/compare/v1.0.2...v1.1.0) (2026-03-10)

### Features

* add diataxis documentation skill ([4ace012](https://github.com/rlespinasse/agent-skills/commit/4ace0128c08598e2ab439f50786892c1a8d085d5))

### Code Refactoring

* move skill directories under skills/ subdirectory ([ea3167d](https://github.com/rlespinasse/agent-skills/commit/ea3167d710eab17a61925f526cca382bc15d2047))

## [1.0.2](https://github.com/rlespinasse/agent-skills/compare/v1.0.1...v1.0.2) (2026-03-10)

### Code Refactoring

* remove npm dependency, add evals infrastructure and plugin manifest ([#4](https://github.com/rlespinasse/agent-skills/issues/4)) ([8b93782](https://github.com/rlespinasse/agent-skills/commit/8b93782472e323ff56715898b65dd5247637b6b8))

## <small>1.0.1 (2026-02-16)</small>

* build(release): customize release trigger ([78a1196](https://github.com/rlespinasse/agent-skills/commit/78a1196))
* build(release): remove generated files from markdown analysis ([9684bfa](https://github.com/rlespinasse/agent-skills/commit/9684bfa))

## 1.0.0 (2026-02-16)

* ci(release): enable persist-credentials ([87582a7](https://github.com/rlespinasse/agent-skills/commit/87582a7))
* ci(release): install just ([da8c21e](https://github.com/rlespinasse/agent-skills/commit/da8c21e))
* build(deps): bump the npm_and_yarn group across 1 directory with 2 updates (#2) ([5239719](https://github.com/rlespinasse/agent-skills/commit/5239719)), closes [#2](https://github.com/rlespinasse/agent-skills/issues/2)
* feat(drawio-export-tools): initialize the skill around drawio export tools (#1) ([868f943](https://github.com/rlespinasse/agent-skills/commit/868f943)), closes [#1](https://github.com/rlespinasse/agent-skills/issues/1)
* initial commit ([f2dae0c](https://github.com/rlespinasse/agent-skills/commit/f2dae0c))
