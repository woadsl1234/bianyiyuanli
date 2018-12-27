# -*- coding: UTF-8 -*-
def before(a, b):
    return len(a) < len(b) and a == b[0:len(a)]

def sortlength(L):
    # 按元素长度排序
    n = len(L)
    for i in range(n):
        k = i
        j = i + 1
        while j < n:
            if len(L[k]) > len(L[j]):
                k = j
            j = j + 1
        if i != k:
            L[k], L[i] = L[i], L[k]

class produce:
    def __init__(self,left,right):
        self.left = left
        self.right = right

    def is_zuodigui(self):
        for i in self.right:
            if self.left == i[0]:
                print self.left + '->' + '|'.join(self.right), '存在左递归'
                return 1
        return 0

    def zuogonggongyinzi(self):
        a = [i[0] for i in self.right]
        if len(list(set(a))) != len(a):
            print self.left + '->' + '|'.join(self.right), '存在左公因子'
            return 1
        else:
            return 0

class zuodigui:
    def __init__(self,path):
        f = open(path)
        self.zhong = f.readline().split()
        self.feizhong = f.readline().split()
        self.kaishi = f.readline().strip('\n')
        x = f.readlines()
        self.wenfa = []
        for i in x:
            j = i.strip().split('->')
            self.wenfa.append(produce(j[0],j[1].split('|')))
        f.close()

    def show(self):
        print "终结符号"
        print self.zhong
        print "非终结符号"
        print self.feizhong
        print "开始符号"
        print self.kaishi
        print "文法"
        for i in self.wenfa:
            print i.left,'->', '|'.join(i.right)

    def is_zuodigui(self):
        for p in self.wenfa :
            if p.is_zuodigui():
                return 1
        return 0
    
    def zuogonggongyinzi(self):
        for p in self.wenfa:
            if p.zuogonggongyinzi():
                return 1
        return 0

    def xiaochuzuodigui(self):
        a=[]
        for p in self.wenfa:
            if p.is_zuodigui():
                a.append(p)
        for p in a:
            f = 'A'
            while f in self.feizhong:
                f = chr(ord(f) + 1)
            self.feizhong.append(f)
            # print p,self.wenfa
            self.wenfa.remove(p)
            f1 = []
            f2 = []
            for i in p.right:
                if i[0] != p.left:
                    f1.append(i + f)
                else:
                    f2.append(i[1:] + f)
            f2.append('ß')
            if len(f1) == 0:
                exit(p.left+'->'+'|'.join(p.right)+' 无限循环')
            self.wenfa.append(produce(p.left, f1))
            self.wenfa.append(produce(f, f2))

    def tiqu(self):
        a = []
        for p in self.wenfa:
            if p.zuogonggongyinzi():
                a.append(p)

        for p in a:
            self.wenfa.remove(p)
            f = 'A'
            while f in self.feizhong:
                f = chr(ord(f) + 1)
            c = []
            d = []
            e = []
            for i in p.right:
                for j in range(1, len(i) + 1):
                    c.append([i[0:j]])
            for i in range(len(c)):
                for j in range(len(c[i])):
                    d.append(c[i][j])
            # print d
            for i in range(len(d)):
                for j in range(i + 1, len(d)):
                    if d[i] == d[j]:
                        e.append(d[i])
            # print e
            g = {}   
            for i in range(len(e)):
                g[e[i]] = [[],[]]
                for j in p.right:
                    if len(j) >= len(e[i]) and j[0:len(e[i])] == e[i]:
                        g[e[i]][0].append(j)
                    else:
                        g[e[i]][1].append(j)
            # exit(g)
            h=[]
            for i in e :
                for j in e:
                    if before(i,j) and len(g[i][0]) - len(g[j][0]) < 2:
                        h += list(set(i))
            for i in h:
                e.remove(i)
                del g[i]
            f2 = []
            sortlength(e)
            e.reverse()
            # print e
            for i in e:
                f1 = g[i][1]
                f1.insert(0, i + f)
                for j in range(len(g[i][0])):
                    f2.append(g[i][0][j][len(i):])
                for j in f2:
                    if j == '':
                        f2[f2.index(j)] = 'ß'
                self.feizhong += f
                self.wenfa.append(produce(p.left, f1))
                self.wenfa.append(produce(f, f2))

path = './3-2/1.txt'
zuodigui = zuodigui(path)

while zuodigui.is_zuodigui():
    zuodigui.xiaochuzuodigui()

while zuodigui.zuogonggongyinzi():
    zuodigui.tiqu()

zuodigui.show()