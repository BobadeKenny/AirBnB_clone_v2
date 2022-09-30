#!/usr/bin/python3
"""creates and distributes an archive to your web servers
"""
import os.path
from fabric.api import env, put, run, local
from datetime import datetime

env.user = "ubuntu"
env.hosts = ["44.210.105.150", "3.238.104.46"]


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


def do_deploy(archive_path):
    """Distributes an archive to a web server
       Returns True if successful and false if not
    """
    if os.path.isfile(archive_path) is False:
        return False
    fullFile = archive_path.split("/")[-1]
    folder = fullFile.split(".")[0]

    # Uploads archive to /tmp/ directory
    if put(archive_path, "/tmp/{}".format(fullFile)).failed is True:
        print("Uploading archive to /tmp/ failed")
        return False

    # Delete the archive folder on the server
    if run("rm -rf /data/web_static/releases/{}/".
           format(folder)).failed is True:
        print("Deleting folder with archive(if already exists) failed")
        return False

    # Create a new archive folder
    if run("mkdir -p /data/web_static/releases/{}/".
           format(folder)).failed is True:
        print("Creating new archive folder failed")
        return False

    # Uncompress archive to /data/web_static/current/ directory
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(fullFile, folder)).failed is True:
        print("Uncompressing archive to failed")
        return False

    # Deletes latest archive from the server
    if run("rm /tmp/{}".format(fullFile)).failed is True:
        print("Deleting archive from /tmp/ directory dailed")
        return False

    # Move folder from web_static to its parent folder, to expose
    # the index files outsite the /we_static path
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".
           format(folder, folder)).failed is True:
        print("Moving content to archive folder before deletion failed")
        return False

    # Delete the empty web_static file, as its content have been moved
    # to its parent directory
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(folder)).failed is True:
        print("Deleting web_static folder failed")
        return False

    # Delete current folder being served (the symbolic link)
    if run("rm -rf /data/web_static/current").failed is True:
        print("Deleting 'current' folder failed")
        return False

    # Create new symbolic link on web server linked to new code version
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(folder)).failed is True:
        print("Creating new symbolic link to new code version failed")
        return False

    print("New version deployed!")
    return True


def deploy():
    """Creates archive then distributes it to a web server."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)