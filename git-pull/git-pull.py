#!/usr/bin/python2

# -*- coding: utf-8 -*-

'''
Created on Sep 28, 2018

@author: mdrotthoff
'''

import os
import sys
import subprocess

DEBUG = False
REPO_SHADE_CHILDREN = False
REPO_PULL_CHILDREN = True


def print_sorted_list(listvar, title=None):
    print('%s:' % str(title))
    for dir in sorted(listvar):
        print('    %s' % dir)


def print_stream(streamvar, title=None, level=0):
#    print('%s:' % str(title))
    title = title + ' ' * 9
#    for line in streamvar.decode('utf8').splitlines():
    for line in streamvar.splitlines():
#        sys.stderr.write("%s\n" % line)
        line = line.strip()
        sys.stdout.write('%s--%s  %s\n' % ('  ' * level, title[0:8], str(line)))

    
def exec_git_cmd(cmd):
#    print(cmd)
    # Ensure there are no embedded spaces in a string command
    if isinstance(cmd, str) and ' ' in cmd:
        print('Spaces embedded in the git command')
        exit(2)

    # Execute the command
    cmd_handle = subprocess.Popen(cmd,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
    (cmd_stdout, cmd_stderr) = cmd_handle.communicate()

#    if DEBUG:
#        print('Return code: %d' % cmd_handle.returncode)
#        print('Length stdout: %s' % str(len(cmd_stdout)))
#        print('Length stderr: %s' % str(len(cmd_stderr)))
#        if cmd_stderr:
#            for line in cmd_stderr.strip().decode("utf-8").splitlines():
#                sys.stderr.write("%s\n" % line)

    # Return the standard output and error streams
    return cmd_handle.returncode, cmd_stdout, cmd_stderr


def git_checkout_master(level = 0):
#    print('git_checkout')
    returncode, stdout, stderr = exec_git_cmd(['git',
                                               'checkout',
                                               'master'
                                               ])
#    if DEBUG: print('git_pull.returncode: %s' % str(returncode))
    if len(stdout) > 0: print_stream(stdout, 'checkout', level)
    if len(stderr) > 0: print_stream(stderr, 'checkout', level)


def git_fetch_all(level = 0):
#    print('git_fetch_all')
    returncode, stdout, stderr = exec_git_cmd(['git',
                                               'fetch',
                                               '--all',
                                               '--prune'
                                               ])
#    if DEBUG: print('git_fetch_all.returncode: %s' % str(returncode))
    if len(stdout) > 0: print_stream(stdout, 'fetch', level)
    if len(stderr) > 0: print_stream(stderr, 'fetch', level)


def git_pull(level = 0):
#    print('git_pull')
    returncode, stdout, stderr = exec_git_cmd(['git',
                                               'pull'
                                               ])
#    if DEBUG: print('git_pull.returncode: %s' % str(returncode))
    if len(stdout) > 0: print_stream(stdout, 'pull', level)
    if len(stderr) > 0: print_stream(stderr, 'pull', level)
    if returncode == 1:
        git_checkout_master(level=level)


def git_submodule_init(level=0):
#    print('git_submodule_init')
    returncode, stdout, stderr = exec_git_cmd(['git',
                                               'submodule',
                                               'update',
                                               '--init'
                                               ])
#    if DEBUG: print('git_submodule_init.returncode: %s' % str(returncode))
    submodule_list=''
    for line in stdout.decode('utf8').splitlines():
#        print('Submodule line %s' % line)
#        line = line.split(' ')[2]
#        submodule_list = submodule_list + str('Submodule %s initialized\n' % line.split(' '))
#        submodule_list = submodule_list + str('Submodule %s initialized\n' % str(line))
        submodule_list = submodule_list + str('Submodule %s initialized\n' % str(line.split(' ')[2]))

#    if len(stdout) > 0: print_stream(stdout, 'init', level)
    if len(stdout) > 0: print_stream(submodule_list, 'init', level)
    if len(stderr) > 0: print_stream(stderr, 'init', level)


def git_submodule_update(reponame, level = 0):
#    print('git_submodule_init')
    returncode, stdout, stderr = exec_git_cmd(['git',
                                               'submodule',
                                               'update',
                                               reponame
                                               ])
#    if DEBUG: print('git_submodule_update.returncode: %s' % str(returncode))
    if len(stdout) > 0: print_stream(stdout, 'subupdate', level)
    if len(stderr) > 0: print_stream(stderr, 'subupdate', level)


def git_submodule_list():
#    print('git_submodule_list')
#    if DEBUG: print('git_submodule_list directory: %s' % os.path.abspath(os.path.curdir))
    submodule_list = []
    returncode, stdout, etderr = exec_git_cmd(['git',
                                               'submodule'
                                               ])
    for line in stdout.decode('utf8').splitlines():
#        sys.stderr.write("%s\n" % line)
        line = line.strip()
        submodule_info = line[2:].split(' ')
#        if DEBUG: print('submodule_info: %s' % str(submodule_info))
        submodule_list.append(submodule_info[1])
#    if DEBUG: print('Submodule list: %s' % str(submodule_list))
#    if DEBUG: print('git_submodule_list.returncode: %s' % str(returncode))
    return sorted(set(submodule_list))


def process_repo(repodir, level):
    current_dir = os.path.abspath(os.path.curdir)
#    if DEBUG: print('Process initial directory: %s' % current_dir)
#    if DEBUG: print('process_repo: %s' % repodir)
    os.chdir(repodir)
    git_fetch_all(level=level)
    git_pull(level=level)
    
    if os.path.isfile('.gitmodules'):
 #       print('Repo has submodules')
        git_submodule_init(level=level)
        submodule_list = git_submodule_list()
        for submodule_name in submodule_list:
            print('%sSubmodule %s' % ('  ' * (level + 1), submodule_name))
            if REPO_PULL_CHILDREN:
                process_repo(submodule_name, level=(level + 1))
            else:
                # TODO: Deal with updated submodules of submodules
                git_submodule_update(submodule_name, level=(level + 1))

    os.chdir(current_dir)
#    if DEBUG: print('Process exit: %s' % os.path.abspath(os.path.curdir) )


def find_git_repos(sourcedir):
    dirlist = []

    print('Scanning directory %s' % sourcedir)
    for source in sourcedir:
        for root, dirs, files in os.walk(source):
            if '.git' in dirs:
                dirlist.append(os.path.abspath(root))
                if REPO_SHADE_CHILDREN:
                    dirs[:] = []
    dirlist = sorted(set(dirlist))
    if DEBUG: print_sorted_list(dirlist, 'Directories to process:')
    return dirlist


def main(argv):
    print('Entered main')
    if len(sys.argv) < 2:
        print('%s requires parameter of directory to process' % argv[0])
        exit(1)

# Find all unique git repositories in the specificed path(s)
    dirlist = find_git_repos(sourcedir = argv[1:])

# Process each of the found repositories
    for dir in dirlist:
        print('Processing repository %s' % dir)
        process_repo(repodir = dir, level = 0)


if __name__ == '__main__':
    print('Started git-pull')
    print('Initial working directory: %s' % os.path.abspath(os.path.curdir) )
    main(sys.argv)
    print('Final     working directory: %s' % os.path.abspath(os.path.curdir) )
