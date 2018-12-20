import re
import string
word = string.lowercase
word_id = string.letters+'_'

x = str(raw_input())

class Analysis:
    def __init__(self,string):
        self.keyword = {'case': 'kw_case', 'do': 'kw_do', 'return': 'kw_return', 'for': 'kw_for', 'int': 'kw_int', 'void': 'kw_void', 'while': 'kw_while', 'else': 'kw_else', 'char': 'kw_char', 'default': 'kw_default', 'switch': 'kw_switch', 'continue': 'kw_continue', 'break': 'kw_break', 'if': 'kw_if'}
        self.changliang = {'num':r'\d+','ch':r'\'.*?\'','str':r'".*?"'}
        self.regex = r'\d+|\'.*?\'|\".*?\"'
        self.string = string
        self.res = []
        self.yunsuan = {'!': 'not', '<=': 'le', '%': 'mod', '>=': 'ge', '++': 'inc', '!=': 'nequ', '+': 'add', '*': 'mul', '-': 'sub', '/': 'div', '<': 'lt', '--': 'dec', '&&': 'and', '==': 'equ', '=': 'assign', '||': 'or', '>': 'gt', '&': '', '|': ''}
        self.fenjie = {')': 'rparen', '(': 'lparen', ',': 'comma', ';': 'simcon', ':': 'colon', '}': 'rbrac', '{': 'lbrac'}
        self.all = dict(self.keyword.items()+self.yunsuan.items()+self.fenjie.items())

    def select_keyword(self):
        for i,j in enumerate(self.string):
            if j not in word:
                self.add_res_string(i)
                break 
    
    def analyse_yuju(self):
        while self.string != '' :
            self.string = self.string.strip(' ')
            if self.string[0] in word_id :
                for i,j in enumerate(self.string):
                    if j in self.all:
                        self.add_res_string(i)
                        break
            else :
                for i,j in enumerate(self.string):
                    if j in self.all:
                        self.add_res_string(i+1)
                        break
    
    def add_res_string(self,i):
        keyword = self.string[:i].strip()
        x = re.search(self.regex, keyword)
        if x:
            key = x.span()[1]
            for i in self.changliang:
                flag = re.search(self.changliang[i],self.string[:key])
                if flag:
                    self.res.append({self.string[:key]:i})
            self.string = self.string[key:]
        else:
            if keyword in self.all:
                if keyword == '+' or keyword == '-' or keyword == '=' or keyword == '&' or keyword == '|':
                    if self.string[i:i+1] == keyword:
                        self.res.append({keyword+keyword:self.all[keyword+keyword]})
                        self.string = self.string[i+1:]
                    else:
                        self.res.append({keyword:self.all[keyword]})
                        self.string = self.string[i:]
                elif keyword == '!' or keyword == '<' or keyword == '>':
                    if self.string[i:i+1] == '=':
                        self.res.append({keyword+keyword:self.all[keyword+keyword]})
                        self.string = self.string[i+1:]
                    else:
                        self.res.append({keyword:self.all[keyword]})
                        self.string = self.string[i:]
                else:        
                    self.res.append({keyword:self.all[keyword]})
                    self.string = self.string[i:]
            else:
                self.res.append({keyword:'id'})
                self.string = self.string[i:]

    def Analysis(self):
        self.select_keyword()
        self.analyse_yuju()
        return self.res

cifa = Analysis(x)
print(cifa.Analysis())

