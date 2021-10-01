Name: Jake OConnor
Files: No additional files from project 3

    Executor.py:
        Added new functionality for executing functions
        3 new methods were added as well as included in self.nonTerminals that maps names -> functions
        func: executes a <func> node 
        decl_func: executes a <decl-func> node
        id_list_func_signature: executues a <id-list> node but for the purpose of retreiving the values of the ids and checking that the ids are in scope
         

    Parser.py:
        Added functionality for functions. To do this I added 
        4 new methods to the parser class
        func : function to parse a function node. Will check that function signature is meet
        decl_func: function to parse a function declartion
        func_signature: function to parse an id-list for a function signature returns a <id-list> node
        id_list_func_dec: function to parse an id-list for a function signature declaration returns a <id-list> node
        these four methods were added to self.nonTerminals map that maps names -> functions
        				
        				
    
    Scanner.py:
        no changes from last week
    Core.py:
        no changes from last week


Special Features and comments: None


Description of the call stack:
	the call stack is implemented by
		1- obtaining the ids being used for the function call
		2- obtain the ids values
		3- obtaining the formal parameters
		4- creating a new function scope that sets the formal parameters equal to the 
			ids values.
		5- creating a new scope that is {{global},{function_scope}}
		6- save old scope 
		7- swap the executors scope with the new scope
		8- execute the function
		9- swap back the scopes
		10- copy over the values from the function scope to the main scope.
		
		
		So on a function call, the scope will always be {global, function}
		if a function calls another function, the old function scope gets swapped
		out with the new scope. 
