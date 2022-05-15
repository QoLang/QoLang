import qstd
from qclasses import * 

#region Built-in Functions

for fn in qstd.available_functions:
  added = BuiltinFunc(fn, getattr(qstd, fn))
  Variables.setVar(added)

#endregion
#region The Lexer

class Lexer:
  def __init__(self, text):
    self.text = text
    self.pos = 0
    self.current_token = None
    self.current_char = self.text[self.pos]
    self.line = 1
    self.column = 1
  
  def error(self):
    raise Exception(f'Invalid character, line: {str(self.line)}, col:{str(self.column)}')

  def advance(self):
    if self.current_char == '\n':
      self.line += 1
      self.column = 0

    self.pos += 1
    if self.pos > len(self.text) - 1:
      self.current_char = None
    else:
      self.current_char = self.text[self.pos]
      self.column += 1

  def skipspace(self):
    while self.current_char is not None and self.current_char.isspace():
      self.advance()

  def skipcomment(self):
    self.advance()
    while self.current_char != '|':
      self.advance()
    self.advance()

  def integer(self):
    result = ''
    while self.current_char is not None and self.current_char.isdigit():
      result += self.current_char
      self.advance()
    return int(result)

  def peek(self):
    peek_pos = self.pos + 1
    if peek_pos > len(self.text) - 1:
      return None
    else:
      return self.text[peek_pos]

  reserved_keyws = {
    "func": Token(Tokens.FUNC, "func"),
    "True": Token(Tokens.TRUE, "True"),
    "False": Token(Tokens.FALSE, "False"),
    "if": Token(Tokens.IF_ST, "if"),
    "elif": Token(Tokens.ELIF_ST, "elif"),
    "else": Token(Tokens.ELSE_ST, "else")
  }
  
  def _id(self):
    isp = False
    if self.current_char == '&':
      isp = True
      self.advance()
    
    result = ''
    while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
      result += self.current_char
      self.advance()

    self.skipspace()
    if self.current_char == '(' and result not in self.reserved_keyws:
      token = Token(Tokens.FUNCCALL, result)
    elif isp:
      token = Token(Tokens.POINTER, result)
    else:
      token = self.reserved_keyws.get(result, Token(Tokens.ID, result))

    return token

  def string(self, char):
    self.advance()
    
    result = ''
    while self.current_char is not None and self.current_char != char:
      result += self.current_char
      self.advance()
        
    self.advance()

    return Token(Tokens.STRING, result)

  def next_token(self):
    text = self.text

    while self.current_char is not None:
      if self.current_char.isspace():
        self.skipspace()
        continue

      if self.current_char == '|':
        self.skipcomment()
        continue

      if self.current_char.isdigit():
        return Token(Tokens.INTEGER, self.integer())
        
      if self.current_char == "'":
        return self.string("'")
        
      if self.current_char == "\"":
        return self.string("\"")

      if self.current_char == '+':
        self.advance()
        return Token(Tokens.PLUS, '+')

      if self.current_char == '-':
        self.advance()
        return Token(Tokens.MINUS, '-')

      if self.current_char == '*':
        self.advance()
        return Token(Tokens.MULTIPLY, '*')

      if self.current_char == '/':
        self.advance()
        return Token(Tokens.DIVIDE, '/')

      if self.current_char == '(':
        self.advance()
        return Token(Tokens.LPAREN, '(')

      if self.current_char == ')':
        self.advance()
        return Token(Tokens.RPAREN, ')')
      
      if self.current_char.isalpha() or self.current_char == '&':
        return self._id()

      if self.current_char == ':' and self.peek() == '=':
        self.advance()
        self.advance()
        return Token(Tokens.ASSIGN, ':=')

      if self.current_char == '=' and self.peek() == '=':
        self.advance()
        self.advance()
        return Token(Tokens.EQUAL, '==')

      if self.current_char == '<' and self.peek() == '=':
        self.advance()
        self.advance()
        return Token(Tokens.LESS_EQUAL, '<=')

      if self.current_char == '>' and self.peek() == '=':
        self.advance()
        self.advance()
        return Token(Tokens.GREATER_EQUAL, '>=')

      if self.current_char == '!' and self.peek() == '=':
        self.advance()
        self.advance()
        return Token(Tokens.NOT_EQUAL, '!=')

      if self.current_char == ';':
        self.advance()
        return Token(Tokens.SEMI, ';')

      if self.current_char == '{':
        self.advance()
        return Token(Tokens.BEGIN, '{')

      if self.current_char == '}':
        self.advance()
        return Token(Tokens.END, '}')

      if self.current_char == ':':
        self.advance()
        return Token(Tokens.COL, ':')

      if self.current_char == ',':
        self.advance()
        return Token(Tokens.COMMA, ',')

      if self.current_char == '[':
        self.advance()
        return Token(Tokens.SBRACKETL, '[')

      if self.current_char == ']':
        self.advance()
        return Token(Tokens.SBRACKETR, ']')

      if self.current_char == '<':
        self.advance()
        return Token(Tokens.LESS_THAN, '<')

      if self.current_char == '>':
        self.advance()
        return Token(Tokens.GREATER_THAN, '>')
    return Token(Tokens.EOF, None)

