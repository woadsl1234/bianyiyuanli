# -*- coding: utf-8 -*-

class Edge:
    def __init__(self,ID,i,next_ID):
        self.ID = ID
        self.input = i
        self.next_ID = next_ID

class NFA:
   
    def __init__(self):
        self.graph = []
        self.total = 0
   
    def read(self,path):
        f = open(path,'r')
        mapping_function=[]
        for line in f.readlines():
                func = line.strip().split(' ')
                
                mapping_function.append(Edge(int(func[0]), func[1], int(func[2])))
        self.graph = mapping_function
        # print(self.graph)
    def printNFA(self):
        for g in self.graph:
            p = "%d %s %d" % (g.ID,g.input,g.next_ID)
            print(p) 
        print("")
char = ['a','b']

class Subset:
    sub_ID = 0
    def __init__(self,nodes):
        self.nodes = nodes
        self.already = 0
        self.id = Subset.sub_ID
        Subset.sub_ID += 1

class DFA:   
    def __init__(self, nfa):
        self.nfa = nfa.graph
        self.total = 0
        self.subsets = []
        self.graph = []
        self.accept = []
        self.no = []
    
    def eclosure(self,nodes): 
        if nodes == []:
            return -1
        nodes.sort()
        # print(nodes)
        for node in nodes:    
            for n in self.nfa:
                if n.ID == node and n.input == 'ß' and n.next_ID not in nodes:
                    nodes.append(n.next_ID)
        nodes.sort()
        f = 0 
        for n in self.subsets: 
            if nodes == n.nodes:
                f = 1
                return n
        if f == 0:
            sub = Subset(nodes) 
            self.subsets.append(sub)
            if 1 in nodes:
                self.accept.append(sub.id)
            else:
                self.no.append(sub.id)
            return sub              
   
    def move(self,nodes,i):
        aims = []
        for node in nodes: 
            for n in self.nfa:
                if n.ID == node and n.input == i:
                    aims.append(n.next_ID)
        return list(set(aims)) # 去重
        
    def determinate(self):
        self.subsets.append(self.eclosure([0]))
        for i in self.subsets:
            if i.already == 1:
                continue
            i.already = 1
            for c in char:
                if not self.eclosure(self.move(i.nodes,c)) == -1:
                    self.graph.append(Edge(i.id,c,self.eclosure(self.move(i.nodes,c)).id))
                else:
                    continue
        
    def printDFA(self):
        for g in self.graph:
            p = "%d %s %d" % (g.ID,g.input,g.next_ID)
            print(p)
            
        
    
if __name__ == "__main__":
    nfa = NFA()
    nfa.read('2-3/4.txt')
    nfa.printNFA()
    dfa = DFA(nfa)
    dfa.determinate()
    dfa.printDFA()
