#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""install.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

Linux用インストーラ。
"""
import os as __os
import sys as __sys
import shutil as __shutil
__shell_script = __os.path.join(__sys.exec_prefix, "games", "starseeker")
__icon = __os.path.join(__sys.exec_prefix, "share", "icons", "starseeker.png")
__source = __os.path.join(__sys.exec_prefix, "share", "games", "StarSeeker")
__desktop_entry = __os.path.join(
    __sys.exec_prefix, "share", "applications", "StarSeeker.desktop")


def __install():
    u"""ゲームをインストール。
    """
    print "Start installation."
    print "---- Set shell script ----"
    startup_file = __os.path.join("linux", "startup.sh")
    __os.chmod(startup_file, 0o755)
    __shutil.copy(startup_file, __shell_script)
    print "---- Set icon ----"
    icon_file = __os.path.join("linux", "icon.png")
    __os.chmod(icon_file, 0o644)
    __shutil.copy(icon_file, __icon)
    print "---- Set source ----"
    for root, dirs, files in __os.walk("Source"):
        for dir_ in dirs:
            __os.chmod(__os.path.join(root, dir_), 0o755)
        for file_ in files:
            __os.chmod(__os.path.join(root, file_), 0o755)
    if __os.path.exists(__source):
        __shutil.rmtree(__source)
    __shutil.copytree("Source", __source)
    print "---- Set desktop entry ----"
    entry_file = __os.path.join("linux", "Entry.desktop")
    __os.chmod(entry_file, 0o644)
    __shutil.copy(entry_file, __desktop_entry)
    print "Installation is finished."


def __uninstall():
    u"""ゲームをアンインストール。
    """
    print "Start uninstallation."
    print "---- Remove shell script ----"
    try:
        __os.remove(__shell_script)
    except OSError:
        print "Shell script does not exsit."
    print "---- Remove icon ----"
    try:
        __os.remove(__icon)
    except OSError:
        print "Icon does not exsit."
    print "---- Remove source ----"
    if __os.path.exists(__source):
        __shutil.rmtree(__source)
    else:
        print "Source does not exsit."
    print "---- Remove desktop entry ----"
    try:
        __os.remove(__desktop_entry)
    except OSError:
        print "Desktop entry does not exsit."
    print "Uninstallation is finished."


if __name__ == '__main__':
    if 1 < len(__sys.argv) and __sys.argv[-1] == "-u":
        __uninstall()
    else:
        __install()
