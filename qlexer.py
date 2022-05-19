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
  
  def _id(self):
    reserved_keyws = {
      "func": Token(Tokens.FUNC, "func", self.line, self.column),
      "True": Token(Tokens.TRUE, "True", self.line, self.column),
      "False": Token(Tokens.FALSE, "False", self.line, self.column),
      "if": Token(Tokens.IF_ST, "if", self.line, self.column),
      "elif": Token(Tokens.ELIF_ST, "elif", self.line, self.column),
      "else": Token(Tokens.ELSE_ST, "else", self.line, self.column),
      "for": Token(Tokens.FOR_ST, "for", self.line, self.column)
    }
    isp = False
    if self.current_char == '&':
      isp = True
      self.advance()
    
    result = ''
    while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
      result += self.current_char
      self.advance()

    self.skipspace()
    if self.current_char == '(' and result not in reserved_keyws:
      token = Token(Tokens.FUNCCALL, result, self.line, self.column)
    elif isp:
      token = Token(Tokens.POINTER, result, self.line, self.column)
    else:
      token = reserved_keyws.get(result, Token(Tokens.ID, result, self.line, self.column))

    return token

  def string(self, char):
    self.advance()
    
    result = ''
    while self.current_char is not None and self.current_char != char:
      result += self.current_char
      self.advance()
        
    self.advance()

    return Token(Tokens.STRING, result, self.line, self.column)

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
        return Token(Tokens.INTEGER, self.integer(), self.line, self.column)
        
      if self.current_char == "'":
        return self.string("'")
        
      if self.current_char == "\"":
        return self.string("\"")

      if self.current_char == '+':
        self.advance()
        return Token(Tokens.PLUS, '+', self.line, self.column)

      if self.current_char == '-':
        self.advance()
        return Token(Tokens.MINUS, '-', self.line, self.column)

      if self.current_char == '*':
        self.advance()
        return Token(Tokens.MULTIPLY, '*', self.line, self.column)

      if self.current_char == '/':
        self.advance()
        return Token(Tokens.DIVIDE, '/', self.line, self.column)

      if self.current_char == '(':
        self.advance()
        return Token(Tokens.LPAREN, '(', self.line, self.column)

      if self.current_char == ')':
        self.advance()
        return Token(Tokens.RPAREN, ')', self.line, self.column)
      
      if self.current_char.isalpha() or self.current_char == '&':
        return self._id()

      if self.current_char == ':' and self.peek() == '=':
        self.advance()
        self.advance()
        return Token(Tokens.ASSIGN, ':=', self.line, self.column)

      if self.current_char == '=' and self.peek() == '=':
        self.advance()
        self.advance()
        return Token(Tokens.EQUAL, '==', self.line, self.column)

      if self.current_char == '<' and self.peek() == '=':
        self.advance()
        self.advance()
        return Token(Tokens.LESS_EQUAL, '<=', self.line, self.column)

      if self.current_char == '>' and self.peek() == '=':
        self.advance()
        self.advance()
        return Token(Tokens.GREATER_EQUAL, '>=', self.line, self.column)

      if self.current_char == '!' and self.peek() == '=':
        self.advance()
        self.advance()
        return Token(Tokens.NOT_EQUAL, '!=', self.line, self.column)

      if self.current_char == ';':
        self.advance()
        return Token(Tokens.SEMI, ';', self.line, self.column)

      if self.current_char == '{':
        self.advance()
        return Token(Tokens.BEGIN, '{', self.line, self.column)

      if self.current_char == '}':
        self.advance()
        return Token(Tokens.END, '}', self.line, self.column)

      if self.current_char == ':':
        self.advance()
        return Token(Tokens.COL, ':', self.line, self.column)

      if self.current_char == ',':
        self.advance()
        return Token(Tokens.COMMA, ',', self.line, self.column)

      if self.current_char == '[':
        self.advance()
        return Token(Tokens.SBRACKETL, '[', self.line, self.column)

      if self.current_char == ']':
        self.advance()
        return Token(Tokens.SBRACKETR, ']', self.line, self.column)

      if self.current_char == '<':
        self.advance()
        return Token(Tokens.LESS_THAN, '<', self.line, self.column)

      if self.current_char == '>':
        self.advance()
        return Token(Tokens.GREATER_THAN, '>', self.line, self.column)
    return Token(Tokens.EOF, None, self.line, self.column)
