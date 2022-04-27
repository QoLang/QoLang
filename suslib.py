class Tokens:
  INTEGER   = 0
  EOF       = 1
  PLUS      = 2
  MINUS     = 3
  MULTIPLY  = 4
  DIVIDE    = 5

class Token:
  def __init__(self, type, value):
    self.type = type
    self.value = value

  def __str__(self):
    return f"Token({self.type}, {self.value})"

  def __repr__(self):
    return self.__str__()

class Interpreter:
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
    
    return Token(Tokens.EOF, None)

  def eat(self, token_type):
    if self.current_token.type == token_type:
      self.current_token = self.next_token()
    else:
      self.error()

  def factor(self):
    token = self.current_token
    self.eat(Tokens.INTEGER)
    return token.value

  def term(self):
    result = self.factor()

    while self.current_token.type in (Tokens.MULTIPLY, Tokens.DIVIDE):
      token = self.current_token
      match token.type:
        case Tokens.MULTIPLY:
          self.eat(Tokens.MULTIPLY)
          result = result * self.factor()
        case Tokens.DIVIDE:
          self.eat(Tokens.DIVIDE)
          result = result / self.factor()
    
    return result

  def expr(self):
    self.current_token = self.next_token()

    result = self.term()

    while self.current_token.type in (Tokens.PLUS, Tokens.MINUS, Tokens.MULTIPLY, Tokens.DIVIDE):
      token = self.current_token
      match token.type:
        case Tokens.PLUS:
          self.eat(Tokens.PLUS)
          result = result + self.term()
        case Tokens.MINUS:
          self.eat(Tokens.MINUS)
          result = result - self.term()
        case Tokens.MULTIPLY:
          self.eat(Tokens.MULTIPLY)
          result = result * self.term()
        case Tokens.DIVIDE:
          self.eat(Tokens.DIVIDE)
          result = result / self.term()
    
    return result