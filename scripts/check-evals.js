#!/usr/bin/env node
"use strict";

const fs = require("fs");

const filePath = process.argv[2];
if (!filePath) {
  console.error("Usage: check-evals.js <evals.json>");
  process.exit(1);
}

const evals = JSON.parse(fs.readFileSync(filePath, "utf8"));
if (!Array.isArray(evals)) {
  console.log("  ❌ ERROR: evals.json must be a JSON array");
  process.exit(1);
}

let valid = true;
const ids = new Set();

evals.forEach((e, i) => {
  const missing = [];
  if (!e.id) missing.push("id");
  if (!e.prompt) missing.push("prompt");
  if (!e.expected_output) missing.push("expected_output");
  if (!e.assertions || !Array.isArray(e.assertions) || e.assertions.length === 0) missing.push("assertions[]");
  if (!e.files || !Array.isArray(e.files) || e.files.length === 0) missing.push("files[]");
  if (missing.length > 0) {
    console.log("  ❌ ERROR: eval[" + i + "] missing required fields: " + missing.join(", "));
    valid = false;
  }
  if (e.id && ids.has(e.id)) {
    console.log("  ❌ ERROR: duplicate eval id: " + e.id);
    valid = false;
  }
  if (e.id) ids.add(e.id);
});

if (!valid) process.exit(1);
console.log("  ✅ " + evals.length + " evals validated");
