# Security Policy

## Supported Versions

Only the latest release on the `main` branch is supported with security updates.
Older versions do not receive backports.

| Branch | Supported |
|--------|-----------|
| `main` | Yes       |
| Other  | No        |

## Security Scope

This repository contains documentation and skill definitions for AI coding assistants, not executable
software. Security concerns relevant to this project include:

- **Prompt injection or agent manipulation** -- skill content that could trick AI agents into performing
  harmful, destructive, or unauthorized actions
- **Malicious references** -- skills that link to, recommend, or embed URLs pointing to malicious tools,
  packages, or resources
- **Dangerous instructions** -- skill content that instructs agents to bypass security controls, disable
  safety features, or execute unsafe commands
- **Incorrect security guidance** -- skills that provide inaccurate security advice (e.g., insecure pinning
  recommendations, flawed authentication patterns)
- **Supply chain risks** -- compromised dependencies in CI/CD workflows or skill installation tooling

The following are **not** in scope:

- Typos, grammar, or formatting issues (open a regular issue instead)
- Feature requests or skill suggestions
- Bugs in third-party tools referenced by skills
- Vulnerabilities in the Agent Skills specification itself (report to [agentskills.io](https://agentskills.io))

## Reporting a Vulnerability

**Do not open a public issue for security vulnerabilities.**

Instead, use one of these methods:

1. **GitHub Private Vulnerability Reporting (preferred)** --
   Go to the [Security Advisories](https://github.com/rlespinasse/agent-skills/security/advisories)
   page and select **"Report a vulnerability"**.

2. **Email** -- Contact the maintainer directly at the email address listed on
   [@rlespinasse's GitHub profile](https://github.com/rlespinasse).

Please include the following in your report:

- A description of the vulnerability and its potential impact
- The affected skill(s) or file(s)
- Steps to reproduce the issue
- Any suggested remediation, if applicable

## Response Timeline

- **Acknowledgment**: within 7 days of receiving the report
- **Assessment**: within 14 days, you will receive an initial assessment and next steps
- **Resolution**: security fixes are prioritized and released as soon as practical

## Disclosure Policy

We follow coordinated disclosure. Please do not publicly disclose the issue until we have had a reasonable
opportunity to address it. We will credit reporters in the fix commit or release notes unless anonymity
is requested.

## Security Best Practices for Skill Authors

When contributing skills to this repository:

- **Verify all URLs** point to official, trusted sources
- **Do not embed credentials, tokens, or secrets** in skill content
- **Avoid instructions that disable security features** (e.g., `--no-verify`, `--insecure`, disabling TLS)
- **Pin external references** to specific versions when possible
- **Test skill instructions** to confirm they do not produce unintended side effects when followed by an
  AI agent
