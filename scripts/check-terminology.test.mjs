import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const fixtureRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'terminology-gate-'));
fs.mkdirSync(path.join(fixtureRoot, 'architecture'), { recursive: true });
fs.mkdirSync(path.join(fixtureRoot, 'diagrams'), { recursive: true });
fs.mkdirSync(path.join(fixtureRoot, 'scripts'), { recursive: true });

fs.copyFileSync('scripts/check-terminology.mjs', path.join(fixtureRoot, 'scripts/check-terminology.mjs'));
fs.copyFileSync('terminology-rules.json', path.join(fixtureRoot, 'terminology-rules.json'));

fs.writeFileSync(path.join(fixtureRoot, 'architecture/pass.md'), [
  '# 测试',
  '运行时（Runtime）负责记录事实。',
  '`Runtime` 是代码标识示例。',
  '```text',
  'Runtime',
  '```',
].join('\n'));

fs.writeFileSync(path.join(fixtureRoot, 'diagrams/pass.architecture.json'), JSON.stringify({
  schema_version: 1,
  diagram_type: 'architecture',
  components: [
    { id: 'runtime', type: 'backend', label: '运行时', sublabel: '记录执行事实', sources: [{ label: 'Runtime' }] },
  ],
}, null, 2));

execFileSync(process.execPath, ['scripts/check-terminology.mjs'], { cwd: fixtureRoot, stdio: 'pipe' });

fs.writeFileSync(path.join(fixtureRoot, 'architecture/fail.md'), '# 测试\nRuntime 负责记录事实。\n');
let failed = false;
try {
  execFileSync(process.execPath, ['scripts/check-terminology.mjs'], { cwd: fixtureRoot, stdio: 'pipe' });
} catch (error) {
  failed = true;
  const stderr = error.stderr.toString();
  assert.match(stderr, /architecture\/fail\.md/);
  assert.match(stderr, /Runtime/);
  assert.match(stderr, /运行时/);
}

assert.equal(failed, true, '裸英文术语应触发失败');
console.log('Terminology gate tests passed.');
