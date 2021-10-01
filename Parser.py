from Core import Core, core_to_str
from Node import Node
import sys


class Parser:
    def __init__(self, tokenList=None):
        self.token_list = tokenList
        self.usedTokens = []
        self.scope = []
        self.functions = {}
        self.root = Node("root")

        self.tree_str = []
        self.spaces = 0
        self.program_str = []
        self.currentStr = ""

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

        if tokenList:
            self.parse()

    """
        Description: creates parse tree from the tokenList
        grammer -> <prog> ::= program <decl-seq> begin <stmt-seq> end
    """

    def parse(self, token_list=None):
        if token_list:
            self.token_list = token_list
        funcName = "parse"
        self.scope.append({})

        # program
        self.root + self.terminal(Core.PROGRAM, funcName)

        # <decl-seq>
        while self.frontToken(funcName) is not Core.BEGIN:
            if self.frontToken(funcName) is Core.INT:
                self.root + self.getNonTerminal("<decl>")
            else:
                self.root + self.getNonTerminal("<decl-func>")

        # begin
        self.root + self.terminal(Core.BEGIN, funcName)

        # <stmt-seq>
        while self.frontToken(funcName) not in [
            Core.END,
            Core.ENDIF,
            Core.ENDWHILE,
            # Core.ELSE,
        ]:
            self.root + self.getNonTerminal("<stmt>")

        # end
        self.root + self.terminal(Core.END, funcName)
        return self.root

    def decl(self):
        funcName = "decl"
        self.spaces += 1
        n = (
            Node("<decl>")
            + self.terminal(Core.INT, funcName)
            + self.getNonTerminal("<id-list>")
            + self.terminal(Core.SEMICOLON, funcName)
        )

        self.spaces -= 1
        return n

    def id_list(self):
        funcName = "id_list"
        n = Node("<id-list>")
        var = self.terminal(str, funcName)
        self.checkLocalScope(var.type)
        self.scope[-1][var.type] = False
        n + var

        while self.frontToken(funcName) is not Core.SEMICOLON:
            n + self.terminal(Core.COMMA, funcName)

            var = self.terminal(str, funcName)
            self.checkLocalScope(var.type)
            self.scope[-1][var.type] = False
            n + var
        return n

    def id_list_func_dec(self):
        funcName = "id_list_func_dec"
        n = Node("<id-list>")
        var = self.terminal(str, funcName)
        self.checkLocalScope(var.type)
        self.scope[-1][var.type] = True
        n + var

        while self.frontToken(funcName) is not Core.RPAREN:
            n + self.terminal(Core.COMMA, funcName)

            var = self.terminal(str, funcName)
            self.checkLocalScope(var.type)
            self.scope[-1][var.type] = True
            n + var
        return n

    def id_list_func_signature(self):
        funcName = "id_list_func_signature"
        n = Node("<id-list>")
        var = self.terminal(str, funcName)
        self.checkScope(var.type, True, True, True)
        n + var

        while self.frontToken(funcName) is not Core.RPAREN:
            n + self.terminal(Core.COMMA, funcName)

            var = self.terminal(str, funcName)
            self.checkScope(var.type, True, True, True)
            n + var
        return n

    def stmt(self):
        n = Node("<stmt>")
        funcName = "stmt"
        self.spaces += 1

        if type(self.token_list[0]) is str:
            n + self.getNonTerminal("<assign>")
        elif self.token_list[0] is Core.IF:
            n + self.getNonTerminal("<if>")
        elif self.token_list[0] is Core.WHILE:
            n + self.getNonTerminal("<loop>")
        elif self.token_list[0] is Core.INPUT:
            n + self.getNonTerminal("<in>")
        elif self.token_list[0] is Core.OUTPUT:
            n + self.getNonTerminal("<out>")
        elif self.token_list[0] is Core.INT:
            n + self.getNonTerminal("<decl>")
        elif self.token_list[0] is Core.BEGIN:
            n + self.getNonTerminal("<func>")
        else:
            self.terminal(
                [str, Core.IF, Core.WHILE, Core.INPUT, Core.OUTPUT, Core.INT], funcName
            )

        self.spaces -= 1
        return n

    def assign(self):
        funcName = "assign"
        n = (
            Node("<assign>")
            + self.terminal(str, funcName)
            + self.terminal(Core.ASSIGN, funcName)
            + self.getNonTerminal("<expr>")
            + self.terminal(Core.SEMICOLON, funcName)
        )
        self.checkScope(n.children[0].type, True, value=True)
        return n

    def __in(self):
        funcName = "__in"
        n = (
            Node("<in>")
            + self.terminal(Core.INPUT, funcName)
            + self.terminal(str, funcName)
            + self.terminal(Core.SEMICOLON, "__in")
        )
        self.checkScope(n.children[1].type, True, value=True)
        return n

    def out(self):
        funcName = "out"
        return (
            Node("<out>")
            + self.terminal(Core.OUTPUT, funcName)
            + self.getNonTerminal("<expr>")
            + self.terminal(Core.SEMICOLON, funcName)
        )

    def __if(self):
        funcName = "__if"
        self.scope.append({})
        n = (
            Node("<if>")
            + self.terminal(Core.IF, funcName)
            + self.getNonTerminal("<cond>")
            + self.terminal(Core.THEN, funcName)
        )
        while self.frontToken(funcName) not in [
            Core.END,
            Core.ENDIF,
            Core.ENDWHILE,
            Core.ELSE,
        ]:
            n + self.getNonTerminal("<stmt>")

        if self.token_list[0] is Core.ELSE:
            self.scope.pop()
            self.scope.append({})
            n + self.terminal(Core.ELSE, funcName)
            while self.frontToken(funcName) not in [
                Core.END,
                Core.ENDIF,
                Core.ENDWHILE,
                Core.ELSE,
            ]:
                n + self.getNonTerminal("<stmt>")

        self.scope.pop()
        (
            n
            + self.terminal(Core.ENDIF, funcName)
            + self.terminal(Core.SEMICOLON, funcName)
        )

        return n

    def loop(self):
        funcName = "loop"
        self.scope.append({})
        n = (
            Node("<loop>")
            + self.terminal(Core.WHILE, funcName)
            + self.getNonTerminal("<cond>")
            + self.terminal(Core.BEGIN, funcName)
        )
        while self.frontToken(funcName) not in [
            Core.END,
            Core.ENDIF,
            Core.ENDWHILE,
            Core.ELSE,
        ]:
            n + self.getNonTerminal("<stmt>")
        (
            n
            + self.terminal(Core.ENDWHILE, funcName)
            + self.terminal(Core.SEMICOLON, funcName)
        )
        self.scope.pop()
        return n

    def cond(self):
        funcName = "cond"
        n = Node("<cond>")
        if self.token_list[0] is Core.NEGATION:
            (
                n
                + self.terminal(Core.NEGATION, funcName)
                + self.terminal(Core.LPAREN, funcName)
                + self.getNonTerminal("<cond>")
                + self.terminal(Core.RPAREN, funcName)
            )
        else:
            n + self.getNonTerminal("<cmpr>")

            if self.token_list[0] is Core.OR:
                n + self.terminal(Core.OR, funcName) + self.getNonTerminal("<cond>")
        return n

    def cmpr(self):
        funcName = "cmpr"
        n = Node("<cmpr>")
        n + self.getNonTerminal("<expr>")
        if self.token_list[0] is Core.EQUAL:
            n + self.terminal(Core.EQUAL, funcName)
        elif self.token_list[0] is Core.LESS:
            n + self.terminal(Core.LESS, funcName)
        elif self.token_list[0] is Core.LESSEQUAL:
            n + self.terminal(Core.LESSEQUAL, funcName)
        else:
            self.terminal([Core.EQUAL, Core.LESS, Core.LESSEQUAL], funcName)
        n + self.getNonTerminal("<expr>")
        return n

    def expr(self):
        funcName = "expr"
        n = Node("<expr>")
        n + self.getNonTerminal("<term>")
        if self.token_list[0] is Core.ADD:
            n + self.terminal(Core.ADD, funcName) + self.getNonTerminal("<expr>")
        elif self.token_list[0] is Core.SUB:
            n + self.terminal(Core.SUB, funcName) + self.getNonTerminal("<expr>")
        return n

    def term(self):
        funcName = "term"
        n = Node("<term>")
        n + self.getNonTerminal("<factor>")
        if self.token_list[0] is Core.MULT:
            n + self.terminal(Core.MULT, funcName) + self.getNonTerminal("<term>")
        return n

    def factor(self):
        n = Node("<factor>")
        funcName = "factor"
        if type(self.token_list[0]) == str:
            var = self.terminal(str, funcName)
            self.checkScope(var.type, True, True)
            n + var
        elif type(self.token_list[0]) is int:
            n + self.terminal(int, funcName)
        elif self.token_list[0] is Core.LPAREN:
            (
                n
                + self.terminal(Core.LPAREN, funcName)
                + self.getNonTerminal("<expr>")
                + self.terminal(Core.RPAREN, funcName)
            )
        else:
            self.terminal([str, int, Core.LPAREN], funcName)
        return n

    def decl_func(self):
        n = Node("<decl-func>")
        funcName = "decl-func"
        self.spaces += 1
        self.scope.append({})

        name = self.terminal(str, funcName)
        if name.type in self.functions:
            print(f"parameter {name.type} already is scope {self.scope}")
            sys.exit()
        self.functions[name.type] = None

        n + name + self.terminal(Core.LPAREN, funcName)
        signature = self.getNonTerminal("id_list_func_dec")
        self.functions[name.type] = signature
        (
            n
            + signature
            + self.terminal(Core.RPAREN, funcName)
            + self.terminal(Core.BEGIN, funcName)
        )

        if self.frontToken(funcName) is Core.ENDFUNC:
            print(f"No function body for function {name.type}")
            sys.exit()

        while self.frontToken(funcName) is not Core.ENDFUNC:
            n + self.getNonTerminal("<stmt>")
        (
            n
            + self.terminal(Core.ENDFUNC, funcName)
            + self.terminal(Core.SEMICOLON, funcName)
        )

        self.scope.pop()
        self.spaces -= 1
        return n

    def func(self):
        n = Node("<func>")
        funcName = "func"
        n + self.terminal(Core.BEGIN, funcName)
        name = self.terminal(str, funcName)
        n + name + self.terminal(Core.LPAREN, funcName)
        signature = self.getNonTerminal("func_signature")
        if name.type not in self.functions:
            print(f"no function name match for {name.type}")
            sys.exit()

        if name.type not in self.functions or len(signature) != len(
            self.functions[name.type]
        ):
            print(f"no function signature match for use of function {name.type}")
            sys.exit()

        (
            n
            + signature
            + self.terminal(Core.RPAREN, funcName)
            + self.terminal(Core.SEMICOLON, funcName)
        )

        return n

    def frontToken(self, func):
        if len(self.token_list) == 0:
            print(f"ERROR {func}: Tried to access a Token from an Empty Token List")
            sys.exit()
        return self.token_list[0]

    """ obtains the next token from the token_list
         error if the token list is empty
        returns the next token
    """

    def nextToken(self, func):
        self.frontToken(func)
        token = self.token_list.pop(0)
        self.usedTokens.append(token)
        return token

    """
        obtains the next terminal node as well as adds the terminal to both
        the tree str and the program str
        Returns: the terminal node
    """

    def terminal(self, typ, func):
        token = self.nextToken(func)
        if not (token is typ or type(token) is typ):
            print(f"ERROR in function {func}: \n{typ} token not found")
            print(f"{self.usedTokens[-1]} was found instead\n")
            print(f"The tokens used so far:\n {self.usedTokens} \n")
            print(f"The tokens left:\n {self.token_list} ")

            sys.exit()
        if type(token) is Core:
            token = core_to_str(token)
        terminal = Node(token)
        self.tree_str.append("| " * self.spaces + str(terminal))

        self.addTerminalStr(str(terminal))
        return terminal
        # return nodes.append(Node(str(token)))

    """
        obtains the next non-terminal node as well as adds the nonterminal 
         to the tree str
        Returns: the terminal node
    """

    def getNonTerminal(self, typ):
        self.spaces += 1
        spot = len(self.tree_str)
        node = self.nonTerminals[typ]()
        self.spaces -= 1

        self.tree_str.insert(spot, "| " * self.spaces + str(node))
        return node

    """
        checks if var is in scope. Throws an error based on check. 
        checkVal and value are to see if a var has a value before its used
            Note: checkVal is NOT perfect. if the value is asigned in  
                in an if statement ChecksVal cannot not figure out 
                if that var was actually assigned or not
    """

    def checkScope(self, var, check, checkVal=False, value=False):
        found = False
        val = False
        for block in self.scope:
            if var in block:
                found = True
                val = block[var]
                if value == True:
                    block[var] = True

        if found != check:
            print(f"ERROR: {var} in scope is {found}\n should be {check}")
            print(self.scope)
            sys.exit()

        if checkVal and val == False:
            print(f"ERROR: {var} does not have a value but was used in an expression\n")
            sys.exit()

    def checkLocalScope(self, var):
        if var in self.scope[-1]:
            print(f"ERROR: {var} is already declared in local scope.")
            print(self.scope)
            sys.exit()

    """
        prints out the tree str
    """

    def prettyPrintTree(self):
        for line in self.tree_str:
            print(line)

    """
        prints out the tree str
    """

    def prettPrintProgram(self):
        for line in self.program_str:
            (print(line))

    """
        properly formats a terminal in the program str
    """

    def addTerminalStr(self, typ):

        if typ == "program":
            self.program_str.append("program")
        elif typ in ["begin", "then"]:
            self.currentStr += " " + typ
            self.program_str.append("  " * (len(self.scope) - 1) + self.currentStr)
            self.currentStr = ""
        elif typ == "else":
            # self.program_str.append('  ' * len(self.scope) + self.currentStr)
            self.program_str.append("  " * (len(self.scope) - 1) + "else")
            self.currentStr = ""
        elif typ == "end":
            self.program_str.append("  " * len(self.scope) + self.currentStr)
            self.program_str.append("end")
        elif typ == "or":
            self.currentStr += f" {typ} "
        elif typ == ";":
            self.currentStr += typ
            self.program_str.append("  " * len(self.scope) + self.currentStr)
            self.currentStr = ""
        elif typ in ["if", "int", "output", "input"]:
            self.currentStr += typ + " "
        else:
            self.currentStr += typ
