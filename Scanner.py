from Core import Core

class Scanner:
  # Constructor should open the file and find the first token
  def __init__(self, filename):

    self.f = open(filename, 'r')
    self.symbolMap = {"==": Core.EQUAL,
                      "<=":  Core.LESSEQUAL,
                      '=': Core.ASSIGN,
                      '<': Core.LESS,
                      '(': Core.LPAREN,
                      ')': Core.RPAREN,
                      ';': Core.SEMICOLON,
                      ',': Core.COMMA,
                      '!': Core.NEGATION,
                      '+': Core.ADD,
                      '*': Core.MULT,
                      '-': Core.SUB}
    self.termMap = {"" : Core.EOF,
                    "program" :  Core.PROGRAM,
                    "begin" :  Core.BEGIN,
                    "end" :  Core.END,
                    "new" :  Core.NEW,
                    "int" :  Core.INT,
                    "define" :  Core.DEFINE,
                    "endfunc" :  Core.ENDFUNC,
                    "class" :  Core.CLASS,
                    "extends" :  Core.EXTENDS, 
                    "endclass" : Core.ENDCLASS,
                    "if" :  Core.IF,
                    "then" : Core.THEN,
                    "else" :  Core.ELSE,
                    "while" :  Core.WHILE,
                    "endwhile" : Core.ENDWHILE,
                    "endif" :  Core.ENDIF,
                    "or" :  Core.OR,
                    "input" : Core.INPUT,
                    "output" : Core.OUTPUT}
    self.MAXCONST = 1023


    self.tokenList = []
    self.token = ""
    self.nextChar = next(self.gnc())

    self.EOF = False

    self.nextToken()

    
  # nextToken should advance the scanner to the next token
  def nextToken(self):

    self.token = "" #clear old token

    #check for end of file
    if self.nextChar is None: return Core.EOF 
    
    #remove white space
    while self.nextChar is ' ':
      self.nextChar = next(self.gnc())
      if self.nextChar is None: return Core.EOF

    #find a symbol
    if self.nextChar in self.symbolMap:
      if self.nextChar in '=<': #tokens with potential 2nd = as a symbol
        if self.move() is None: return Core.EOF
        if self.nextChar is '=': 
          if self.move() is None: return Core.EOF
      else: 
        if self.move() is None: return Core.EOF
    # find a digit
    elif self.nextChar.isdigit():
      while self.nextChar.isdigit():
        if self.move() is None: break
      if int(self.token) > self.MAXCONST:  
        print ("ERROR: Constant: " +self.token+ " exceeds the maximum")
        return Core.EOF
    #find a string of alphanumeric characters
    else:
      while self.nextChar.isalnum():
        if self.move() is None: break #return Core.EOF

    token = self.currentToken()
    if token is Core.ID: self.tokenList.append(self.getID())
    elif token is Core.CONST: self.tokenList.append(self.getCONST())
    else: self.tokenList.append(token)
    
    if self.EOF: return Core.EOF
    return 0

  # currentToken should return the current token
  def currentToken(self):
  
    if self.token in self.termMap: return self.termMap[self.token]
    elif self.token in self.symbolMap: return self.symbolMap[self.token]
    elif self.token.isdigit(): return Core.CONST
    else: return Core.ID
      
    

  # If the current token is ID, return the string value of the identifier
	# Otherwise, return value does not matter
  def getID(self):
    return self.token

  # If the current token is CONST, return the numerical value of the constant
	# Otherwise, return value does not matter
  def getCONST(self):
    return int(self.token)




  #custom functions  

  '''     
  get next character
    a generator function that will 
    1- return the character if its valid
    2- return None if EOF
    3- obmit new line and tab
    4- throw an error

  '''
  def gnc(self):  
    char = self.f.read(1)
    if char and (char in self.symbolMap or char.isalnum() or char is ' '): yield char
    elif char is '': 
      #print("\nEND OF FILE REACHED\n")
      yield None
    elif char in ['\n','\t','\'','\\','\r','\b','\f']  : 
      #char = next(self.gnc())
      yield ' '
    else: 
      print("ERROR: (fuction gnc) invalid Character " + char + ".")
      yield None


  '''
    This function will add nextchar to the current tokenand then advance
    the file reader one character while setting nextchar to to the char just read in.
    Named move because you are "moving" forward one character
  '''
  def move(self):
    self.token += self.nextChar
    self.nextChar = next(self.gnc())

    if self.nextChar is None: 
      self.EOF = True
      return None
    else: return 0 