from Core import Core, core_to_str
import sys


class Node:
    def __init__(self, type):
        self.type = type
        self.children = []

    def __str__(self):
        return str(self.type)

    def __add__(self, other):
        self.children.append(other)
        return self

    def __len__(self):
        return len(self.children)


class Parser:
    def __init__(self, tokenList=None):
        self.token_list = tokenList
        self.usedTokens = []
        self.scope = []
        self.functions = {}
        self.root = Node("root")
        self.nonTerminals = {
            "<decl>": self.decl,
            "<id-list>": self.id_list,
            "<stmt>": self.stmt,
            "<assign>": self.assign,
            "<in>": self.__in,
            "<out>": self.out,
            "<if>": self.__if,
            "<loop>": self.loop,
            "<cond>": self.cond,
            "<cmpr>": self.cmpr,
            "<expr>": self.expr,
            "<term>": self.term,
            "<factor>": self.factor,
            "<decl-func>": self.decl_func,
            "<func>": self.func,
            "func_signature": self.id_list_func_signature,
            "id_list_func_dec": self.id_list_func_dec,
        }

        # for printing  purposes
        self.tree_str = []
        self.spaces = 0
        self.program_str = []
        self.currentStr = ""

        if tokenList:
            self.parse()

    """
        Description: 
            creates parse tree for the core langauge out of the tokenList using the grammer below.
            grammer -> <prog> ::= program <decl-seq> begin <stmt-seq> end
        params:
            token_list -> [str] of tokens
    """

    def parse(self, token_list=None):
        # setup
        if token_list:
            self.token_list = token_list
        funcName = "parse"
        self.scope.append({})

        # helpers
        ft = self.frontToken
        r = self.root

        # program
        r + self.terminal(Core.PROGRAM, funcName)

        # <decl-seq>
        while ft(funcName) is not Core.BEGIN:
            if ft(funcName) is Core.INT:
                r + self.getNonTerminal("<decl>")
            else:
                r + self.getNonTerminal("<decl-func>")

        # begin
        r + self.terminal(Core.BEGIN, funcName)

        # <stmt-seq>
        while ft(funcName) not in [Core.END, Core.ENDIF, Core.ENDWHILE]:
            r + self.getNonTerminal("<stmt>")

        # end
        r + self.terminal(Core.END, funcName)
        return r

    # <prog> ::= program <decl-seq> begin <stmt-seq> end
    # <decl-seq> ::= <decl> | <decl><decl-seq> | <decl-func> | <decl-func><decl-seq>
    # <stmt-seq> ::= <stmt> | <stmt><stmt-seq>
    # <decl> ::= int <id-list> ;
    # <decl-func> ::= id ( <id-list> ) begin <stmt-seq> endfunc ;
    # <id-list> ::= id | id , <id-list>
    # <stmt> ::= <assign> | <if> | <loop> | <in> | <out> | <decl> | <func>
    # <func> ::= begin id ( <id-list> ) ;
    # <assign> ::= id = <expr> ;
    # <in> ::= input id ;
    # <out> ::= output <expr> ;
    # <if> ::= if <cond> then <stmt-seq> endif ;|
    #          if <cond> then <stmt-seq> else <stmt-seq> endif ;
    # <loop> ::= while <cond> begin <stmt-seq> endwhile ;
    # <cond> ::= <cmpr> | ! ( <cond> ) | <cmpr> or <cond>
    # <cmpr> ::= <expr> == <expr> | <expr> < <expr> | <expr> <= <expr>
    # <expr> ::= <term> | <term> + <expr> | <term> – <expr> <term> ::= <factor> | <factor> * <term>
    # <factor> ::= id | const | ( <expr> )

    def decl(self):
        pass

    def id_list(self):
        pass

    def id_list_func_dec(self):
        pass

    def id_list_func_signature(self):
        pass

    def stmt(self):
        pass

    def assign(self):
        pass

    def __in(self):
        pass

    def loop(self):
        pass

    def cond(self):
        pass

    def cmpr(self):
        pass

    def expr(self):
        pass

    def term(self):
        pass

    def factor(self):
        pass

    def decl_func(self):
        pass

    def func(self):
        pass

    def frontToken(self, func):
        pass

    def nextToken(self, func):
        pass

    def terminal(self, typ, func):
        pass

    def getNonTerminal(self, typ):
        pass

    def checkScope(self, var, check, checkVal=False, value=False):
        pass

    def checkLocalScope(self, var):
        pass

    def prettyPrintTree(self):
        pass

    def prettPrintProgram(self):
        pass

    def addTerminalStr(self, typ):
        pass
