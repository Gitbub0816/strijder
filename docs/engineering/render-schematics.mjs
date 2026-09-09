// Public PlantUML rendering only: no Java, Graphviz, or local layout engine.
// Running this submits the .puml sources in this directory to www.plantuml.com.
import { readdir, readFile, mkdir, writeFile } from 'node:fs/promises';
import { deflateRawSync } from 'node:zlib';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const root = path.dirname(fileURLToPath(import.meta.url));
const sourceDir = path.join(root, 'schematics');
const renderedDir = path.join(sourceDir, 'rendered');
const alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_';
function encode(bytes) {
  let result = '';
  for (let i = 0; i < bytes.length; i += 3) {
    const a = bytes[i], b = bytes[i + 1] ?? 0, c = bytes[i + 2] ?? 0;
    result += alphabet[a >> 2] + alphabet[((a & 3) << 4) | (b >> 4)]
      + alphabet[((b & 15) << 2) | (c >> 6)] + alphabet[c & 63];
  }
  return result;
}
await mkdir(renderedDir, { recursive: true });
for (const file of (await readdir(sourceDir)).filter(f => f.endsWith('.puml')).sort()) {
  const source = await readFile(path.join(sourceDir, file));
  const url = 'https://www.plantuml.com/plantuml/svg/' + encode(deflateRawSync(source));
  const svg = execFileSync('curl', ['--fail', '--silent', '--show-error', '--max-time', '45', url], { encoding: 'utf8', maxBuffer: 5_000_000 });
  if (!svg.includes('<svg') || /Syntax Error|Error line|An error has occur/i.test(svg)) {
    throw new Error(`Renderer did not return a valid diagram: ${file}`);
  }
  await writeFile(path.join(renderedDir, file.replace(/\.puml$/, '.svg')), svg);
  console.log(`${file}: ${Buffer.byteLength(svg)} bytes`);
}
