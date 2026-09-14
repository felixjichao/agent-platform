import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const configPath = path.join(root, 'terminology-rules.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

const targetRoots = [
  path.join(root, 'architecture'),
  path.join(root, 'diagrams'),
];

const visibleJsonKeys = new Set([
  'title',
  'subtitle',
  'label',
  'sublabel',
  'tag',
  'note',
  'items',
]);

function walk(dir) {
  if (!fs.existsSync(dir)) return [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  return entries.flatMap((entry) => {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) return walk(full);
    return [full];
  });
}

function relative(file) {
  return path.relative(root, file).split(path.sep).join('/');
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function makeTermRegex(term) {
  const escaped = escapeRegExp(term);
  const startsWord = /[A-Za-z0-9]/.test(term[0]);
  const endsWord = /[A-Za-z0-9]/.test(term[term.length - 1]);
  return new RegExp(`${startsWord ? '\\b' : ''}${escaped}${endsWord ? '\\b' : ''}`, 'g');
}

function insideParentheses(text, start, end) {
  const prefix = text.slice(0, start);
  const open = Math.max(prefix.lastIndexOf('（'), prefix.lastIndexOf('('));
  const closeBefore = Math.max(prefix.lastIndexOf('）'), prefix.lastIndexOf(')'));
  if (open <= closeBefore) return false;

  const suffix = text.slice(end);
  const closes = [suffix.indexOf('）'), suffix.indexOf(')')].filter((index) => index >= 0);
  return closes.length > 0;
}

function isAllowlisted(file, term) {
  if (config.allowedEnglish?.includes(term)) return true;
  return config.fileAllowlist?.[file]?.includes(term) ?? false;
}

function findViolations(text, file, location) {
  const violations = [];
  const occupied = [];

  const rules = [
    ...(config.forbiddenEnglish ?? []).map((rule) => ({ ...rule, allowParenthetical: true })),
    ...(config.forbiddenChinese ?? []).map((rule) => ({ ...rule, allowParenthetical: false })),
  ].sort((a, b) => b.term.length - a.term.length);

  for (const rule of rules) {
    if (isAllowlisted(file, rule.term)) continue;

    const regex = makeTermRegex(rule.term);
    for (const match of text.matchAll(regex)) {
      const start = match.index;
      const end = start + match[0].length;

      if (occupied.some(([left, right]) => start < right && end > left)) continue;
      if (rule.allowParenthetical && insideParentheses(text, start, end)) continue;

      occupied.push([start, end]);
      violations.push({
        file,
        location,
        term: rule.term,
        recommended: rule.recommended,
      });
    }
  }

  return violations;
}

function scanMarkdown(file) {
  const rel = relative(file);
  const lines = fs.readFileSync(file, 'utf8').split(/\r?\n/);
  const violations = [];
  let fence = null;

  lines.forEach((line, index) => {
    const trimmed = line.trimStart();
    const fenceMatch = trimmed.match(/^(```|~~~)/);
    if (fenceMatch) {
      if (fence === null) fence = fenceMatch[1];
      else if (fence === fenceMatch[1]) fence = null;
      return;
    }
    if (fence !== null) return;

    let visible = line;
    visible = visible.replace(/`[^`]*`/g, '');
    visible = visible.replace(/\[([^\]]*)\]\([^)]*\)/g, '$1');

    violations.push(...findViolations(visible, rel, `line ${index + 1}`));
  });

  return violations;
}

function collectVisibleJson(node, jsonPath = '$', values = []) {
  if (Array.isArray(node)) {
    node.forEach((value, index) => collectVisibleJson(value, `${jsonPath}[${index}]`, values));
    return values;
  }

  if (node === null || typeof node !== 'object') return values;

  for (const [key, value] of Object.entries(node)) {
    if (key === 'sources') continue;
    const nextPath = `${jsonPath}.${key}`;

    if (visibleJsonKeys.has(key)) {
      if (typeof value === 'string') {
        values.push({ text: value, jsonPath: nextPath });
      } else if (Array.isArray(value)) {
        value.forEach((item, index) => {
          if (typeof item === 'string') {
            values.push({ text: item, jsonPath: `${nextPath}[${index}]` });
          } else {
            collectVisibleJson(item, `${nextPath}[${index}]`, values);
          }
        });
      } else {
        collectVisibleJson(value, nextPath, values);
      }
      continue;
    }

    if (typeof value === 'object') collectVisibleJson(value, nextPath, values);
  }

  return values;
}

function scanArchitectureJson(file) {
  const rel = relative(file);
  const raw = fs.readFileSync(file, 'utf8');
  const data = JSON.parse(raw);
  const visibleValues = collectVisibleJson(data);
  return visibleValues.flatMap(({ text, jsonPath }) => findViolations(text, rel, jsonPath));
}

const files = targetRoots.flatMap(walk).filter((file) => {
  const rel = relative(file);
  return rel.startsWith('architecture/') && rel.endsWith('.md')
    || rel.startsWith('diagrams/') && rel.endsWith('.architecture.json');
});

const violations = files.flatMap((file) => {
  if (file.endsWith('.architecture.json')) return scanArchitectureJson(file);
  return scanMarkdown(file);
});

if (violations.length > 0) {
  console.error(`Terminology check failed with ${violations.length} violation(s):`);
  for (const violation of violations) {
    const where = violation.location ? ` (${violation.location})` : '';
    console.error(`- ${violation.file}${where}: "${violation.term}" → use "${violation.recommended}"`);
    console.error(`::error file=${violation.file},title=Terminology::${violation.term} → ${violation.recommended}`);
  }
  process.exit(1);
}

console.log(`Terminology check passed: ${files.length} file(s) scanned.`);
console.log(`Allowed standards/identifiers: ${(config.allowedEnglish ?? []).join(', ')}`);
