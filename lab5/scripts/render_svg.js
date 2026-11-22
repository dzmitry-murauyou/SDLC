const fs = require('node:fs');
const path = require('node:path');
const { Resvg } = require('@resvg/resvg-js');
const directory = path.resolve(__dirname, '..', 'diagrams');
for (const name of ['use-case', 'activity', 'state', 'sequence']) {
  const input = path.join(directory, `${name}.svg`);
  const output = path.join(directory, `${name}.png`);
  const renderer = new Resvg(fs.readFileSync(input, 'utf8'));
  fs.writeFileSync(output, renderer.render().asPng());
  console.log(`Rendered ${output}`);
}
