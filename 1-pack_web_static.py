#!/usr/bin/python3
"""generates a .tgz archive from the contents of the web_static"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """generates a .tgz archive from the contents of the web_static
    """
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    path = 'versions/web_static_{}.tgz'.format(now)

    local('mkdir -p versions/')
    createArchive = local('tar -cvzf {} web_static/'.format(path))

    if createArchive.failed:
        return None
    return path
