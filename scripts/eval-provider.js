#!/usr/bin/env node
"use strict";

// Custom promptfoo provider that uses Claude Code CLI for evaluation.
//
// This provider calls `claude -p` to generate responses and judge assertions.
// It works with a Claude Code Max subscription (no API key needed).
//
// NOTE: Running evals consumes Claude Code rate limits.
// Sponsorship or API credits would allow faster, parallelized eval runs.
// See: https://github.com/rlespinasse/agent-skills (Sponsor section)

const { spawnSync } = require("child_process");
const fs = require("fs");
const path = require("path");

class ClaudeCodeProvider {
  constructor(options) {
    this.config = options.config || {};
  }

  id() {
    return "claude-code";
  }

  async callApi(prompt, context) {
    // If context has skill files, prepend their content for grounded answers
    const filesRaw = context.vars && context.vars.context_files;
    let fileContext = "";

    if (filesRaw) {
      const files = filesRaw.split(",").filter(Boolean);
      for (const file of files) {
        const filePath = path.resolve(file.trim());
        if (fs.existsSync(filePath)) {
          const content = fs.readFileSync(filePath, "utf-8");
          fileContext += `<file path="${file.trim()}">\n${content}\n</file>\n\n`;
        }
      }
    }

    const fullPrompt = fileContext
      ? `You are an AI coding assistant with the following skill files loaded.\n` +
        `Use ONLY these files to answer. Do not make up information.\n\n` +
        `${fileContext}` +
        `User question: ${prompt}`
      : prompt;

    try {
      const result = spawnSync("claude", ["-p", fullPrompt, "--output-format", "text"], {
        encoding: "utf-8",
        timeout: 180000,
        maxBuffer: 2 * 1024 * 1024,
      });

      if (result.error) {
        return { error: `Claude Code error: ${result.error.message}` };
      }
      if (result.status !== 0) {
        const stderr = (result.stderr || "").trim();
        return { error: `Claude Code exit ${result.status}: ${stderr}` };
      }

      return { output: result.stdout.trim() };
    } catch (err) {
      return { error: `Provider error: ${err.message}` };
    }
  }
}

module.exports = ClaudeCodeProvider;
