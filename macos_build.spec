# -*- mode: python ; coding: utf-8 -*-
"""
Example build.spec file
This hits most of the major notes required for
building a stand alone version of your Gooey application.
"""


import os
import platform
import gooey
gooey_root = os.path.dirname(gooey.__file__)
gooey_languages = Tree(os.path.join(gooey_root, 'languages'), prefix = 'gooey/languages')
gooey_images = Tree(os.path.join(gooey_root, 'images'), prefix = 'gooey/images')

from PyInstaller.building.api import EXE, PYZ, COLLECT
from PyInstaller.building.build_main import Analysis
from PyInstaller.building.datastruct import Tree
from PyInstaller.building.osx import BUNDLE

block_cipher = None

a = Analysis(['od_normalizer.py'],  # The local path to the script for compilation
             pathex=['/Users/bermanlab/Dropbox (Berman Lab)/Berman Lab Staff Files/Vladimir/od_normalizer.py'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             )
pyz = PYZ(a.pure)

options = [('u', None, 'OPTION'), ('v', None, 'OPTION'), ('w', None, 'OPTION')]


exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          options,
          gooey_languages,
          gooey_images,
          name='od_normalizer',
          debug=False,
          strip=None,
          upx=True,
          console=False,
          icon=os.path.join(gooey_root, 'images', 'program_icon.ico'))

info_plist = {'addition_prop': 'additional_value'}
app = BUNDLE(exe,
             name='od_normalizer.app',
             bundle_identifier=None,
             info_plist=info_plist
            )