# Processing logic for the git-pull utility:


Here is the git-pull logic for developing Python app:

1. Identify all core level git repositories
        (find <dir> -name '.git' -type d)
1. For each core repository
  1. Find the repository path
  1. Change to the repository path
  1. Fetch all updates to the repository
            (git fetch --all --prune)
  1. Update the current branch
            (git pull)
  1. If not on a current branch, type to checkout the master branch
            (git checkout master)
  1. Register any submodule that is not properly registered
            (git submodule update --init)
  1. For each submodule
		3. Find the submodule path
		3. Change to the submodule path
		3. Fetch all updates to the submodule
                (git fetch --all --prune)
		3. Update the current branch
                (git pull)
		3. If not on a current branch, type to checkout the master branch
                (git checkout master)
		3. If submodules exist, execute step 2.d recursively for the associated submodules
                (if [[ -f '.gitmodule' ]])
