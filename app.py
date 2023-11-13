import os
import platform
import sys
import zipfile

import requests

import base
import gui_server
from gui_server import app


py_version = list(map(int, platform.python_version().split('.')))
if not (py_version[0] >= 3 and py_version[1] >= 10):
    print(f'Python 3.10 or above version is required! The app is running on Pyhon {platform.python_version()} now!')
    sys.exit(-1)

app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
requirements_js = [
    {
        'name': 'mdui',
        'res_path': os.path.join(app_dir, 'static', 'mdui'),
        'is_exist': os.path.exists(os.path.join(app_dir, 'static', 'mdui', 'css', 'mdui.min.css')) and os.path.exists(
            os.path.join(app_dir, 'static', 'mdui', 'js', 'mdui.min.js')),
        'download_url': 'https://cdn.w3cbus.com/mdui.org/mdui-v1.0.1.zip',
        'is_zip': True,
        'zip_name': os.path.join(app_dir, 'tmp.zip')
    }, {
        'name': 'jQuery',
        'res_path': os.path.join(app_dir, 'static', 'jquery', 'js', 'jquery.min.js'),
        'is_exist': os.path.exists(os.path.join(app_dir, 'static', 'jquery', 'js', 'jquery.min.js')),
        'download_url': 'https://cdn.bootcdn.net/ajax/libs/jquery/3.7.1/jquery.min.js',
        'is_zip': False,
        'zip_name': ''
    }, {
        'name': 'Viewer.js - js',
        'res_path': os.path.join(app_dir, 'static', 'viewerjs', 'js', 'viewer.min.js'),
        'is_exist': os.path.exists(os.path.join(app_dir, 'static', 'viewerjs', 'js', 'viewer.min.js')),
        'download_url': 'https://cdn.bootcdn.net/ajax/libs/viewerjs/1.11.5/viewer.min.js',
        'is_zip': False,
        'zip_name': ''
    }, {
        'name': 'Viewer.js - css',
        'res_path': os.path.join(app_dir, 'static', 'viewerjs', 'css', 'viewer.min.css'),
        'is_exist': os.path.exists(os.path.join(app_dir, 'static', 'viewerjs', 'css', 'viewer.min.css')),
        'download_url': 'https://cdn.bootcdn.net/ajax/libs/viewerjs/1.11.5/viewer.min.css',
        'is_zip': False,
        'zip_name': ''
    }, {
        'name': 'Geetest 3 - SDK',
        'res_path': os.path.join(app_dir, 'static', 'geetest-sdk', 'js', 'gt.0.4.9.js'),
        'is_exist': os.path.exists(os.path.join(app_dir, 'static', 'geetest-sdk', 'js', 'gt.0.4.9.js')),
        'download_url': 'https://static.geetest.com/static/js/gt.0.4.9.js',
        'is_zip': False,
        'zip_name': ''
    },
]

for requirement in requirements_js:
    try:
        if not requirement['is_exist']:
            print(f"The resources of {requirement['name']} is missing, downloading...", end='')
            # messagebox.showinfo("请稍后", f"正在下载{requirement['name']}...")
            conn = requests.get(requirement['download_url'])
            print('\tdownloaded, writing to file...', end='')
            if requirement['is_zip']:
                with open(requirement['zip_name'], mode='wb') as f:
                    f.write(conn.content)
                zipfile.ZipFile(requirement['zip_name']).extractall(requirement['res_path'])
                os.remove(requirement['zip_name'])
            else:
                if not os.path.exists(os.path.dirname(requirement['res_path'])):
                    os.makedirs(os.path.dirname(requirement['res_path']))
                with open(requirement['res_path'], mode='wb') as f:
                    f.write(conn.content)
            print('\tfinished!')
    except:
        print('\nAn error was occurred and download had been interrupted, exiting...')
        sys.exit(255)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)