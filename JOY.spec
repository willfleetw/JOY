# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['src/JOY.py'],
             pathex=['./venv/Lib/site-packages/', '.'],
             binaries=[],
             datas=[('./venv/Lib/site-packages/vosk', './vosk')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='JOY',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          clean=True,
          icon='res/JOY.ico',
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )

import shutil
shutil.copyfile('JOY.yml', '{0}/JOY.yml'.format(DISTPATH))
shutil.copyfile('README.md', '{0}/README.md'.format(DISTPATH))
shutil.copytree('model', '{0}/model'.format(DISTPATH), dirs_exist_ok=True)
shutil.copytree('res', '{0}/res'.format(DISTPATH), dirs_exist_ok=True)