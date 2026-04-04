# Agent Skills Development Justfile
# https://github.com/casey/just

set quiet := true

import 'just/quality.just'
import 'just/skills.just'
import 'just/documentation.just'
import 'just/development.just'
import 'just/python.just'

# List available recipes
default:
    just --list

# Auto-fix formatting, sync generated files, and run all checks
autofix: format sync fix check
    echo "✅ All autofix steps completed"

# Validate commit message format
[group('release')]
validate-commit message:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "✅ Validating commit message..."
    echo "{{ message }}" | npx -y -p @commitlint/cli -p @commitlint/config-conventional commitlint
