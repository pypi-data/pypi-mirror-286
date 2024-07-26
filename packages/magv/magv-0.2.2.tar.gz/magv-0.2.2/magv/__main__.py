import os
import argparse
from tabulate import tabulate
import magv.default as default
import magv.pgxn as pgxn
import magv.install as install
from magv import magv_config
import magv.integrity as integrity

def search(ext, config):
    try:
        k = pgxn.search(ext, config) + default.search(ext, config)
        if len(k) == 0:
            print("No extension found.")
            exit(0)
        return k
    except Exception as e :
        config.logger.error(f"Failed to search {ext}")
        config.logger.error(f"e")
        exit(1)

def searchdownload(ext, config):
    try:
        k = pgxn.search(ext, config) + default.search(ext, config)
        if len(k) == 0:
            print("No extension found.")
            exit(0)
        print(tabulate(k, headers=['Extension', 'Source', 'Repo', 'Description'], showindex="always"))
        i = 0
        if not len(k) == 1:
            i = secure_input(f"Which extension to download? [0 ~ {len(k)- 1}] ", "int", 0, len(k) - 1)
        return (k[i][0], k[i][1], k[i][2])
    except Exception:
        config.logger.error(f"Failed to download {ext}")
        exit(1)

def download(path, ext, ver, source, repo, config):
    if ver == "latest":
        ver = "master"
    try:
        if source == "MANGROVE":
            default.download(path, ext, ver, repo, config)
        elif source == "PGXN":
            pgxn.download(path, ext, ver, config)
        integrity.create_int_file(path)
    except Exception:
        config.logger.error(f"Failed to download {ext}")
        exit(1)

def secure_input(hint, type, lower_bound = 0, upper_bound = 0):
    print(hint)
    if type == "str":
        k = input()
        while k.strip() == "":
            print(hint)
            k = input()
    elif type == "int":
        k = int(input())
        while k > upper_bound or k < lower_bound:
            print(hint)
            try:
                k = int(input())
            except ValueError: # e.g. a float num is given
                k = lower_bound - 1 # So the loop will excute again
    return k

def initialize_parser():
    parser = argparse.ArgumentParser(description = "MANGROVE - PostgreSQL Extension Network Client")
    parser.add_argument('-s', '--search', nargs = 1, help="Search for an extension", metavar = ("extension"))
    parser.add_argument('-d', '--download', nargs = 1, help="Download an extension", metavar = ("extension"))
    parser.add_argument('-i', '--install', nargs = 1, help="Install an extension", metavar = ("extension"))
    parser.add_argument('-p', '--path', nargs = 1, help = "Specify the installtion source / Download destination", metavar = "path")
    parser.add_argument('-v', '--version', nargs = 1, help = "Speicify which version to download or install", metavar = "version")
    parser.add_argument('-r', '--root', action = "store_true", help = "Install extension with root permission")
    return parser.parse_args()

if __name__ == "__main__":
    config = magv_config()
    try:
        if os.path.isfile(os.path.expanduser(config.config["Postscript"])):
            print("Executing initialization script!")
            os.system(f"sh {os.path.expanduser(config.config["Postscript"])}")
    except:
        config.logger.info("Failed to load postscript")

    arg = initialize_parser()
    path_  = arg.path
    
    if not arg.version == None:
        j = arg.version[0]
    else:
        j = "latest"

    if not arg.search == None:
        print(tabulate(search(arg.search[0], config), headers=['Extension', 'Source', 'Repo', 'Description'], showindex="always"))

    if not arg.download == None:
        k = searchdownload(arg.download[0], config)
        if path_ == None:
            path = os.path.join(config.config_path, k[0])
        else:
            path = path_[0]
        try:
            if os.path.isdir(path):
                option = input("Folder already exists, empty the folder? (Y/n)")
                if not (option == 'n' or option == 'N'):
                    os.system(f"rm -rf {path}")
            os.makedirs(path, exist_ok = True)
        except:
            config.logger.error(f"Failed to create directories at {path}")
            exit(1)
        download(path, k[0], j, k[1], k[2], config)

    if not arg.install == None:
        k = searchdownload(arg.install[0], config)
        choice = 'n'
        if path_ == None:
            path = os.path.join(config.config_path, k[0])
        else:
            path = path_[0]
        if os.path.exists(path):
            if integrity.integrity_check(path, config) == False:
                print("WARNING: Integrity check FAILED, the extension in your local folder might be broken or it might not be downloaded using Mangrove")
                choice = input("Proceed? (y/N) ")
            else:
                choice = input(f"It seems you've already downloaded {k[0]}, install from local folder? (y/N) ")
        if not (choice == 'y' or choice == 'Y'):
            try:
                os.system(f"rm -rf {path}")
                os.makedirs(path, exist_ok = True)
            except:
                config.logger.error(f"Failed to create directories at {path}")
                exit(1)
            download(path, k[0], j, k[1], k[2], config)
        else:
            print("WARNING: Please make sure the local extension is intact and secure.\n")
        choice = 'n'
        if os.path.isfile(os.path.join(path, ".PRIVILEGE")) and arg.root == None:
            choice = input("This extension requires root privilege to install, proceed with sudo? (y/N) ")
        try:
            if arg.root == True or (choice == 'y' or choice == 'Y'):
                install.install(path, config, True)
            else:
                install.install(path, config, False)
        except:
            exit(1)