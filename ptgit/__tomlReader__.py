import subprocess

def search_betweenDelimiters(string:str, start:str, end:str)->(None | str):
    start_index = string.find(start)
    if start_index == -1:
        return None

    end_index = string.find(end, start_index)
    if end_index == -1:
        return None

    return string[start_index:end_index]

def getDependencies(gitPath:str)->list[str]:
    tomlFile = open(gitPath + "/pyproject.toml", "r")
    string = tomlFile.read()
    tomlFile.close()
    dep_str = search_betweenDelimiters(string, "dependencies=", "[")
    dep_str = dep_str.removeprefix("[")

    dependencies = dep_str.splitlines()
    for dependency in dependencies:
        dependency = dependency.replace('"', "")
        requirements = [] # The package list of requirements.
        requirements.append(dependency)

    return requirements

def installDependecies(gitPath):
    for dependency in getDependencies(gitPath):
        process = subprocess.Popen("pip", ['install', dependency])

        if process.wait() == 0:
            print(process.stdout.read())