# Python Packages through git repositories! | PTGit

PTGit (Pip through Git) is an alternative pip install method that allows you to install python packages directly through a git repository

> [!NOTE]
> WARNING: make sure you trust a repo before installing python packages, it could be malicious!


## Useage

`python -m ptgit packagename packageURL <arguments> - Install a package from git.`

Arguments:

`--help`:                              Displays the help message

`--branch="branchName"`:               Determines which branch to install from (Currently does not do anythng)

`--autoinstall="[<packagenames>]"`:    calls pip to install these packages if they are not included as a requirement in the package's repo (Currently does not do anythng)

`--config`:                            starts the configuration script