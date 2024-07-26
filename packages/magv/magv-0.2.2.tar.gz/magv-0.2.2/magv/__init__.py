import os
import json
import logging

name = "magv"

config_sample = '''{
    "Index-Repo" : ["https://atomgit.com/zouxiangneihe/magv-index.git"]
}'''

VERSION = "0.2.2"

def verify_version():
    try:
        with open(os.path.expanduser("~/.magv/VERSION"), "r") as f:
            if f.read() == VERSION:
                f.close()
                return True
    except:
        return False
    return False

def write_version():
    with open(os.path.expanduser("~/.magv/VERSION"), "w+") as f:
        f.write(VERSION)
        f.close()

def get_local_name(repo_name):
    l = -1
    r = -1
    for i in range(len(repo_name) - 1, -1, -1):
        if l == -1 and repo_name[i] == '/': # Find the last slash
            l = i
        if r == -1 and repo_name[i] == '.': # And the last dot
            r = i
    return repo_name[l + 1 : r]

def init_repo(jsonb, basedir):
    dist = jsonb['Index-Repo']
    for i in dist:
        os.makedirs(os.path.join(basedir, get_local_name(i)), exist_ok = True)
        os.system(f"git clone {i} {os.path.join(basedir, get_local_name(i))}")

def update_repo(jsonb, basedir):
    dist = jsonb['Index-Repo']
    current_working_dir = os.getcwd()
    for i in dist:
        repo_path = os.path.join(basedir, get_local_name(i))
        os.chdir(repo_path)
        os.system(f"git pull")
    os.chdir(current_working_dir)

def repo_paths(jsonb, basedir):
    dist = jsonb['Index-Repo']
    res = list()
    for i in dist:
        repo_path = os.path.join(basedir, get_local_name(i))
        res.append(repo_path)
    return res

class magv_config:
    def __init__(self):
        self.logger = logging.getLogger("MANGROVE")
        self.config_json = os.path.expanduser("~/.magv/config.json")
        self.config_path = os.path.expanduser("~/.magv")
        self.log_path = os.path.expanduser("~/.magv/magv.log")
        try:
            FIRST_RUN = False
            if not os.path.isfile(self.config_json):
                os.makedirs(self.config_path, exist_ok = True)
                with open(self.config_json, "w+") as f:
                    f.write(config_sample)
                    f.close()
                FIRST_RUN = True
                write_version()
            if verify_version() == False:
                print("ERROR: Version check failed. Please manually update config file")
                exit(1)
            logging.basicConfig(filename=os.path.expanduser("~/.magv/magv.log"), level=logging.DEBUG, filemode="w+")
            with open(self.config_json) as f:
                self.config = json.loads(f.read())
                f.close()
                if FIRST_RUN:
                    init_repo(self.config, self.config_path)
                    print("WARNING: YOU SHOULD CHANGE YOUR CONFIGURE FILE MANUALLY AT ~/.magv/config.json TO USE MANGROVE")
                    self.logger.warning("WARNING: YOU SHOULD CHANGE YOUR CONFIGURE FILE MANUALLY AT ~/.magv/config.json TO USE MANGROVE")
                else:
                    update_repo(self.config, self.config_path)
            self.repo_path = repo_paths(self.config, self.config_path)
        except Exception as e:
            self.logger.fatal("An error occured while initialization")
            self.logger.fatal(e)
            exit(1)