---
layout: default
---

# Git Commands Reference Guide

A comprehensive guide to essential Git commands organized by workflow categories.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Operations](#basic-operations)
3. [Viewing History & Information](#viewing-history--information)
4. [Branch Management](#branch-management)
5. [Merging](#merging)
6. [Remote Operations](#remote-operations)
7. [Advanced Workflows](#advanced-workflows)
8. [Utility Commands](#utility-commands)

---

## Getting Started

### Check Git Version
```bash
git -v
```

### Initial Configuration
```bash
git config --global user.name "Your name"
git config --global user.email "email@domain.com"
```

You can check this configuration in the `~/.gitconfig` file.

---

## Basic Operations

### Check Repository Status
```bash
git status
```

### Adding and Restoring Files
```bash
git add .                              # Stage all changes
git restore --staged <file-name>       # Unstage a specific file
git restore <file(s)>                  # Retrieve state of file from HEAD commit and revert back to that version
```

### Committing Changes
```bash
git commit -m "Your commit message"    # Commit staged changes
git commit --amend -m "Updated commit message"  # Update commit message

# Amend a commit with additional changes
git add <file>                         # Add file
git commit --amend --no-edit           # Amend without changing message

# Remove/undo latest commit
git reset HEAD~1                       # HEAD minus 1
```

---

## Viewing History & Information
### Commit History
```bash
git log                               # View chronological list of commits
git log --stat                        # Show file modifications within each commit
git log --oneline                     # Condensed version of log output
git show <commit-hash>                # Similar to log; focus on single commit
```

---

## Branch Management

### Creating and Switching Branches
```bash
git branch <branch-name>              # Create new branch
git switch <branch-name>              # Switch to existing branch
git switch -c <branch-name>           # Create and switch (c stands for create)
git branch                            # List all branches with current marked *
git branch -d <branch-name>           # Delete branch
```

---

## Merging

### Basic Merge Operations
```bash
git switch main                       # Switch to target branch
git merge widgets                     # Merge widgets branch into main
git merge --abort                     # Cancel the merge
```

### Resolving Merge Conflicts
```bash
git status                            # Check merge status
# Output: "All conflicts fixed but you are still merging."
#         "(use 'git commit' to conclude merge)"
git commit -m "<commit-message>"      # Complete the merge
```

---

## Remote Operations

### Cloning Repositories
```bash
git clone <repository-url>                    # Clone repository
git clone <repository-url> <directory>        # Clone and rename directory
git clone --mirror <repository-url>           # Read-only clone (for mirroring, not contributing)
```

### Pushing Changes
```bash
git push <remote-repo-label> <branch>         # Push specific branch
# Example:
git push origin main
# Note: If no remote repo specified, git defaults to 'origin'
#       If no branch specified, uses currently checked out branch

git push <remote-repo-label> --force          # Force push (overwrites remote changes)
# Example:
git push origin --force
# Warning: This discards remote changes and replaces with local changes
```

### Fetching and Pulling Changes
```bash
# Fetch (download without merging)
git fetch <remote-repo-label> <branch>        # Download changes without merging
# Example:
git fetch origin main
# Note: If no remote repo specified, defaults to 'origin'
#       If no branch specified, uses currently checked out branch

# Manual merge after fetch
git switch main
git merge origin/main

# Rebase after fetch
git switch main
git rebase origin/main

# Pull (combines fetch and merge/rebase)
git pull <remote-repo-label> <branch> <merge-option>
# Example:
git pull origin main --ff-only    # Equivalent to: git fetch origin main, git merge origin/main --ff-only
```

### Pull Options
```bash
--ff-only      # (default) Fast-forward merge only; aborts if branches have diverged
--ff           # Merge even if fast-forward isn't possible
--rebase       # Use rebase instead of merge; replays local changes on top of remote commits
```

### Configure Default Pull Behavior
```bash
git config pull.ff only           # Set --ff-only as default
git config pull.rebase false      # Set --ff as default
git config pull.rebase true       # Set --rebase as default
```

### Working with Remote Branches
```bash
# Create and push new branch
git checkout -b <branch>                      # Create a new local branch
git push -u <repository-label> <branch>       # Upload local branch to remote repository

# Delete remote branch
git push <repository-label> -d <branch>       # Delete remote branch

# View all branches (local and remote)
git fetch                                     # Fetch all branch information from remote
git branch -a                                 # List all branches (local and remote)
```

---

## Advanced Workflows

### Rebasing
```bash
git rebase <source-branch> <topic-branch>     # Rebase topic branch onto source branch
git rebase main topic                         # Rebase topic branch commits onto main branch
# Note: If topic-branch is not mentioned, currently selected branch is used
```

### Handling Rebase Conflicts
```bash
# When conflicts occur during rebase:
git rebase --abort                           # Cancel the rebase
# OR resolve conflicts manually, then:
git add <filename>                           # Stage resolved files
git status                                   # Verify resolution
git rebase --continue                        # Continue rebase after resolving conflicts

# After rebase, force push may be needed:
git push --force                             # Push rebased branch (overwrites remote refs)
```

### Interactive Rebase
```bash
git rebase -i HEAD~3                          # Interactive rebase for last 3 commits from HEAD
```

#### Interactive Rebase Commands:
```bash
# Reword commit message
reword 7f9d4bf Frontpage bug fix
pick 3f8e810 Refactored navbar

# Delete commit
pick 2f8e823 Refactored screenreader attributes
drop 7f9d4bf Updated README
pick 3f8e810 Accessibility fix

# Squash commits (combine multiple commits)
pick 7f9d4bf Accessibility fix for frontpage bug
squash 3f8e810 Updated screenreader attributes
squash ec48d74 Added comments & updated README
```

---

## Utility Commands

### Cherry Pick
```bash
# Select commits for cherry-pick
git log <branch-name> --oneline               # View commit history

git switch <target-branch>                    # Switch to target branch

# Cherry-pick operations
git cherry-pick <commit-hash>                 # Pick single commit
git cherry-pick <commit-1-hash> <commit-2-hash>  # Pick multiple commits
git cherry-pick <commit-1-hash>~..<commit-2-hash>  # Pick range of commits

# Handle conflicts
git cherry-pick --continue                    # Continue after resolving conflicts
git cherry-pick --abort                       # Cancel cherry-pick operation
```

### Stash Operations
```bash
# Create stash
git stash                                     # Stash staged and unstaged changes (not untracked files)
git stash -u                                  # Stash including untracked files
git stash -m "Description of stashed changes" # Add descriptive message
git stash -u -m "Description of stashed changes"  # Untracked files + message

# Apply stash
git stash pop                                 # Apply most recent stash
git stash pop stash@{2}                       # Apply specific stash

# Manage stashes
git stash list                                # List all stashes
# Output example:
# stash@{0}: On main: hotfix in progress
# stash@{1}: On auth: Started login widget
# stash@{2}: On nav: WIP darkmode navbar

git stash drop <stash-index>                  # Delete specific stash
git stash clear                               # Delete all stashes
```

### Tagging
```bash
# Create tags (links tag to most recent commit)
git tag <tag-name>                            # Lightweight tag
git tag <tag-name> -a -m "Tag description"    # Annotated tag
git tag <tag-name> <commit-hash>              # Tag specific commit in history

# View tags
git tag                                       # List all tags
git show <tag-name>                           # Show tag information

# Push tags
git push --tags                               # Push all tags to remote
git push <repo-label> <tag-name>              # Push specific tag to remote

# Delete tags
git tag -d <tag-name>                         # Delete local tag
git push <repo-label> --delete <tag-name>     # Delete remote tag
```

---

## Quick Reference

### Common Workflows
```bash
# Start new feature
git switch -c feature-branch
# ... make changes ...
git add .
git commit -m "Add new feature"
git push -u origin feature-branch

# Update from main
git switch main
git pull origin main
git switch feature-branch
git rebase main

# Merge feature
git switch main
git merge feature-branch
git push origin main
git branch -d feature-branch
```