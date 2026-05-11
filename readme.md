# Python Packages through git repositories! | PTGit

PTGit (Pip through Git) is an alternative pip install method that allows you to install python packages directly through a git repository


## Adding better compatibility with this tool

If you would like the tool to be able to run smoother with YOUR project, simply include a built package with the following structure in your project

```
Root
|
|   packaged
|
|___    pgit.tar.gz
|
|___    pgit_details.whl (optional)
```

## Useage

`python -m ptgit packagename sourceURL`

Installs `packagename` from `sourceURL`