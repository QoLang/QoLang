from qclasses import *

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
