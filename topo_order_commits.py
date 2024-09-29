# Keep the function signature,
# but replace its body with your implementation.
#
# Note that this is the driver function.
# Please write a well-structured implemention by creating other functions outside of this one,
# each of which has a designated purpose.
#
# As a good programming practice,
# please do not use any script-level variables that are modifiable.
# This is because those variables live on forever once the script is imported,
# and the changes to them will persist across different invocations of the imported functions.
def topo_order_commits():
    import os, sys, zlib

    class CommitNode:
        #Each commit is instance of class commitnode
        def __init__(self, commit_hash, parens=set(), childs=set()):
            """
            :type commit_hash: str
            """
            self.commit_hash = commit_hash
            self.parents = list(parens)
            self.children = list(childs)
            
        def __repr__(self): 
            #Allows printing for debugging purposes
            return "Commit node: " + str(self.commit_hash) + " Parents: " + str(self.parents) + " Children: " + str(self.children)

    def getdir():
        #Searches upwards for the .git folder
        curpath = os.getcwd()
        gitdir = None

        while curpath != "/":
            if os.path.exists(curpath+"/.git"):
                return curpath+"/.git"
            else:
                curpath = os.path.abspath(os.path.join(curpath, os.pardir))

        if gitdir == None:   
            print('Not inside a Git repository',file=sys.stderr)
            exit(1)

    def getbranches(gitdir):
        #Get local branch names and corresponding hashes
        branches = {}
        for br in os.listdir(gitdir+"/refs/heads"):
            if br == "dev": #Is directory error fix
                for br in os.listdir(gitdir+"/refs/heads/dev"):
                    with open(gitdir+"/refs/heads/dev/"+br) as file: branches["dev/"+br]=file.read().strip()
            else:
                with open(gitdir+"/refs/heads/"+br) as file: branches[br]=file.read().strip()
        return branches


    def makegraph(branches):
        
        #MAY NEED TO ADD SEEN INTO ELSE, AND IF INTO GRAPH PARENTS AND CURRENT
        
        
        def getparents(hash):
            #Finds object from its hash, strips and decompresses it, returns string
            if os.path.isfile(dir+"/objects/"+hash[:2]+"/"+hash[2:]):
                obj = str(zlib.decompress(open(dir+"/objects/"+hash[:2]+"/"+hash[2:], 'rb').read()))
                obj_lines = obj.split("\\n")
                return [x.split(" ")[-1] for x in obj_lines if "parent" in x]
            else:
                return []


        graph = dict()
        roots = list()

        while branches:
            current = branches.pop()
            
            #Make new commit node for branch
            if current not in graph.keys():
                current_node = CommitNode(current)
                graph[current] = current_node

            #Iterates for every parent of node
            for parent in getparents(current):
                if parent not in graph.keys():
                    parent_node = CommitNode(parent)
                    graph[parent] = parent_node
                    branches.append(parent)
                else:
                    branches.append(parent)

                #Add info to nodes
                if current in graph[parent].children: #Fixed root parent duplication glitch
                    continue
                else:
                    graph[parent].children.append(current)
                graph[current].parents.append(parent)

        for nodes in list(graph.values()):
            if len(nodes.parents)==0:
                roots.append(nodes.commit_hash)

        return graph, roots

    def toposort(graph, roots):
        #Topologically sort the given graph
        sorted_list = []
        process = list(roots)

        while process:
            item = process.pop()
            sorted_list.append(item)

            child = graph[item].children
            graph[item].children = []
            for c in child:
                graph[c].parents.remove(item)
                if not graph[c].parents:
                    process.append(c)
        
        
        sorted_list.reverse()
        return sorted_list

    def printfunc(graph, branches, sortedlist):
        #Prints from topological order
        sticky = False
        for current in sortedlist:
            branchnames = [name for name, hash in branches.items() if current == hash]
            branchnames.sort()
            head = " ".join(branchnames)
            children=""
            parents =""

            
            if sticky:
                if graph[current].children:
                    children = " ".join(graph[current].children)
                print("=" + children+ "\n"+current+ " "+ head)
                sticky = False
            else:
                print(current + " " + head)

            if current != sortedlist[-1] and sortedlist[sortedlist.index(current) + 1] not in graph[current].parents:

                if  graph[current].parents:
                    parents=" ".join(graph[current].parents)
                print(parents+"="+ "\n")
                sticky = True



    #MAIN
    dir = getdir()
    branches = getbranches(dir)
    graph, root_commits = makegraph(list(branches.values()))
    sorted = toposort(graph,root_commits)
    graph, root_commits = makegraph(list(branches.values()))
    printfunc(graph,branches,sorted)

if __name__ == '__main__':
    topo_order_commits()
