/**
 * Synchronize root assets with public/ directory for Vercel deployment
 */
const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.resolve(__dirname, '..');
const PUBLIC_DIR = path.join(ROOT_DIR, 'public');

function copyRecursive(src, dest) {
  if (!fs.existsSync(src)) return;
  const stats = fs.statSync(src);
  if (stats.isDirectory()) {
    if (!fs.existsSync(dest)) {
      fs.mkdirSync(dest, { recursive: true });
    }
    const entries = fs.readdirSync(src);
    for (const entry of entries) {
      copyRecursive(path.join(src, entry), path.join(dest, entry));
    }
  } else {
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.copyFileSync(src, dest);
  }
}

console.log('[SYNC] Starting build sync: root -> public/...');

// 1. Sync index.html
copyRecursive(path.join(ROOT_DIR, 'index.html'), path.join(PUBLIC_DIR, 'index.html'));

// 2. Sync js/ directory
copyRecursive(path.join(ROOT_DIR, 'js'), path.join(PUBLIC_DIR, 'js'));

// 3. Sync css/ directory
copyRecursive(path.join(ROOT_DIR, 'css'), path.join(PUBLIC_DIR, 'css'));

// 4. Sync data/ directory
copyRecursive(path.join(ROOT_DIR, 'data'), path.join(PUBLIC_DIR, 'data'));

console.log('[SYNC] Build sync completed successfully!');
