#!/usr/bin/env node
// Mermaid on stdin -> SVG on stdout, drawn by Pele (https://pele.run, MIT).
// Installs the pinned Pele into the user cache on first run. Usage: node mermaid-svg.mjs < diagram.mmd > diagram.svg
import { execFileSync } from 'node:child_process';
import { existsSync, readFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';

const version = '1.6.0';
const dir = join(process.env.XDG_CACHE_HOME || join(homedir(), '.cache'), `pele-${version}`);
const entry = join(dir, 'node_modules/pele/dist/pele.js');
if (!existsSync(entry)) {
  execFileSync('npm', ['install', '--prefix', dir, '--ignore-scripts', '--no-audit', '--no-fund', `pele@${version}`],
    { stdio: ['ignore', 2, 2] }); // npm's output to stderr, so stdout stays the SVG
}
const { render } = await import(pathToFileURL(entry).href);
process.stdout.write(render(readFileSync(0, 'utf8')).svg + '\n');
