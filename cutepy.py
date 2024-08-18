import sys

## TOKENS ## 
# Digits
digit_tok = "Digit"
# Characters 
variable_tok = "Variable"
# String
string_tok = "String"
# Expression Tokens
plus_tok = "Plus"
minus_tok = "Minus"
mult_tok = "Multiply"
div_tok = "Divide"
mod_tok = "Modulo"
# Comparing Tokens
less_than_tok = "Less Than"
more_than_tok = "More Than"
less_or_equals_tok = "Less Or Equals Than"
more_or_equals_tok = "More Or Equals Than"
equals_tok = "Equals"
not_equals_tok = "Not Equals"
# Assignment Token
assignment_tok = "Assign"
#Separator Tokens
comma_tok = "Comma"
dot_tok = "Dot"
colon_tok = "Colon"
# Grouping Tokens
open_block_tok = "Open Block"
close_block_tok = "Close Block"
l_par_tok = "LPar"
r_par_tok ="RPar"
# Comment Token
comment_tok = "Comment"
def_tok = "Function Name"
## KEYWORDS ##
keywords = [
    'main', 'def', '#def', '#int', 'global',
    'if', 'elif', 'else', 'while', 'print',
    'return', 'input', 'int', 'and', 'or', 'not'
]
keyword_tok = "Keyword"
## POSITION ## 
position = [0, 0]
## TOKENS ##
input_prog = []
tokens = []

class Token:
    def __init__(self, token_type, token_value=None, token_line=None):
        self.token_type = token_type
        self.token_value = token_value
        self.token_line = token_line

    def __repr__(self):
        return f"[Type: {self.token_type}, Value: \"{self.token_value}\", Line: {self.token_line}]" if self.token_value else f"[Type: {self.token_type}, Line: {self.token_line}]"
    def get_token_type(self):
        return self.token_type

    def get_token_value(self):
        return self.token_value
    
    def get_token_line(self):
        return self.token_line
class Error:
    def __init__(self, error_type, error_pos, value):
        self.error_type = error_type
        self.error_pos = error_pos
        self.value = value

    def __repr__(self):
        return f"Error on position {self.error_pos}: {self.error_type} <{self.value}>"

