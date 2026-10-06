import os
import shutil

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_DIR = os.path.join(ROOT_DIR, 'public')

def sync():
    print('[SYNC] Starting Python build sync: root -> public/...')
    
    # 1. index.html
    shutil.copy2(os.path.join(ROOT_DIR, 'index.html'), os.path.join(PUBLIC_DIR, 'index.html'))
    print('  - Synced index.html')
    
    # 2. js/
    dest_js = os.path.join(PUBLIC_DIR, 'js')
    if os.path.exists(dest_js):
        shutil.rmtree(dest_js)
    shutil.copytree(os.path.join(ROOT_DIR, 'js'), dest_js)
    print('  - Synced js/')
    
    # 3. css/
    dest_css = os.path.join(PUBLIC_DIR, 'css')
    if os.path.exists(dest_css):
        shutil.rmtree(dest_css)
    shutil.copytree(os.path.join(ROOT_DIR, 'css'), dest_css)
    print('  - Synced css/')
    
    # 4. data/
    dest_data = os.path.join(PUBLIC_DIR, 'data')
    if os.path.exists(dest_data):
        shutil.rmtree(dest_data)
    shutil.copytree(os.path.join(ROOT_DIR, 'data'), dest_data)
    print('  - Synced data/')
    
    print('[SYNC] Sync completed successfully!')

if __name__ == '__main__':
    sync()
