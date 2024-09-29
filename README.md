# Git Repository Topological Commit Order

## Overview
This project implements a Python script `topo_order_commits.py` that traverses a Git repository's commit history and outputs the commits in topologically sorted order. The commits are sorted from most recent to oldest, ensuring that children (descendant commits) are printed before their parents (ancestor commits). Project for UCLA CS 35L class.

The goal is to traverse the Git commit Directed Acyclic Graph (DAG) and generate a topologically ordered sequence of commits, providing visual indicators of relationships between commits when necessary.

## Features
- **Git Repository Detection**: The script searches upwards from the current directory to find the `.git` directory, ensuring it is run within a Git repository.
- **Branch Detection**: The script reads local branch names and their corresponding commit hashes from the `.git/refs/heads/` directory, supporting branch names with slashes.
- **Commit Graph Construction**: It constructs a commit graph where each commit node tracks its parents (ancestors) and children (descendants).
- **Topological Sorting**: The script generates a topological order of the commits, ensuring all descendants are printed before their ancestors.
- **Commit Output**: The output includes:
  - Commit hashes.
  - Branch names if the commit is a branch head.
  - Sticky start/ends to indicate transitions between commit segments when commits are not directly related.

## Example Usage
To run the script in a Git repository:
```bash
python3 topo_order_commits.py
```

### Example Output
For a simple repository with the following commits:

```text
  c0 -> c1 -> c2 (branch-1)
         \
          c3 -> c4 (branch-2, branch-5)
                 \
                  c5 (branch-3)
```

The output could look like this:
```bash
h5 branch-3
h4 branch-2 branch-5
h3
h1=

=
h2 branch-1
h1
h0
```

For a repository with a merge commit:
```text
  c0 -> c1 -> c2 -> c6 (branch-1)
	 \         /
	  c3 -> c4
```

The output could look like this:
```bash
h6 branch-1
h2
h1=

=h6
h4
h3
h1
h0
```

## Key Functions
### `topo_order_commits`
This is the main driver function that organizes the entire process.

### `getdir()`
- Traverses upwards from the current directory to locate the `.git` folder. 
- If not found, it outputs an error and exits.

### `getbranches(gitdir)`
- Reads the local branches from the `.git/refs/heads/` directory and retrieves the corresponding commit hashes.

### `makegraph(branches)`
- Constructs a graph representing the commit history using the `CommitNode` class.
- Each commit node stores its parent and child commits. The graph is built by traversing the commit history.

### `toposort(graph, roots)`
- Performs a topological sort on the commit graph using a depth-first search algorithm.
- Ensures that descendants (children) are printed before their ancestors (parents).

### `printfunc(graph, branches, sortedlist)`
- Prints the commits in the topologically sorted order.
- Adds sticky start/end indicators where necessary, and displays branch names if the commit corresponds to a branch head.

## Installation
To install and run the script:
1. Clone the repository.
2. Ensure Python 3 is installed.
3. Run the script from within a Git repository using:
   ```bash
   python3 topo_order_commits.py
   ```