class Lexical:
    def __init__(self, filename):
        self.filename = filename
        self.position = position
        self.tokens = tokens 
        self.line_number = 1  # Initialize the line number
        self.input_prog = self.load_file()
        
    def load_file(self):
        characters = []
        with open(self.filename) as f:
            while True:
                c = f.read(1)
                if not c:
                    break
                characters.append(c)
        return characters
        
    def next_char(self): 
        if self.input_prog:
            self.position[1] += 1
            return self.input_prog.pop(0)
        else:
            return None
    
    def peek_next(self):
        if self.position[0] >= len(self.input_prog):
            return 'eof'
        else:
            return self.input_prog[self.position[0]]

    def lex(self):
        while self.position[0] < len(self.input_prog):
            current_char = self.next_char()

            if current_char == '\n':
                self.line_number += 1
                self.position[1] = 0  # Reset column position at new line

            if current_char == '/':
                next_char = self.peek_next()
                if next_char == '/':
                    self.tokens.append(Token(token_type=div_tok, token_value=current_char+next_char, token_line=self.line_number))
                '''else:
                    while self.peek_next() not in ' \n':
                        self.next_char()'''
            elif current_char.isspace():
                pass
            elif current_char.isalpha(): 
                identifier = current_char
                while self.peek_next().isalnum():
                    identifier += self.next_char()
                if identifier in keywords:
                    self.tokens.append(Token(token_type=keyword_tok, token_value=identifier, token_line=self.line_number))
                elif self.peek_next() == '(':
                    self.tokens.append(Token(token_type=def_tok, token_value=identifier, token_line=self.line_number))
                else:
                    self.tokens.append(Token(token_type=variable_tok, token_value=identifier, token_line=self.line_number))
            elif current_char == '#':
                identifier = current_char
                while self.peek_next().isalnum():
                    identifier += self.next_char()
                if identifier in keywords:
                    self.tokens.append(Token(token_type=keyword_tok, token_value=identifier, token_line=self.line_number))
                elif self.peek_next() == "#":
                    self.next_char()
                    self.tokens.append(Token(token_type=comment_tok, token_value="##", token_line=self.line_number))
                    while self.peek_next() != "#" and self.peek_next() != '\n':
                        self.next_char()
                elif self.peek_next() == "{":
                    identifier += self.next_char()
                    self.tokens.append(Token(token_type=open_block_tok, token_value=identifier, token_line=self.line_number))
                elif self.peek_next() == "}":
                    identifier += self.next_char()
                    self.tokens.append(Token(token_type=close_block_tok, token_value=identifier, token_line=self.line_number))
            elif current_char.isdigit():
                number = current_char
                while self.peek_next().isdigit():
                    number += self.next_char()
                self.tokens.append(Token(token_type=digit_tok, token_value=number, token_line=self.line_number))
            else:
                if current_char == "+":
                    self.tokens.append(Token(token_type=plus_tok, token_value=current_char, token_line=self.line_number))
                elif current_char == "-":
                    self.tokens.append(Token(token_type=minus_tok, token_value=current_char, token_line=self.line_number))
                elif current_char == "*":
                    self.tokens.append(Token(token_type=mult_tok, token_value=current_char, token_line=self.line_number))
                elif current_char == "%":
                    self.tokens.append(Token(token_type=mod_tok, token_value=current_char, token_line=self.line_number))
                elif current_char == ">":
                    next_char = self.peek_next()
                    if(next_char == '='):
                        self.tokens.append(Token(token_type=more_or_equals_tok, token_value=current_char+next_char, token_line=self.line_number))
                        current_char = self.next_char()
                    else:
                        self.tokens.append(Token(token_type=more_than_tok, token_value=current_char, token_line=self.line_number))
                elif current_char == "<":
                    next_char = self.peek_next()
                    if(next_char == '='):
                        self.tokens.append(Token(token_type=less_or_equals_tok, token_value=current_char+next_char, token_line=self.line_number))
                        current_char = self.next_char()
                    else:
                        self.tokens.append(Token(token_type=less_than_tok, token_value=current_char, token_line=self.line_number))
                elif current_char == "=":
                    next_char = self.peek_next()
                    if(next_char == '='):
                        self.tokens.append(Token(token_type=equals_tok, token_value=current_char+next_char, token_line=self.line_number))
                        current_char = self.next_char()
                    else:
                        self.tokens.append(Token(token_type=assignment_tok, token_value=current_char, token_line=self.line_number))
                elif current_char == "!":
                    next_char = self.peek_next()
                    if(next_char == '='):
                        self.tokens.append(Token(token_type=not_equals_tok, token_value=current_char+next_char, token_line=self.line_number))
                        current_char = self.next_char()
                    else:
                        error = Error(error_type="Unknown Character expected '=' after '!' ", error_pos=self.position, value=current_char)
                        print(error.__repr__())
                elif current_char == ",":
                    self.tokens.append(Token(token_type=comma_tok, token_value=current_char, token_line=self.line_number))
                elif current_char == "(":
                    self.tokens.append(Token(token_type=l_par_tok, token_value=current_char, token_line=self.line_number))
                elif current_char == ")":
                    self.tokens.append(Token(token_type=r_par_tok, token_value=current_char, token_line=self.line_number))
                elif current_char == ":":
                    self.tokens.append(Token(token_type=colon_tok, token_value=current_char, token_line=self.line_number))
                else:
                    error = Error(error_type="Unknown Character", error_pos=self.position, value=current_char)
                    print(error.__repr__())

        self.print_tokens()

    def print_tokens(self):
        for token in self.tokens:
            print(token)
        print('########################################################################################################')
        print("LEXICAL ANALYSIS COMPLETED")
        print('########################################################################################################')
        
