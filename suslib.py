#region Tokens

class Tokens:
  INTEGER   = "INTEGER"
  EOF       = "EOF"
  PLUS      = "PLUS"
  MINUS     = "MINUS"
  MULTIPLY  = "MULTIPLY"
  DIVIDE    = "DIVIDE"
  LPAREN    = "LPAREN"
  RPAREN    = "RPAREN"
  BEGIN     = "BEGIN"
  END       = "END"
  ASSIGN    = "ASSIGN"
  SEMI      = "SEMI"
  ID        = "ID"

class Token:
  def __init__(self, type, value):
    self.type = type
    self.value = value

  def __str__(self):
    return f"Token({self.type}, {self.value})"

  def __repr__(self):
    return self.__str__()

#endregion
#region Absract Syntax Trees

class AST:
  pass

class BinOp(AST):
  def __init__(self, left, op, right):
    self.left = left
    self.token = self.op = op
    self.right = right

class Num(AST):
  def __init__(self, token):
    self.token = token
    self.value = token.value

class UnaryOp(AST):
  def __init__(self, op, expr):
    self.token = self.op = op
    self.expr = expr

class Compound(AST):
  def __init__(self):
    self.children = []

class Assign(AST):
  def __init__(self, left, op, right):
    self.left = left
    self.token = self.op = op
    self.right = right

class Var(AST):
  def __init__(self, token):
    self.token = token
    self.value = token.value

class NoOp(AST):
  pass

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

  def _id(self):
    result = ''
    while self.current_char is not None and self.current_char.isalnum():
      result += self.current_char
      self.advance()

    token = Token(Tokens.ID, result)
    return token

  def next_token(self):
    text = self.text

    while self.current_char is not None:
      if self.current_char.isspace():
        self.skipspace()
        continue

      if self.current_char.isdigit():
        return Token(Tokens.INTEGER, self.integer())

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
      
      if self.current_char.isalpha():
        return self._id()

      if self.current_char == ':' and self.peek() == '=':
        self.advance()
        self.advance()
        return Token(Tokens.ASSIGN, ':=')

      if self.current_char == ';':
        self.advance()
        return Token(Tokens.SEMI, ';')

      if self.current_char == '{':
        self.advance()
        return Token(Tokens.BEGIN, '{')

      if self.current_char == '}':
        self.advance()
        return Token(Tokens.END, '}')
    
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
    node = self.compound_statement()
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
    if self.current_token.type == Tokens.BEGIN:
      node = self.compound_statement()
    elif self.current_token.type == Tokens.ID:
      node = self.assignment_statement()
    else:
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
    self.GLOBAL_SCOPE = {}

  def visit_BinOp(self, node):
    match node.op.type:
      case Tokens.PLUS:
        return self.visit(node.left) + self.visit(node.right)
      case Tokens.MINUS:
        return self.visit(node.left) - self.visit(node.right)
      case Tokens.MULTIPLY:
        return self.visit(node.left) * self.visit(node.right)
      case Tokens.DIVIDE:
        return self.visit(node.left) / self.visit(node.right)
  
  def visit_Num(self, node):
    return node.value
  
  def visit_UnaryOp(self, node):
    op = node.op.type
    match node.op.type:
      case Tokens.PLUS:
        return +self.visit(node.expr)
      case Tokens.MINUS:
        return -self.visit(node.expr)

  def visit_Compound(self, node):
    for child in node.children:
      self.visit(child)

  def visit_NoOp(self, node):
    pass

  def visit_Assign(self, node):
    var_name = node.left.value
    self.GLOBAL_SCOPE[var_name] = self.visit(node.right)

  def visit_Var(self, node):
    var_name = node.value
    val = self.GLOBAL_SCOPE.get(var_name)
    if val is None:
      raise NameError(repr(var_name))
    else:
      return val
  
  def interpret(self):
    tree = self.parser.parse()
    if tree is None:
      return ''
    return self.visit(tree)

#endregion