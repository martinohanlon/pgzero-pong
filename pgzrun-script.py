#!C:\Python34\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'pgzero==1.1','console_scripts','pgzrun'
__requires__ = 'pgzero==1.1'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('pgzero==1.1', 'console_scripts', 'pgzrun')()
    )
