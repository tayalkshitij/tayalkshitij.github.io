---
layout: default
---

# Github Commands


This commands tell the git version .

```bash
git -v
```

```
git config --global user.name "Your name"
git config --global user.email "email@domain.com"
```

we can check this configuration in ~/.gitconfig file.

```bash
git status
```

if accidentally did

```bash
git add .
git restore —staged <file-name>.  ##revoke staged file
git restore <file(s)> # retrieve state of file from HEAD commit and revert back to that version
```

view a chronological list of commits

```bash
git log
git log --stat # show file modification contained within each commit
git log --oneline # condensed version of the log output
git show <commit-has> #similar to log; focus on single commit
```

```bash
git commit --amend -m 'Updated commit message' # update commit message

#amend a commit
git add <file> # add file
git commit --amend --no-edit

# remove/undo latest commit
git reser HEAD~1 #HEAD minus 1

```

Branches 

```bash
git branch <branch-name> #create new branch
git switch  <branch-name> switch to this branch
git switch -c <branch-name> # create and switch, c stands for create
git branch # list all branches with checkout marked *
git branch -d <branch-name> # delete branch name

```

Merge 

```bash
git switch main
git merge widgets #merge widgets branch into main
git merge --abort # cancel the merge
git status
On branch main
All conflicts fixed but you are still merging.
  (use "git commit" to conclude merge)
...
git commit -m '<commit-message>'
```

Clone

```bash
git clone <repository-url>
git clone <repository-url> <directory> #rename
git clone --mirror <repository-url> #read only, not want to contrinute

```

Push 

```bash
git push <remote-repo-label> <branch>
# Example
git push origin main
# if no remote repo then git will pass origin. if no branch then currently checkout out branch.
git push <remote-repo-label> --force # throw away remote changes and replace wirh local changes
# Example
git push origin --force

```

Pull/Fetch 

```bash
git fetch <remote-repo-label> <branch> #download without merging 
# Example
git fetch origin main
# if no remote repo then git will pass origin. if no brancg then currently checkout branch.

# To merge 
git switch main
git merge origin/main

#rebase
git switch main
git rebase origin/main

#Pull encapsulate both fetch and merge/rebase
git pull <remote-repo-label> <branch> <merge-option>

# Example
git pull origin main --ff-only # git fetch origin main, git merge origin/main --ff-only

--ff-only (default) #fast-forward merge possible them only merge. will abort if diverge branch
--ff #merge even if fast-forward merge isn't possible
--rebase # swaps merge for rebase. Local change will be replayed on top of remote commits. 

#setting default
git config pull.ff only       # --ff-only
git config pull.rebase false  # --ff
git config pull.rebase true   # --rebase

```

Remote Repository 

```bash
# Create a new local branch
git checkout -b <branch>

# Upload a local branch to a remote repository
git push -u <repository-label> <branch>

#delete remote branch
git push -d <branch>
git push -d <branch>

git fetch # fetch all branch information from remote
git branch -a 

```

Rebase 

```bash
git rebase <source-branch> <topic-branch>
git rebase main topic # rebase topic branch commit onto the main branch
# if topic-branch is not mentioned then selected branch will be the 

#conflicts could potentially happen
git rebase --abort #abort the rebase
git add <filename> # after resolving merge, add the file
git status #verify
git rebase --continue # conflicts are resolved. 

#conflict during push
git push --force #push rebase branch that will overwrite refs that exist in the remote repository
```

Interactive/Advance Rebase 

```bash

git rebase -i HEAD~3 # interactive rebase to modify last 3 commit from HEAD pointer

#reword commit
**reword** 7f9d4bf Frontpag bug fiz
pick 3f8e810 Refactored navbar

# delete commit
pick 2f8e823 Refactored screenreader attributes
**drop** 7f9d4bf Updated README
pick 3f8e810 Accessibility fix

#squash commit
pick 7f9d4bf Accessibility fix for frontpage bug
**squash** 3f8e810 Updated screenreader attributes
**squash** ec48d74 Added comments & updated README
```

Utility Commands - Cherry Pick

```bash
# select commit for cherry-pick
git log <branch-name> --oneline

git switch <target-branch>

git cherry-pick <commit-hash>
git cherry-pick <commit-1-hash> <commit-2-hash> # multipe hash
git cherry-pick <commit-1-hash>~..<commit-2-hash> # range of hash

# merge conflict
git cherry-pick --continue

#abort just like rebase
git cherry-pick --abort
```

Utility Commands - Stash 

```bash
git stash # stash staged and unstaged changes; not untracked files 
git stash -u # stash untracked files as well

git stash -m 'Description of stashed changes' # add stash message as well
git stash -u -m 'Description of stashed changes'

git stash pop # apply stashed changes (most recent)

git stash list # list of existing changes 
// Output
stash@{0}: On main: hotfix in progress
stash@{1}: On auth: Started login widget
stash@{2}: On nav: WIP darkmode navbar

git stash pop --index 2 # apply third stash 

git stash drop <stash-index-num> # delete stash 

git stash clear # delete all stashes
```

Utility Commands - Tagging 

```bash
# tag command links tag to most recent commit
git tag <tag-name> #lightweight tag
git tag <tag-name> -a -m 'Tag description' # annotated tag

git tag <tag-name> <commit-hash> # tag commit further back in history

git tag # see list of tags
git show <tag-name> # show tag info

git push --tags # push tag; otherwise they will be in local 
git push <repo-label> <tag-name> # push a specific tag

git tag -d <tag-name> #delete taggit

```