########################################################################################################
# Syntax Analyzer
########################################################################################################
class Syntax:


    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[self.position]

        # De thelw comments sto suntaktiko
        self.tokens = [token for token in self.tokens if token.get_token_type() != comment_tok]
        

        # Quad Variables
        self.quad_counter = 0
        self.quad_list = []
        self.temp_variables = []
        self.T_i = 1
        

    def nextQuad(self):
        #H tampela tou kathe quad prwta ginetai +1 kai meta epistrefetai giati h prwth einai 1
        self.quad_counter += 1
        return self.quad_counter
    
    def genQuad(self, op, x, y, z):
        quad = [self.nextQuad(), op, x, y, z]
        self.quad_list.append(quad)
        
        return quad
    
    def newTemp(self):
        # ta temp variables pou mpainoun sth teleutaia thesh tou quad
        # T_i = 1,2,3...
        self.temp = f"T_{self.T_i}"   
        
        self.temp_variables.append(self.temp)
        self.T_i += 1
        return self.temp
    
    def emptyList(self):
        return []
    
    def makeList(self, x):
        return [x]
    
    def merge(self, list1, list2):
        return list1 + list2
        
    def backpatch(self, counters_list, z):
        '''Vazei to value tou z se ola ta quads me 
        counter idio me tous counters ths counters_list
        kai kaino sth thesh 4 -> vhma - pou kanei jump'''
        for i in counters_list:
            self.quad_list[i-1][4] = z
        '''dedomenou oti kathe quad exei unique counter
        pou ksekina apo 1 tote h thesh kathe quad sth lista 
        einai counter - 1 opou counter = i edw'''
    
    def print_all_quads(self):
            # gia elegxo
            for i in range(len(self.quad_list)):
                print(f"Quad {self.quad_list[i][0]}: {self.quad_list[i][1]}, {self.quad_list[i][2]}, {self.quad_list[i][3]}, {self.quad_list[i][4]}")
            #print(self.quad_list)

    def next_token(self):
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
            print(self.current_token)
        else:
            self.current_token = None
            print('SYNTAX SUCCESSFULLY PARSED')
            self.print_all_quads()
            exit()
    
    def startRule(self):
        self.declarations()
        self.functions()
        self.call_main_part()
        
    
    def functions(self):
        while self.current_token.get_token_value()  == 'def':
            self.function()

    def function(self):
        if self.current_token.get_token_value() == 'def':
            self.next_token()
            if self.current_token.get_token_type() == def_tok:
                self.next_token()
                if self.current_token.get_token_type() == l_par_tok:
                    self.next_token()
                    self.id_list()
                    if self.current_token.get_token_type() == r_par_tok:
                        self.next_token()
                        if self.current_token.get_token_type() == colon_tok:
                            self.next_token()
                            if self.current_token.get_token_type() == open_block_tok:
                                self.next_token()
                                self.declarations()
                                self.functions()
                                self.glob_decl()
                                self.code_block()
                                if self.current_token.get_token_type() == close_block_tok:
                                    self.next_token()
                                else:
                                    print("Error: Missing #}", self.current_token)
                            else:
                                print("Error: Missing #{", self.current_token)
                        else:
                            print("Error: Missing : after function declaration", self.current_token)
                    else:
                        print("Error: Parenthesis not closed", self.current_token)
                else:
                    print("Error: Parenthesis not opened", self.current_token)
            else:
                print("Error: Missing function name", self.current_token)
        else:
            print("Error: Missing def keyword", self.current_token)

    
    def declarations(self):
        while(self.current_token.get_token_value() == "#int"):
            self.next_token()
            self.id_list()
    
        
    def glob_decl(self):
        while(self.current_token.get_token_value() == 'global'):
            self.next_token()
            self.id_list

                                
    def id_list(self):
        if self.current_token.get_token_type() == variable_tok:
                self.next_token()
    
                while(self.current_token.get_token_type() == comma_tok):
                    self.next_token()
                    if(self.current_token.get_token_type() == variable_tok):
                        self.next_token()               
                    else:
                        print("Error: Missing variable after ,", self.current_token)
                        exit(-1)               
                
    def statement(self):
        if(self.current_token.get_token_type()==variable_tok or self.current_token.get_token_value()=='print' or self.current_token.get_token_value()=='return'):
            self.simple_statement()
        elif(self.current_token.get_token_value()=='if' or self.current_token.get_token_value()=='while'):
            self.structured_statement()
        else:
            print("Error: Statement not found", self.current_token)
            exit(-1)

    def code_block(self):
        self.statement()
        while(self.current_token.get_token_value()=='print' or self.current_token.get_token_value()=='return' or self.current_token.get_token_value()=='if' or self.current_token.get_token_value()=='while' or self.current_token.get_token_type()==variable_tok):
            self.statement()
            

    def simple_statement(self):
        if(self.current_token.get_token_type()==variable_tok):
            self.assignment_stat()
        elif(self.current_token.get_token_value()=='print'):
            self.print_stat()
        elif(self.current_token.get_token_value()=='return'):
            self.return_stat()
        
    def structured_statement(self):
        if(self.current_token.get_token_value()=='if'):
            self.if_stat()
        elif(self.current_token.get_token_value()=='while'):
            self.while_stat()

    def assignment_stat(self):
        if(self.current_token.get_token_type() == variable_tok):
            while(self.current_token.get_token_type() == variable_tok):
                self.next_token()
            
            if(self.current_token.get_token_type() == assignment_tok):
                self.next_token()
                if(self.current_token.get_token_value() == 'int'):
                    self.next_token()
                    if(self.current_token.get_token_type() == l_par_tok):
                        self.next_token()
                        if(self.current_token.get_token_value() == 'input'):
                            self.next_token()  
                            if(self.current_token.get_token_type() == l_par_tok):
                                self.next_token()
                                if(self.current_token.get_token_type() == r_par_tok):
                                    self.next_token()
                                    if(self.current_token.get_token_type() == r_par_tok):
                                        self.next_token()
                                    else:
                                        print("Error: Expected ) after assignement", self.current_token)
                                        exit(-1)
                                else:
                                    print("Error: Expected ) after assignement", self.current_token)
                                    exit(-1)
                            else:
                                print("Error: Expected ( in assignment", self.current_token)
                                exit(-1)
                        else:
                            print("Error: Missing input in assignment", self.current_token)
                            exit(-1)
                    else:
                        print("Error: Missing ( in assignment", self.current_token)
                        exit(-1)                
                else:
                    self.expression()
            else:
                print("Error: Expected '=' after variable", self.current_token)
                exit(-1) 
        else:
            print("Error: Missing variable", self.current_token)
            exit(-1)

    def print_stat(self):
        if(self.current_token.get_token_value() == 'print'):
            self.next_token()
            if(self.current_token.get_token_type() == l_par_tok):
                self.next_token() 
                self.expression()                
                if(self.current_token.get_token_type() == r_par_tok):
                    self.next_token() 
                else:
                    print("Error: print command left open", self.current_token)
                    exit(-1)
            else:
                print("Error: Missing left parenthesis in print command", self.current_token)
                exit(-1)
        else:
            print("Error: missing print command", self.current_token)
            exit(-1)

    def return_stat(self):
        if(self.current_token.get_token_value() == 'return'):
            self.next_token()
            self.expression()
        else:
            print("Error: Missing return command", self.current_token)
            exit(-1)

    def statement_or_block(self):
        self.statement()
        if self.current_token.get_token_type() == open_block_tok:
                    self.next_token()                
                    self.code_block()
                    if self.current_token.get_token_type() == close_block_tok:
                        self.next_token()
                    else:
                        print("Error: statement block left open", self.current_token)
                        exit(-1)
        '''else:
            print("Error: expected #{ before statement block", self.current_token)
            exit(-1)'''

    def if_stat(self):
        if self.current_token.get_token_value() == 'if':
            self.next_token()  
            self.condition()  
            if self.current_token.get_token_type() == colon_tok:
                self.next_token()
                self.statement_or_block()
                while self.current_token.get_token_value() == 'elif':
                    self.next_token()        
                    self.condition()
                    if self.current_token.get_token_type() == colon_tok:
                        self.next_token()             
                        self.statement_or_block()
                    else:
                        print("Error: missing colon after elif", self.current_token)
                        exit(-1)
                if self.current_token.get_token_value() == 'else':
                    self.next_token()         
                    if self.current_token.get_token_type() == colon_tok:
                        self.next_token()
                        self.statement_or_block()
                    else:
                        print("Error: missing colon after else", self.current_token)
                        exit(-1)
                else:
                    self.statement_or_block()
            else:
                print("Error: missing colon after if", self.current_token)
                exit(-1)

                
    def while_stat(self):
        if(self.current_token.get_token_value() == 'while'):
            self.next_token()
            self.condition()
            if(self.current_token.get_token_type() == colon_tok):
                self.next_token()
                if(self.current_token.get_token_type() == open_block_tok):
                    self.next_token()
                    self.code_block()
                    if(self.current_token.get_token_type() == close_block_tok):
                        self.next_token()            
                    else:
                        print("Error: while block left open", self.current_token)
                        exit(-1)
                else:
                    print("Error: missing #{ after while condition", self.current_token)
                    exit(-1)
            else:
                print("Error: missing collon after while condition", self.current_token)
                exit(-1)
        else:
            print("Error: missing while", self.current_token)
            exit(-1)


    def expression(self):
        # op = +|- -> add, sub
        # E -> T1 ( op T2 {P1} )* {P2} apo thewria dinontai ola

        self.optional_sign()
        T1place = self.term()
        while(self.current_token.get_token_type()==plus_tok or self.current_token.get_token_type()==minus_tok):
            add_op = self.ADD_OP()
            T2place =  self.term()

            w = self.newTemp()
            self.genQuad(add_op, T1place, T2place, w)
            T1place = w
        Eplace = T1place
        return Eplace
    

    def term(self):
        # op = *|//|% -> mul, div, mod
        # T -> F1 ( op F2 {P1} )* {P2} idio me expression
        F1place = self.factor()

        while(self.current_token.get_token_type()==mult_tok or self.current_token.get_token_type()==div_tok or self.current_token.get_token_type()==mod_tok):
            mul_op = self.MUL_OP()
            F2place = self.factor()

            w = self.newTemp()
            self.genQuad(mul_op, F1place, F2place, w)
            F1place = w
        Tplace = F1place
        return Tplace
    

    def factor(self):
        # F -> (E) {P1}  
        # P1 -> F.place = E.place metafora tou E.place sto F.place
        # thelw na epistrefw ta value twn tokens dhladh an exw digit, expression h paw se idtail
        if(self.current_token.get_token_type()==digit_tok):
            value = self.current_token.get_token_value()
            
            self.next_token() 
            return value       
        elif(self.current_token.get_token_type()==l_par_tok):
            self.next_token()

            eplace = self.expression()
            
            if(self.current_token.get_token_type()==r_par_tok):
                self.next_token()

                return eplace       
            else:
                print("Error: FACTOR statement left open", self.current_token)
                exit(-1)
        elif(self.current_token.get_token_type()==variable_tok or self.current_token.get_token_type()==def_tok):
            value = self.current_token.get_token_value()

            self.next_token()  

            self.idtail() 

            return value         
        else:
            print("Error: Element other than constant/expression/variable in FACTOR", self.current_token)
            exit(-1)
        
    
    def idtail(self):
        if(self.current_token.get_token_type() == l_par_tok ):
            self.next_token()
            self.actual_par_list()            
            if(self.current_token.get_token_type()==r_par_tok):
                self.next_token()                
            else:
                print("Error: Missing right parethesis in defnition", self.current_token)
                exit(-1)
        elif(self.current_token.get_token_value() == 'return'):
            self.return_stat()

    def actual_par_list(self):
        if (self.current_token.get_token_type()==digit_tok or self.current_token.get_token_type()==l_par_tok or self.current_token.get_token_type()==variable_tok):
            self.expression()
            while(self.current_token.get_token_type() == comma_tok):
                self.next_token()
                self.expression()            
                        
    def optional_sign(self):
        if(self.current_token.get_token_type() == plus_tok or self.current_token.get_token_type() == minus_tok):
            self.ADD_OP()
        
    def ADD_OP(self):
        # thelw na epistrefw kathe fora ton operator gia na pernei timh to op stoixeio tou quad
        if(self.current_token.get_token_type()==plus_tok):
            add_op = self.current_token.get_token_value()
            self.next_token()
            return add_op  
             
        elif(self.current_token.get_token_type()==minus_tok):
            minus_op = self.current_token.get_token_value()
            self.next_token()
            return minus_op
            
    def MUL_OP(self):
        # idio me ADD_OP
        if (self.current_token.get_token_type() == mult_tok):
            mul_op = self.current_token.get_token_value()
            self.next_token()  
            return mul_op         
        elif (self.current_token.get_token_type() == div_tok):
            div_op = self.current_token.get_token_value()
            self.next_token() 
            return div_op
        elif (self.current_token.get_token_type() == mod_tok):
            mod_op = self.current_token.get_token_value()
            self.next_token()
            return mod_op
                        
    def condition(self):
        self.bool_term()        
        while(self.current_token.get_token_value()=='or'):
            self.next_token()
            self.bool_term()
            
    def bool_term(self):
        self.bool_factor()
        while(self.current_token.get_token_value()=='and'):
            self.next_token()
            self.bool_factor()
                
    def bool_factor(self):
        if(self.current_token.get_token_type()=='not'):
            self.next_token()
            self.condition()
        else:
            self.expression()
            self.REL_OP()
            self.expression()

    def REL_OP(self):
        if(self.current_token.get_token_type()==equals_tok):
            self.next_token()       
        elif(self.current_token.get_token_type()==less_than_tok):
            self.next_token()      
        elif(self.current_token.get_token_type()==less_or_equals_tok):            
            self.next_token()       
        elif(self.current_token.get_token_type()==not_equals_tok):
            self.next_token()       
        elif(self.current_token.get_token_type()== more_than_tok):
            self.next_token()        
        elif(self.current_token.get_token_type()==more_or_equals_tok):
            self.next_token()      
        else:
            print("Error: Missing comparison token ", self.current_token)
            exit(-1)

    def call_main_part(self):
        if self.current_token.get_token_value() == '#def':
            self.next_token()
            if self.current_token.get_token_value() == 'main':
                self.next_token()
                self.declarations()
                self.code_block()
            else:
                print("Error: Missing main in call_main_part", self.current_token)
                exit(-1)
        else:
            print("Error: Missing #def in call_main_part", self.current_token)
            exit(-1)



if __name__ == "__main__":
    if len(sys.argv) == 0:
        print("Error")
        print(sys.argv)
        exit()
    lex = Lexical(filename=sys.argv[1]) 
    lex.lex()
    syn = Syntax(tokens=tokens)
    syn.startRule()
    