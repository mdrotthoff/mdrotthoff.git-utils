# Processing logic for the git-pull utility:


Here is the git-pull logic for developing Python app:

1. Identify all core level git repositories  
		(find <dir> -name '.git' -type d)
      1. Get the absolute path of the directory
      1. Ensure the path is unique in the list
1. For each core repository
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
      1. Find the submodule path
      1. Change to the submodule path
      1. Fetch all updates to the submodule  
			(git fetch --all --prune)
      1. Update the current branch  
 			(git pull)
      1. If not on a current branch, type to checkout the master branch  
			(git checkout master)
      1. If submodules exist, execute step 2 recursively for each associated submodules
			(if [[ -f '.gitmodule' ]])
