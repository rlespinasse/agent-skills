#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const skills = [];
for (const entry of fs.readdirSync("skills", { withFileTypes: true })) {
  if (!entry.isDirectory()) continue;
  const skillPath = path.join("skills", entry.name, "SKILL.md");
  if (!fs.existsSync(skillPath)) continue;
  const content = fs.readFileSync(skillPath, "utf8");
  const frontmatter = content.split("---")[1] || "";
  const lines = frontmatter.split("\n");
  let desc = "";
  let capturing = false;
  for (const line of lines) {
    if (/^description:\s*/.test(line)) {
      desc = line.replace(/^description:\s*/, "").trim();
      capturing = true;
    } else if (capturing && /^\s+/.test(line)) {
      desc += " " + line.trim();
    } else if (capturing) {
      break;
    }
  }
  skills.push({ name: entry.name, path: `skills/${entry.name}`, description: desc });
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
