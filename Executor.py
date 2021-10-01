from Core import Core, core_to_str
from Node import Node
import sys
value_chain = None

class Executor:

    def __init__(self, root=None, data_list=None):
        self.scope = []
        if root:
            self.root = root
        else:
            self.root = Node('root')

        self.data_list = data_list
        self.functions = {}

        self.nonTerminals = {
         '<decl>' :  self.decl,
         '<id-list>':  self.id_list,
         '<stmt>':  self.stmt,
         '<assign>': self.assign,
         '<in>':  self.__in,
         '<out>':  self.out,
         '<if>':  self.__if,
         '<loop>':  self.loop,
         '<cond>':  self.cond,
         '<cmpr>':  self.cmpr,
         '<expr>':  self.expr,
         '<term>':  self.term,
         '<factor>':  self.factor,
         '<decl-func>': self.decl_func,
         '<func>': self.func,
         'func_signature': self.id_list_func_signature,
        }



    def execute(self, root=None):
        """

        :param root: will use the provided root instead of the one saved
        :return:
        """
        if root: self.root = root
        self.scope.append({})  #global scope

        # execute non-terminals
        for n in self.root.children:
            if n.type in self.nonTerminals:
                self.executeNonTerminal(n)

    def decl(self, node):
        '''

        :param node: a declaration node
        :return: none
        '''
        self.executeNonTerminal(node.children[1])
        return None

    def id_list(self, node):
        '''

        :param node: id list node
        :return: None
        '''
        for id in node.children:
            if id.type is not ',':
                self.checkLocalScope(id.type)
                self.scope[-1][id.type] = None
                pass

        return None

    def id_list_func_signature(self, node):
        """
        :param node: id list node
        :return: a map of ids -> integer values
        """
        vals = {}
        for id in node.children:
            if id.type is not ',':
                self.checkScope(id.type)
                vals[id.type] = self.getVar(id.type)
        return vals

    def stmt(self, node):
        '''

        :param node: statement node
        :return: none
        '''
        self.executeNonTerminal(node.children[0])
        return None

    def assign(self, node):
        '''

        :param node: assign node
        :return: none
        '''
        if not self.checkScope(node.children[0].type):
            print(f'ERROR EXECUTOR assign: variable with id {node.children[0].type} is not in scope {self.scope}')
            sys.exit()
        value = self.executeNonTerminal(node.children[2])  # expr node
        self.setIdValue(node.children[0].type, value)
        return None

    def __in(self, node):
        '''

        :param node: input node
        :return: none
        '''

        if not self.checkScope(node.children[1].type):
            print(f'ERROR EXECUTOR __in: variable with id {node.children[1].type} is not in scope {self.scope}')
            sys.exit()
        if len(self.data_list) == 0:
            print(f'ERROR EXECUTOR __in: no data to read in')
            sys.exit()

        value = self.data_list.pop(0)  # get and remove the first token from the data_list
        self.setIdValue(node.children[1].type, value)

        return None

    def out(self, node):
        '''

        :param node: output node
        :return: None
        '''

        print(str(self.executeNonTerminal(node.children[1])))
        return None


    def __if(self, node):
        '''
        :param node: an if node
        :return: None
        '''

        # find if an else token exists, and record its location
        else_location = None
        for i, c in enumerate(node.children):
            if c.type is 'else':
                else_location = i

        truth = self.executeNonTerminal(node.children[1])  # cond node
        if truth:
            self.scope.append({})  # if blocks have their own scope
            for i in range(3,len(node)):
                if node.children[i].type is 'endif' or node.children[i].type is 'else':
                    break
                self.executeNonTerminal(node.children[i])
            self.scope.pop()
        elif else_location:
            self.scope.append({})  # else blocks have their own scope
            for i in range(else_location+1, len(node)):
                if node.children[i].type is 'endif':
                    break
                self.executeNonTerminal(node.children[i])
            self.scope.pop()

        return None


    def loop(self, node):
        '''
        :param node: a loop node
        :return: None
        '''

        self.scope.append({})  # loops have their own scope
        while self.executeNonTerminal(node.children[1]): # cond node
            for i in range(3, len(node)):  # starting at 3 because 2 is a begin node
                if node.children[i].type in self.nonTerminals:
                    self.executeNonTerminal(node.children[i])
        self.scope.pop()
        return None

    def cond(self, node):
        '''

        :param node: a condition node
        :return: the truth of the condition
        '''
        value = None
        if len(node) == 1:  # cmpr
            value = self.executeNonTerminal(node.children[0])
        elif len(node) == 4:  # !(cond)
            value = not self.executeNonTerminal(node.children[2])
        elif len(node) == 3:  #  cmpr or cond
            value = self.executeNonTerminal(node.children[0]) or \
                    self.executeNonTerminal(node.children[2])

        return value

    def cmpr(self, node):
        '''

        :param node: a comparison node
        :return: the truth of the comparison
        '''
        truth = False
        value1 = self.executeNonTerminal(node.children[0])  # expr 1
        value2 = self.executeNonTerminal(node.children[-1])  # expr 2

        if node.children[1].type == '==':
            truth = value1 == value2
        elif node.children[1].type == '<':
            truth = value1 < value2
        elif node.children[1].type == '<=':
            truth = value1 <= value2

        return truth

    def expr(self, node):
        '''

        :param node: the node to evaluate
        :return: the value of the node
        '''

        value = self.executeNonTerminal(node.children[0])  # term node
        if len(node) == 3:
            value2 = self.executeNonTerminal(node.children[-1])  # expr node
            if node.children[1].type is '+':
                value += value2
            else:
                value -= value2

        return value

    def term(self, node):
        '''

        :param node: the nonde to evaluate
        :return: returns the value of node
        '''
        value = self.executeNonTerminal(node.children[0])  # factor
        if len(node) == 3:
            value *= self.executeNonTerminal(node.children[-1])  # term node

        return value

    def factor(self, node):
        '''
        checks for expr, if not then the first character of the type
        character results in an id
        number results in a constant

        :param node: a factor node
        :return: the value of the factor
        '''
        value = None
        if len(node) == 1:
            if type(node.children[0].type) is int:
                value = node.children[0].type
            elif node.children[0].type[0].isalpha():
                value = self.getVar(node.children[0].type)
        else:
            value = self.executeNonTerminal(node.children[1])

        return value

    def decl_func(self, node):
        """
            adds a function object to the map self.functions
            a function object consists of a
            name
            signature
            body
            self.functions maps names -> function object
        :param node:
        :return:
        """
        name = node.children[0]
        signature = node.children[2]
        body = list(filter(lambda x: x.type == '<stmt>', node.children))

        self.functions[name.type] = {'name': name, 'signature':signature, 'body':body}

    def func(self, node):
        """

        :param node:
        :return:
        """
        name = node.children[1]
        function = self.functions[name.type]

        ids = [id.type for id in node.children[3].children if id.type is not ',']
        ids_vals = [self.getVar(id.type) for id in node.children[3].children if id.type is not ',']
        signature = [id.type for id in function['signature'].children if id.type is not ',']
        scope = {formal: actual for formal, actual in zip(signature, ids_vals)}

        # need to replace the scope of the program with global and the new function scope
        old_scope = self.scope
        self.scope = [self.scope[0], scope]
        for stmt in function['body']: self.executeNonTerminal(stmt)

        # execute the function
        for stmt in function['body']:
            self.executeNonTerminal(stmt)

        # swap scopes
        # print(self.scope)

        function_scope = self.scope
        self.scope = old_scope
        self.scope[0] = function_scope[0]  # replace the global scope in case of change

        # print(self.scope)
        # print(function_scope)
        #copy values back
        for formal, actual in zip(signature, ids):
            self.setIdValue(actual, function_scope[-1][formal])


    def executeNonTerminal(self, node):
        """
        executes the function corresponding to the type of node
        :param node: a non-erminal node
        :return:
        """
        return self.nonTerminals[node.type](node)


    def getVar(self, id):
        '''
        checks the scopes from inner to outer for id.
        Throws an error if id is not found
        :param id: id of the variable
        :return: the value of the id
        '''

        for scope in reversed(self.scope):
            if id in scope:
                if scope[id] == None:
                    print(f'ERROR EXECUTOR getVar: variable with id {id} is not in scope {self.scope}')
                    sys.exit()
                else:
                    return scope[id]

    def checkScope(self, id):
        """
        :param id: the id to check for
        :return: True if found, else false
        """
        for scope in reversed(self.scope):
            if id in scope:
                return True
        return False

    def checkLocalScope(self,id):
        """

        :param id: the id to check the local scope for
        :return: True is found, else false
        """
        if id in self.scope[-1]:
            return True
        return False

    def setIdValue(self,id,value):
        
        if value > 1023:
            print(f'ERROR EXECUTOR setIdValue: variable with id {id} is being set to a value of {value} which is > than 1023')
            sys.exit()

        for scope in reversed(self.scope):
            if id in scope:
                scope[id] = value
                break


