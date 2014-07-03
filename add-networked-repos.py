#!/usr/bin/python

import urllib2
import json
import subprocess
import argparse

URL = "https://api.github.com/repos/%s/%s/forks"
REPO_URL = "https://github.com/%s/%s"
p = subprocess.Popen(['git', 'config', 'github.user'],
                     stdout=subprocess.PIPE)
login = p.communicate()[0].strip()
p = subprocess.Popen(['git', 'config', 'github.password'],
                     stdout=subprocess.PIPE)
passwd = p.communicate()[0].strip()


def get_forks(repo):
    user, name = repo.split("/", 2)

    repo_url = URL % (user, name)
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, repo_url, login, passwd)
    auth_handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)
    response = urllib2.urlopen(repo_url)
    repos = json.load(response)
    for repo in repos:
        full_name = repo['full_name']
        f_user, f_name = full_name.split("/", 2)
        subprocess.call(['git', 'remote', 'add', f_user.lower(),
                        REPO_URL % (f_user, f_name)])
        subprocess.call(['git', 'fetch', f_user.lower()])
        get_forks(full_name)

parser = argparse.ArgumentParser()
parser.add_argument('fname_repo',
                    help="full name of the repo (e.g., user/name)")
args = parser.parse_args()

get_forks(args.fname_repo)
