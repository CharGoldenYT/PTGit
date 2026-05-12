import sys
import os
from typing import Any
from urllib.parse import urlparse as parse
from __configReader__ import readConfigFile, setConfig, checkOS
from subprocess import run
from pathlib import Path
from git import Repo

global packName
global URL
global branch
global build
global allowPrePackaged

packName = ""
URL = ""
branch = ""
build = False
allowPrePackaged = False

def processArg(arg:str, base:str = "") -> Any:
    if (arg.lower() == "help"):
        print("""PTGit (Pip Through Git)

Useage:

ptgit packagename packageURL <arguments> - Install a package from git.

Arguments:
--help:                             Displays this message
--branch="branchName"               Determines which branch to install from
--autoinstall="[<packagenames>]"    calls pip to install these packages if they are not included as a requirement in the package's repo
--config                            starts the configuration script""")
        exit(0)
        

    if (arg.lower().startswith("branch=")):
        return arg.split("=")[1]
        
    
    print(f"Not a valid argument {base}{arg}! Use --help for information!")

def checkArgs():
    arg_array = []
    for item in args:
        if (arg_array.__contains__(item) and ["--branch"].__contains__(item)):
            print(f"You cannot call {item} twice!")
            processArg("help")
        arg_array.append(item)

def runConfigScript():
    configFile = readConfigFile()
    validOptions = {"1": "AllowPackagedFiles"}
    result = input("From the following options choose one to switch\n1: Allow Potentially Unsafe Pre-Packaged files from git repositories: " + str(configFile["AllowPackagedFiles"]))

    if (result == "1"):
        setConfig("AllowPackagedFiles", (not configFile["AllowPackagedFiles"]))

    if (not validOptions.__contains__(result)):
        print("Invalid Option!")
        runConfigScript()

    print("Configuration saved! " + validOptions[result] + " set to " + configFile[validOptions[result]])
    exit(0)

args = sys.argv
if (args[0].endswith(".py") or args[0] == "ptgit"):
    args.remove(args[0])

if (args.__contains__("--config")):
    runConfigScript()

if (args.__len__() < 2):
    print("Invalid number of arguments!")
    processArg("help")

config = readConfigFile()
if (config["AllowPackagedFiles"]):
    i = input("WARNING: unsafe switch \"AllowPackagedFiles\" is enabled!\nThis may make it easy for malicious actors to install fake packages that comprimise your system!\nAlways check official sources before installng from a git repo!\nPress ENTER to continue, type IGNORE to permanently remove this warning.")
    if (i.upper() == "IGNORE"):
        setConfig("IgnoreWarning", True)

checkArgs()

result = parse(args[0])

if (all([result.scheme, result.netloc])):
    print("Invalid arguments!")
    processArg("help")
else:
    packName = args[0]

result = parse(args[1])

if (not all([result.scheme, result.netloc])):
    print("Invalid arguments!")
    processArg("help")
else:
    URL = args[1]

for item in args:
    if (item.startswith("--")):
        result = processArg(item.removeprefix("--"), "--")
        if (isinstance(result, str)):
            branch = result
        if (isinstance(result, bool)):
            build = True
        


br = ""
if (branch.__len__() > 0):
    br = f" at branch {branch}"

curOS = checkOS()

path = ""

if (curOS == "WINDOWS"):
    path += os.getenv("LOCALAPPDATA")
else:
    path += os.getenv("HOME")

def showProg(op_code, cur_count, max_count=None, message=''):
    finalStr = ""

    match op_code:
        case 0:
            finalStr += "[Beginning Clone]: "
        case 1:
            finalStr += "[Finished Cloning]: "
        case 2:
            finalStr += "[Counting Objects]: "
        case 3:
            finalStr += "[Compressing Objects]: "
        case 4:
            finalStr += "[Writing objects]: "
        case 5:
            finalStr += "[Recieving Objects]: "
        case 6:
            finalStr += "[Unimplemented Code]: "
        case 7:
            finalStr += "[Unimplemented Code]:"
        case 8:
            finalStr += "[Checking Out Branch]"
    
    finalStr += " | " + str(cur_count)
    if (max_count is not None):
        finalStr += " / " + str(max_count)
    else:
        finalStr += " / ?"

    if (message is not None and message.__len__() > 0):
        finalStr += "\n" + message

    if (curOS == "WINDOWS"):
        os.system("cls")
    else:
        os.system("clear")

    print(f"Getting package {packName} from {URL}{br}.")
    print(finalStr)



fullPath = path + "/Temp_ptgit/" + packName

if (Path(fullPath).exists()):
    import shutil
    shutil.rmtree(fullPath)

repo = Repo.clone_from(URL, fullPath, showProg)

zip_path = fullPath + "/" + packName + ".zip"

print(f'zip {zip_path} {os.curdir}')
os.chdir(fullPath)
if curOS == "WINDOWS":
    input("You MUST have 7zip installed for this command to work, press ENTER to continue")
    zip_process = run(["7z", "a", "-tzip", zip_path, ".\\"])

    while zip_process.returncode is None:
        from time import sleep
        if (curOS == "WINDOWS"):
            os.system("cls")
        else:
            os.system("clear")

        print(zip_path.stdout.read())

        sleep(0.01)

    print(zip_process.returncode)
else:
    zip_process = run(['zip', '-r', zip_path, "./"])

    while zip_process.returncode is None:
        from time import sleep
        if (curOS == "WINDOWS"):
            os.system("cls")
        else:
            os.system("clear")

        print(zip_path.stdout.read())

        sleep(0.01)

    print(zip_process.returncode)

process = run(['pip', 'install', Path(zip_path).resolve().__str__()])

while process.returncode is None:
    from time import sleep
    if (curOS == "WINDOWS"):
        os.system("cls")
    else:
        os.system("clear")

    print(process.stdout.read())

    sleep(0.01)


print("Cleaning up!")

import shutil
shutil.rmtree(path + "/Temp_ptgit/") # Remove any git dirs leftover.