/**
 * scripts/batch_parse_n2.js
 * Runner for JLPT N2 Batch Parser & Standardizer.
 * Executes Python 3.12 batch parser engine and reports progress.
 */

const { spawn } = require('child_process');
const path = require('path');

const rootDir = path.dirname(__dirname);
const scriptPath = path.join(rootDir, 'scripts', 'batch_parse_n2.py');

console.log('='.repeat(60));
console.log('Starting JLPT N2 Batch Parser via Node.js runner...');
console.log(`Script: ${scriptPath}`);
console.log('='.repeat(60));

const pythonExe = process.env.PYTHON_PATH || 'C:\\Users\\default.LAPTOP-ECP2IL69\\AppData\\Local\\Programs\\Python\\Python312\\python.exe';

const child = spawn(pythonExe, [scriptPath], {
  cwd: rootDir,
  env: {
    ...process.env,
    PYTHONIOENCODING: 'utf-8'
  }
});

child.stdout.on('data', (data) => {
  process.stdout.write(data.toString());
});

child.stderr.on('data', (data) => {
  process.stderr.write(data.toString());
});

child.on('close', (code) => {
  console.log(`\nBatch parse finished with exit code ${code}`);
  process.exit(code);
});
