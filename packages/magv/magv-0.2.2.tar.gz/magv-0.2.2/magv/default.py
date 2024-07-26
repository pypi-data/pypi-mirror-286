import magv.gitrepo as gitrepo
import json
import os
from magv import get_local_name

def download(path, ext, ver, repo, config):
    try:
        with open(os.path.join(config.config_path, repo, f"{ext}.json"), "r") as f:
            dist = json.loads(f.read())
            f.close()
    except Exception:
        config.logger.error("Extension not found")
        raise Exception("Extension not found")
    try:
        gitrepo.download(path, dist["repo"], ver, config)
        with open(os.path.join(path, ".REQUIREMENTS"), "w+") as f:
            f.write(str(dist["requirements"]))
            f.close()
        try:
            if dist["privilege"] == True:
                with open(os.path.join(path, ".PRIVILEGE"), "w+") as f:
                    f.write("True")
                    f.close()
        except:
            return
    except Exception as e:
        config.logger.error("An error occured while downloading extension")
        config.logger.error(e)
        raise e

def search(ext, config):
    try:
        for repodir in config.repo_path:
            dist = os.listdir(repodir)
            res = list()
            for i in dist:
                if not i.find(ext) == -1:
                    with open(os.path.join(repodir, i), "r") as f:
                        item = json.loads(f.read())
                        f.close()
                        res.append([i.rsplit(".", 1)[0], "MANGROVE", get_local_name(repodir + "."), item["abstract"]]) # Strip the ".json" part
    except Exception as e:
        config.logger.error("An error occured while searching extension")
        raise e
    return res