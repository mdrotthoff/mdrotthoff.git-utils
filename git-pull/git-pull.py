'''
Created on Sep 28, 2018

@author: mdrotthoff
'''

'''
Here is the git-pull logic for developing Python app:
    Identify all core level git repositories
        (find <dir> -name '.git' -type d)
    For each core repository
        Find the repository path
        Change to the repository path
        Fetch all updates to the repository
            (git fetch --all --prune)
        Update the current branch
            (git pull)
        If not on a current branch, type to checkout the master branch
            (git checkout master)
        Register any submodule that is not properly registered
            (git submodule update --init)
        For each submodule
            Find the submodule path
            Change to the submodule path
            Fetch all updates to the submodule
                (git fetch --all --prune)
            Update the current branch
                (git pull)
            If not on a current branch, type to checkout the master branch
                (git checkout master)
            If submodules exist, execute step 2.d recursively for the associated submodules
                (if [[ -f '.gitmodule' ]])
'''

if __name__ == '__main__':
    pass
