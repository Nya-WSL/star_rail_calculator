'''
Author: Nya-WSL
Copyright © 2023 by Nya-WSL All Rights Reserved. 
Date: 2023-12-12 18:46:54
LastEditors: 狐日泽
LastEditTime: 2024-02-22 15:21:16
'''
import os
import subprocess
from pathlib import Path
import nicegui

cmd = [
    'pyinstaller',
    'main.py', # your main file with ui.run()
    '-w', # prevent console appearing, only use with ui.run(native=True, ...)
    '--add-data', f'{Path(nicegui.__file__).parent}{os.pathsep}nicegui',
    '-i', 'icon.ico'
]
subprocess.call(cmd)