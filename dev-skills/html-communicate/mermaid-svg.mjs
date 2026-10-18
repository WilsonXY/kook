#!/usr/bin/env node
// Mermaid on stdin -> SVG on stdout, drawn by Pele (https://pele.run, MIT).
// Installs the pinned Pele into the user cache on first run. Usage: node mermaid-svg.mjs < diagram.mmd > diagram.svg
import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, renameSync, rmSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, join } from 'node:path';
import { pathToFileURL } from 'node:url';

const version = '1.6.0';
const dir = join(process.env.XDG_CACHE_HOME || join(homedir(), '.cache'), `pele-${version}`);
const entry = join(dir, 'node_modules/pele/dist/pele.js');
if (!existsSync(entry)) {
  // Install into a private folder, then rename it into place, so a crash or a parallel first run never leaves a half-installed cache.
  mkdirSync(dirname(dir), { recursive: true });
  const tmp = mkdtempSync(`${dir}.tmp-`);
  try {
    execFileSync('npm', ['install', '--prefix', tmp, '--ignore-scripts', '--no-audit', '--no-fund', `pele@${version}`],
      { stdio: ['ignore', 2, 2] }); // npm's output to stderr, so stdout stays the SVG
    renameSync(tmp, dir);
  } catch (e) {
    rmSync(tmp, { recursive: true, force: true });
    if (!existsSync(entry)) throw e; // fine if a parallel run got there first
  }
}
const { render } = await import(pathToFileURL(entry).href);
process.stdout.write(render(readFileSync(0, 'utf8')).svg + '\n');
