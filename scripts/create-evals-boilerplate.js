#!/usr/bin/env node
"use strict";

const fs = require("fs");

const skillName = process.argv[2];
if (!skillName) {
  console.error("Usage: create-evals-boilerplate.js <skill-name>");
  process.exit(1);
}

const evals = [
  {
    id: "example-eval",
    prompt: "TODO - describe what the user asks",
    expected_output: "TODO - describe expected agent behavior",
    assertions: ["TODO - specific assertion about the response"],
    files: [skillName + "/SKILL.md"],
  },
];

fs.writeFileSync(
  skillName + "/evals/evals.json",
  JSON.stringify(evals, null, 2) + "\n"
);
