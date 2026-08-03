import os
import json
from typing import Any
from pathlib import Path
configuration = {"AllowPackagedFiles": False, "IgnoreWarning": False, "ZipLocation": "_default_"}

class ConfigurationFile:
    AllowPackagedFiles:bool = False
    IgnoreWarning:bool = False
    ZipLocation:str = "_default_"

    def __init__(self, config : configuration):
        for item in configuration.keys():
            self.setConfig(item, config[item])

    def setConfig(self, name:str, value:Any):
        if vars(self).__contains__(name):
            setattr(self, name, value)

    def getConfig(self, name:str)->Any:
        if vars(self).__contains__(name):
            return getattr(self, name, None)

    def exists(self, name:str)->bool:
        return self.getConfig(name) != None

    def toDict(self)->configuration:
        config = configuration.copy()
        for item in configuration.keys():
            if vars(self).__contains__(item):
                config[item] = vars(self)[item]

        return config

default_config = ConfigurationFile(configuration) # Initialize empty config for reference

def checkOS()->str:
    if (os.getenv("HOME") is None):
        return "WINDOWS"

    return "UNIX"

def readConfigFile()->ConfigurationFile:
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

    config = json.loads(rawJson)["config"]
    return ConfigurationFile(config)

def writeConfigFile(config:ConfigurationFile):
    curOS = checkOS()
    path = ""
    if (curOS == "WINDOWS"):
        path += os.getenv("APPDATA")
    else:
        path += os.getenv("HOME")
    file = open(path + "/ptgit_config/config.json", "w")
    file.write(json.dumps({"config": config.toDict()}, indent="\t"))
    file.close()


def setConfig(name:str, newValue:Any):
    config = readConfigFile()
    if not config.exists(name): return

    config.setConfig(name, newValue)
    writeConfigFile(config)