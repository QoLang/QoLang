class Tokens:
  INTEGER   = 0
  EOF       = 1
  PLUS      = 2
  MINUS     = 3
  MULTIPLY  = 4
  DIVIDE    = 5
  LPAREN    = 6
  RPAREN    = 7

class Token:
  def __init__(self, type, value):
    self.type = type
    self.value = value

  def __str__(self):
    return f"Token({self.type}, {self.value})"

  def __repr__(self):
    return self.__str__()

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

class Lexer:
  def __init__(self, text):
    self.text = text
    self.pos = 0
    self.current_token = None
    self.current_char = self.text[self.pos]
  
  def error(self):
    raise Exception('Syntax error')

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
    
    return Token(Tokens.EOF, None)

class Parser:
  def __init__(self, lexer):
    self.lexer = lexer
    self.current_token = self.lexer.next_token()

  def eat(self, token_type):
    if self.current_token.type == token_type:
      self.current_token = self.lexer.next_token()
    else:
      self.error()

  def factor(self):
    token = self.current_token
    match token.type:
      case Tokens.INTEGER:
        self.eat(Tokens.INTEGER)
        return Num(token)
      case Tokens.LPAREN:
        self.eat(Tokens.LPAREN)
        node = self.expr()
        self.eat(Tokens.RPAREN)
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

  def parse(self):
    return self.expr()

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