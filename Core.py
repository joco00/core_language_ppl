from enum import Enum

Core = Enum('Core',
	'PROGRAM,\
	BEGIN,\
	END,\
	NEW,\
	INT,\
	ENDFUNC,\
	DEFINE,\
	EXTENDS,\
	CLASS,\
	ENDCLASS,\
	IF,\
	THEN,\
	ELSE,\
	WHILE,\
	ENDWHILE,\
	ENDIF,\
	SEMICOLON,\
	LPAREN,\
	RPAREN,\
	COMMA,\
	ASSIGN,\
	NEGATION,\
	OR,\
	EQUAL,\
	LESS\
	LESSEQUAL,\
	ADD,\
	SUB,\
	MULT,\
	INPUT,\
	OUTPUT,\
	CONST,\
	ID,\
  EOF'
)

def core_to_str(elem):
	if elem is Core.PROGRAM: return 'program'
	elif elem is Core.BEGIN: return 'begin'
	elif elem is Core.END: return 'end'
	elif elem is Core.NEW: return 'new'
	elif elem is Core.INT: return 'int'
	elif elem is Core.ENDFUNC: return 'endfunc'
	elif elem is Core.DEFINE: return 'define'
	elif elem is Core.EXTENDS: return 'extends'
	elif elem is Core.CLASS: return 'class'
	elif elem is Core.ENDCLASS: return 'endclass'
	elif elem is Core.IF: return 'if'
	elif elem is Core.THEN: return 'then'
	elif elem is Core.ELSE: return 'else'
	elif elem is Core.WHILE: return 'while'
	elif elem is Core.ENDWHILE: return 'endwhile'
	elif elem is Core.ENDIF: return 'endif'
	elif elem is Core.SEMICOLON: return ';'
	elif elem is Core.LPAREN: return '('
	elif elem is Core.RPAREN: return ')'
	elif elem is Core.COMMA: return ','
	elif elem is Core.ASSIGN: return '='
	elif elem is Core.NEGATION: return '!'
	elif elem is Core.OR: return 'or'
	elif elem is Core.EQUAL: return '=='
	elif elem is Core.LESS: return '<'
	elif elem is Core.LESSEQUAL: return '<='
	elif elem is Core.ADD: return '+'
	elif elem is Core.SUB: return '-'
	elif elem is Core.MULT: return '*'
	elif elem is Core.INPUT: return 'input'
	elif elem is Core.OUTPUT: return 'output'
	