#endregion
#region The Parser

class Parser:
  def __init__(self, lexer):
    self.lexer = lexer
    self.current_token = self.lexer.next_token()
    self.next_token = self.lexer.next_token()
  
  def error(self):
    raise Exception(f'Syntax error, token: {str(self.current_token)}')

  def get_next_token(self):
    current_token = self.next_token
    self.next_token = self.lexer.next_token()
    return current_token

  def eat(self, token_type):
    if self.current_token.type == token_type:
      self.current_token = self.get_next_token()
    else:
      self.error()

  def factor(self):
    token = self.current_token
    match token.type:
      case Tokens.PLUS:
        self.eat(Tokens.PLUS)
        return UnaryOp(token, self.factor())
      case Tokens.MINUS:
        self.eat(Tokens.MINUS)
        return UnaryOp(token, self.factor())
      case Tokens.INTEGER:
        self.eat(Tokens.INTEGER)
        return Num(token)
      case Tokens.LPAREN:
        self.eat(Tokens.LPAREN)
        node = self.expr()
        self.eat(Tokens.RPAREN)
        return node
      case Tokens.STRING:
        self.eat(Tokens.STRING)
        return String(token)
      case Tokens.TRUE:
        self.eat(Tokens.TRUE)
        return Boolean(token)
      case Tokens.FALSE:
        self.eat(Tokens.FALSE)
        return Boolean(token)
      case Tokens.POINTER:
        self.eat(Tokens.POINTER)
        return Pointer(token)
      case _:
        node = self.variable()
        return node

  def term(self):
    node = self.factor()

    while self.current_token.type in (Tokens.MULTIPLY, Tokens.DIVIDE):
      token = self.current_token
      match token.type:
        case Tokens.MULTIPLY:
          self.eat(Tokens.MULTIPLY)
        case Tokens.DIVIDE:
          self.eat(Tokens.DIVIDE)
      node = BinOp(node, token, self.factor())
    
    return node

  def expr(self):
    return self.relation()
  
  def relation(self):
    node = self.arithmetic_expr()
    if self.current_token.type in (
      Tokens.LESS_THAN,
      Tokens.GREATER_THAN,
      Tokens.LESS_EQUAL,
      Tokens.GREATER_EQUAL,
      Tokens.EQUAL,
      Tokens.NOT_EQUAL,
    ):
      token = self.current_token
      match self.current_token.type:
        case Tokens.LESS_THAN:
          self.eat(Tokens.LESS_THAN)
        case Tokens.GREATER_THAN:
          self.eat(Tokens.GREATER_THAN)
        case Tokens.EQUAL:
          self.eat(Tokens.EQUAL)
        case Tokens.LESS_EQUAL:
          self.eat(Tokens.LESS_EQUAL)
        case Tokens.GREATER_EQUAL:
          self.eat(Tokens.GREATER_EQUAL)
        case Tokens.NOT_EQUAL:
          self.eat(Tokens.NOT_EQUAL)
      node = BinOp(left=node, op=token, right=self.arithmetic_expr())
    return node

  def arithmetic_expr(self):
    node = self.term()
    
    while self.current_token.type in (Tokens.PLUS, Tokens.MINUS, Tokens.MULTIPLY, Tokens.DIVIDE):
      token = self.current_token
      match token.type:
        case Tokens.PLUS:
          self.eat(Tokens.PLUS)
        case Tokens.MINUS:
          self.eat(Tokens.MINUS)
      node = BinOp(node, token, self.term())

    return node
  
  def program(self): # compound statement, without {}
    nodes = self.statement_list()
    root = Compound()
    for node in nodes:
      root.children.append(node)

    return root
  
  def compound_statement(self):
    self.eat(Tokens.BEGIN)
    nodes = self.statement_list()
    self.eat(Tokens.END)

    root = Compound()
    for node in nodes:
      root.children.append(node)

    return root
  
  def statement_list(self):
    node = self.statement()

    results = [node]

    while self.current_token.type == Tokens.SEMI:
      self.eat(Tokens.SEMI)
      results.append(self.statement())

    if self.current_token.type == Tokens.ID:
      self.error()
    
    if not isinstance(results[-1], NoOp):
      self.error()

    return results
  
  def statement(self):
    match self.current_token.type:
      case Tokens.BEGIN:
        node = self.compound_statement()
      case Tokens.ID:
        node = self.assignment_statement()
      case Tokens.FUNC:
        node = self.fncdec()
      case Tokens.FUNCCALL:
        node = self.fnccall()
      case Tokens.IF_ST:
        node = self.if_st()
      case _:
        node = self.empty()
    return node
    
  def assignment_statement(self):
    left = self.variable()
    token = self.current_token
    self.eat(Tokens.ASSIGN)
    right = self.expr()
    node = Assign(left, token, right)
    return node
  
  def variable(self):
    node = Var(self.current_token)
    self.eat(Tokens.ID)
    return node

  def empty(self):
    return NoOp()
  
  def fncdec(self):
    self.eat(Tokens.FUNC)
    self.eat(Tokens.COL)
    proc_name = self.current_token.value
    self.eat(Tokens.ID)
    self.eat(Tokens.SBRACKETL)

    args = [self.expr()]
    while self.current_token.type == Tokens.COMMA:
      self.eat(Tokens.COMMA)
      args.append(self.expr())

    self.eat(Tokens.SBRACKETR)
    node = self.compound_statement()
    var = FncDec(proc_name, node, args)
    return var
  
  def fnccall(self):
    proc_name = self.current_token.value
    self.eat(Tokens.FUNCCALL)
    self.eat(Tokens.LPAREN)

    toadd = self.expr()
    args = [toadd]
    while self.current_token.type == Tokens.COMMA:
      self.eat(Tokens.COMMA)
      toadd = self.expr()
      args.append(toadd)

    self.eat(Tokens.RPAREN)

    func = Variables.getVar(proc_name)
    var = None

    if func is None:
      func = Variables.getVar("func_" + proc_name)
      if func is None:
        self.error()
      else:
        var = BuiltinFuncCall(func.func, args)
    else:
      var = FncCall(proc_name, args)

    return var
  
  def if_st(self):
    if self.current_token.type == Tokens.IF_ST:
      self.eat(Tokens.IF_ST)                 # if
    else:                                    # *or*
      self.eat(Tokens.ELIF_ST)               # elif
    self.eat(Tokens.LPAREN)                  # (
    condition = self.expr()                  # condition
    self.eat(Tokens.RPAREN)                  # )
    consequences = self.compound_statement() # { code(); }

    alternatives = [] # else

    if (self.current_token.type == Tokens.ELSE_ST and self.next_token.type == Tokens.IF_ST) or self.next_token.type == Tokens.ELIF_ST:
      alternatives.append(self.elif_st())
    elif self.current_token.type == Tokens.ELSE_ST:
      alternatives.extend(self.else_st())
    
    node = If_St(condition=condition)

    for consequence in consequences.children:
      node.consequences.append(consequence)

    for alternative in alternatives:
      node.alternatives.append(alternative)
    
    self.current_token = Token(Tokens.SEMI, ';')

    return node
  
  def elif_st(self):
    if self.current_token.type == Tokens.ELSE_ST:
      self.eat(Tokens.ELSE_ST)
    return self.if_st()
  
  def else_st(self):
    self.eat(Tokens.ELSE_ST)         # else
    self.eat(Tokens.BEGIN)        # {
    nodes = self.statement_list() # code();
    self.eat(Tokens.END)          # }
    return nodes

  def parse(self):
    node = self.program()

    if self.current_token.type != Tokens.EOF:
      self.error()
    
    return node

#endregion