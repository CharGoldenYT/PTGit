# Python Packages through git repositories! | PTGit

PTGit (Pip through Git) is an alternative pip install method that allows you to install python packages directly through a git repository

> [!NOTE]
> WARNING: make sure you trust a repo before installing python packages, it could be malicious!


## Useage

`python -m ptgit packagename packageURL <arguments> - Install a package from git.`

Arguments:

`--help`:                              Displays the help message

`--branch="branchName"`:               Determines which branch to install from (Currently does not do anythng)

`--config`:                            starts the configuration script

Configuration:

`ZipLocation` :                        Where your install of 7-zip is, specifying this may fix any problems where it cannot find 7zip