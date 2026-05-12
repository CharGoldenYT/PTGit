import os
import json
from typing import Any
from pathlib import Path
configuration = {"AllowPackagedFiles": False, "IgnoreWarning": False}

def checkOS()->str:
    if (os.getenv("HOME") is None):
        return "WINDOWS"

    return "UNIX"

def readConfigFile()->configuration:
    curOS = checkOS()
    path = ""
    if (curOS == "WINDOWS"):
        path += os.getenv("APPDATA")
    else:
        path += os.getenv("HOME")
    if (not Path(path + "/ptgit_config").exists()):
        os.mkdir(path + "/ptgit_config")
        writeConfigFile(configuration)
    if (not Path(path + '/ptgit_config/config.json').exists()):
        writeConfigFile(configuration)
    file = open(path + "/ptgit_config/config.json", "r")
    rawJson = file.read()
    print(f"RawJson: {rawJson}")

    return json.loads(rawJson)["config"]

def writeConfigFile(config:configuration):
    curOS = checkOS()
    path = ""
    if (curOS == "WINDOWS"):
        path += os.getenv("APPDATA")
    else:
        path += os.getenv("HOME")
    file = open(path + "/ptgit_config/config.json", "w")
    file.write(json.dumps({"config": config}, indent="\t"))
    file.close()


def setConfig(name:str, newValue:Any):
    config = readConfigFile()
    value = config["name"]
    if (value is None):
        return

    config[name] = newValue
    writeConfigFile(config)