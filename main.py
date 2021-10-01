#! /usr/bin/python3

from Scanner import Scanner
from Parser import Parser
from Executor import Executor
from Core import Core
import sys

def main():
  # Initialize the scanner with the input file
  S = Scanner(sys.argv[1])
  S2 = Scanner(sys.argv[2])


  # Print the token stream
  while (S.currentToken() != Core.EOF): S.nextToken();
  while (S2.currentToken() != Core.EOF): S2.nextToken();

  P = Parser(S.tokenList)
  E = Executor(P.root, S2.tokenList)
  E.execute()

if __name__ == "__main__":
    main()