import os
import json
from typing import Any
configuration = {"AllowPackagedFiles": False, "IgnoreWarning": False}

def checkOS()->str:
    if (os.environ.get("HOME") is None):
        return "WINDOWS"

    return "UNIX"

def readConfigFile()->configuration:
    os = checkOS()
    path = ""
    if (os == "WINDOWS"):
        path += os.environ["APPDATA"]
    else:
        path += os.environ["HOME"]
    file = open(path + "/ptgit_config/config.ini", "r")
    if (file.read().__len__() < 1):
        file.close()
        writeConfigFile(configuration)
        file.open(path + "/ptgit_config/config.ini", "r")

    rawJson = file.read()

    return json.loads(rawJson)

def writeConfigFile(config:configuration):
    os = checkOS()
    path = ""
    if (os == "WINDOWS"):
        path += os.environ["APPDATA"]
    else:
        path += os.environ["HOME"]
    file = open(path + "/ptgit_config/config.ini", "w")
    file.write(json.dump(config))
    file.close()


def setConfig(name:str, newValue:Any):
    config = readConfigFile()
    value = config["name"]
    if (value is None):
        return

    config[name] = newValue
    writeConfigFile(config)