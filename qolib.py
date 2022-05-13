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
  
  def error(self):
    raise Exception('Invalid character')

  def advance(self):
    self.pos += 1
    if self.pos > len(self.text) - 1:
      self.current_char = None
    else:
      self.current_char = self.text[self.pos]

  def skipspace(self):
    while self.current_char is not None and self.current_char.isspace():
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
    "False": Token(Tokens.FALSE, "False")
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
    if self.current_char == '(':
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
  
  def error(self):
    raise Exception('Syntax error - ' + str(self.lexer.pos))

  def eat(self, token_type):
    if self.current_token.type == token_type:
      self.current_token = self.lexer.next_token()
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
  
  def program(self):
    node = self.compound_statement() # program
    return node
  
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

  def parse(self):
    node = self.program()

    if self.current_token.type != Tokens.EOF:
      self.error()
    
    return node

#endregion
#region The Interpreter

class NodeVisitor:
  def visit(self, node):
    method_name = 'visit_' + type(node).__name__
    visitor = getattr(self, method_name, self.generic_visit)
    return visitor(node)

  def generic_visit(self, node):
    raise Exception(f"No visit_{type(node).__name__} method")

class Interpreter(NodeVisitor):
  def __init__(self, parser):
    self.parser = parser

  def visit_BinOp(self, node):
    left = self.visit(node.left)
    right = self.visit(node.right)
    if isinstance(left, VarVal):
      left = left.value
    if isinstance(right, VarVal):
      right = right.value
    match node.op.type:
      case Tokens.PLUS:
        return left + right
      case Tokens.MINUS:
        return left - right
      case Tokens.MULTIPLY:
        return left * right
      case Tokens.DIVIDE:
        return left / right
      case Tokens.LESS_THAN:
        return str(left < right)
      case Tokens.GREATER_THAN:
        return str(left > right)
      case Tokens.EQUAL:
        return str(left == right)
      case Tokens.LESS_EQUAL:
        return str(left <= right)
      case Tokens.GREATER_EQUAL:
        return str(left >= right)
      case Tokens.NOT_EQUAL:
        return str(left != right)
  
  def visit_Num(self, node):
    return node.value
  
  def visit_UnaryOp(self, node):
    op = node.op.type
    match node.op.type:
      case Tokens.PLUS:
        val = self.visit(node.expr)
        if isinstance(val, VarVal):
          val = val.value
        return +val
      case Tokens.MINUS:
        val = self.visit(node.expr)
        if isinstance(val, VarVal):
          val = val.value
        return -val

  def visit_Compound(self, node):
    for child in node.children:
      self.visit(child)

  def visit_NoOp(self, node):
    pass

  def visit_Assign(self, node):
    var_name = node.left.value
    var_val = self.visit(node.right)
    var = VarVal(var_name, var_val)
    Variables.setVar(var)

  def visit_Var(self, node):
    var_name = node.value
    val = Variables.getVar(var_name)
    if val is None:
      raise NameError(repr(var_name))
    else:
      return val

  def visit_FncDec(self, node):
    Variables.setVar(node)

  def visit_FncCall(self, node):
    var = Variables.getVar(node.name)
    if var is None:
      raise Exception("Function not found")
    if not len(node.args) == len(var.args):
      raise Exception(f"Expected {str(len(node.args))} args, got {str(len(var.args))}")
    
    i = 0
    for arg in node.args:
      nvar = VarVal(var.args[i].value, arg.token)
      Variables.setVar(nvar)
      i += 1
    
    nnode = self.visit(var.node)
    return nnode

  def visit_BuiltinFuncCall(self, node):
    global Variables
    args = []
    i = 0
    for arg in node.args:
      args += [self.visit(arg)]
      i += 1

    Variables = node.func(Variables, args)

  def visit_String(self, node):
    return node.value

  def visit_Boolean(self, node):
    return node.value

  def visit_Pointer(self, node):
    return node.value

  def interpret(self):
    tree = self.parser.parse()
    if tree is None:
      return ''
    return self.visit(tree)

#endregion