# -*- coding: UTF-8 -*-

from zuodigui import *

flat = lambda L: sum(map(flat, L), []) if isinstance(L, list) else [L]

class ll_1:
    def __init__(self,zhong,feizhong,start_character,produce):
        self.zhong = zhong          
        self.feizhong = feizhong   
        self.start_character = start_character          # 开始符
        self.produce = produce                          # 产生式

    def f(self, a):
        if a not in self.feizhong:
            print a, '不在文法的非终结符中'
            return
        # print [i.right for i in self.produce if a == i.left][0]
        return [i.right for i in self.produce if a == i.left][0]

    def first(self, a):
        # 求a的FIRST集
        if a not in self.feizhong and a not in self.zhong:
            print a, '不在文法的终结或非终结符中'
            return
        if a == 'ß':
            return set(list(['ß']))
        elif a in self.zhong:
            return set(a)
        fir = set([i[0] for i in self.f(a) if i[0] in self.zhong])
        # print "zhong",fir
        fir_n = set([i[0] for i in self.f(a) if i[0] in self.feizhong])
        # print "feizhong",fir_n
        if 'ß' in self.f(a):
            fir.add('ß')
        elif len([1 for i in fir_n if 'ß' in self.first(i)]) == len(fir_n) > 0 and len(fir) == 0:
            fir.add('ß')
        for i in fir_n:
            fir = fir | (self.first(i) - set(list(['ß'])))
        return set(fir)

    def follow(self, a):
        # 求a的FOLLOW集
        if a not in self.feizhong:
            print a, '不在文法非终结符中'
            return
        fol = set()
        s = flat([p.right for p in self.produce])
        # print s
        if a == self.start_character or len([1 for i in s if i[-1] == a]) > 0:
            fol.add('#')
        back1 = [i[j + 1:] for i in s for j in range(len(i) - 1) if i[j] == a]
        # print back1
        for i in back1:
            for j in range(len(i)):
                fol = fol | (self.first(i[j]) - set(list(['ß'])))
                if 'ß' not in self.first(i[j]):
                    break
        le = [p.left for p in self.produce for i in p.right if i[-1] == a and p.left != a]
        # print le
        for i in le:
            fol = fol | self.follow(i)
        # print fol
        return fol

    def check_ll1(self):
        for p in self.produce:
            if 'ß' in p.right:
                if len([1 for i in p.right if i != 'ß' and len(self.first(i[0]) & self.follow(p.left)) != 0]) > 0:
                    return 0
            else:
                if len([1 for i in range(len(p.right)) for j in range(i + 1, len(p.right))
                        if len(self.first(p.right[i]) & self.first(p.right[j])) > 0]) > 0:
                    return 0
        return 1

    def analysis(self):
        # 求文法的LL(1)分析表
        terminator = [i for i in self.zhong]
        if 'ß' in terminator:
            terminator.remove('ß')
        terminator.append('#')
        table = [[''] * len(terminator) for _ in range(len(self.feizhong))]
        for p in self.produce:
            for i in p.right:
                if i != 'ß':
                    for j in self.first(i[0]):
                        table[self.feizhong.index(p.left)][terminator.index(j)] = p.left + '->' + i
                else:
                    for j in self.follow(p.left):
                        table[self.feizhong.index(p.left)][terminator.index(j)] = p.left + '->' + 'ß'
        self.table = table

    def showtable(self):
        # 打印文法的LL(1)分析表
        terminator = [i for i in self.zhong]
        if 'ß' in terminator:
            terminator.remove('ß')
        terminator.append('#')
        print '-' * len(terminator) * 5 + 'LL(1)分析表' + '-' * len(terminator) * 5
        print ' ' * 10,
        for i in terminator:
            print '%-10s' % i,
        print
        for i in range(len(self.table)):
            print '%-10s' % self.feizhong[i],
            for j in self.table[i]:
                print '%-10s' % j,
            print
        print '-' * (len(terminator) + 1) * 10


path = '3-3/1.txt'
zuodigui = zuodigui(path)

while zuodigui.is_zuodigui():
    zuodigui.xiaochuzuodigui()

while zuodigui.zuogonggongyinzi():
    zuodigui.tiqu()
zuodigui.show()
ll = ll_1(zuodigui.zhong,zuodigui.feizhong,zuodigui.kaishi,zuodigui.wenfa)
for i in ll.feizhong:
    print 'FIRST(%s) =' % i, ll.first(i)
for i in ll.feizhong:
    print 'FOLLOW(%s) =' % i, ll.follow(i)

if ll.check_ll1():
    ll.analysis()
    ll.showtable()
else:
    print '该文法不是LL(1)文法'