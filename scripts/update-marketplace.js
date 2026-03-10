#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const skills = [];
for (const entry of fs.readdirSync(".", { withFileTypes: true })) {
  if (!entry.isDirectory()) continue;
  const skillPath = path.join(entry.name, "SKILL.md");
  if (!fs.existsSync(skillPath)) continue;
  const content = fs.readFileSync(skillPath, "utf8");
  const descMatch = content.match(/^description:\s*(.+)/m);
  const desc = descMatch ? descMatch[1].trim() : "";
  skills.push({ name: entry.name, path: entry.name, description: desc });
}

const manifest = {
  name: "agent-skills",
  owner: "rlespinasse",
  description: "A collection of Agent Skills for AI coding assistants",
  repository: "https://github.com/rlespinasse/agent-skills",
  skills,
  metadata: {
    specification: "https://agentskills.io/specification",
    author: "@rlespinasse",
    license: "MIT",
  },
};

fs.writeFileSync(
  ".claude-plugin/marketplace.json",
  JSON.stringify(manifest, null, 2) + "\n"
);
