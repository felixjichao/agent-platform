import { existsSync, readFileSync, writeFileSync } from 'node:fs'
import { dirname, resolve } from 'node:path'

const archifyBin = process.argv[2]

if (!archifyBin) {
  console.error('Usage: node scripts/patch-archify-readability.mjs <archify-bin>')
  process.exit(1)
}

const rendererPath = resolve(
  dirname(archifyBin),
  '..',
  'renderers',
  'architecture',
  'render-architecture.mjs'
)

if (!existsSync(rendererPath)) {
  console.error(`Archify architecture renderer not found: ${rendererPath}`)
  process.exit(1)
}

let source = readFileSync(rendererPath, 'utf8')

function replaceOnce(label, before, after) {
  const first = source.indexOf(before)
  if (first === -1) {
    throw new Error(`Unable to apply ${label}: expected Archify source was not found`)
  }

  if (source.indexOf(before, first + before.length) !== -1) {
    throw new Error(`Unable to apply ${label}: expected Archify source is ambiguous`)
  }

  source = `${source.slice(0, first)}${after}${source.slice(first + before.length)}`
}

replaceOnce(
  'component secondary text readability',
  `const componentTextFit = {
  sublabelPreferred: 9,
  sublabelMinimum: 6,
  tagPreferred: 7,
  tagMinimum: 6,
};`,
  `const componentTextFit = {
  sublabelPreferred: 11,
  sublabelMinimum: 8,
  tagPreferred: 9,
  tagMinimum: 7,
};`
)

replaceOnce(
  'boundary title readability',
  `  boundaryLabelFontPreferred: 9,
  boundaryLabelFontMinimum: 6,`,
  `  boundaryLabelFontPreferred: 11,
  boundaryLabelFontMinimum: 8,`
)

replaceOnce(
  'component primary label readability',
  'const labelFontSize = fittedNodeFontSize(c.label, brandLabelFitWidth(c, c.width), 11, 8);',
  'const labelFontSize = fittedNodeFontSize(c.label, brandLabelFitWidth(c, c.width), 12, 9);'
)

writeFileSync(rendererPath, source)
console.log(`Applied Agent Platform readability profile to ${rendererPath}`)
