from qclasses import *

class Lexer:
  def __init__(self, text):
    self.text = text
    self.pos = 0
    self.current_token = None
    self.previous_token = None
    self.current_char = self.text[self.pos]
    self.line = 0
    self.column = 0
  
  def error(self):
    print("Lexer Error")
    print(self.text.splitlines()[self.line])
    print(" " * self.column + "^")
    print(f'Invalid character on position {str(self.line)}:{str(self.column)}')
    exit(1)

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
    self.advance()
    while self.current_char != '*' and self.peek() != '/':
      self.advance()
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
    line = self.line
    column = self.column
    reserved_keyws = {
      "func": Token(Tokens.FUNC, "func", line, column),
      "True": Token(Tokens.TRUE, "True", line, column),
      "False": Token(Tokens.FALSE, "False", line, column),
      "if": Token(Tokens.IF_ST, "if", line, column),
      "elif": Token(Tokens.ELIF_ST, "elif", line, column),
      "else": Token(Tokens.ELSE_ST, "else", line, column),
      "for": Token(Tokens.FOR_ST, "for", line, column),
      "while": Token(Tokens.WHILE_ST, "while", line, column),
      "times": Token(Tokens.TIMES_ST, "times", line, column),
      "as": Token(Tokens.AS, "as", line, column),
      "return": Token(Tokens.RETURN, "return", line, column),
      "in": Token(Tokens.IN, "in", line, column),
      "foreach": Token(Tokens.FOREACH, "foreach", line, column),
      "None": Token(Tokens.NONE, "None", line, column),
      "include": Token(Tokens.INCLUDE, "include", line, column),
      "define": Token(Tokens.DEFINE, "define", line, column),
    }
    isp = False
    if self.current_char == '&':
      isp = True
      self.advance()
    
    result = ''
    while self.current_char is not None and (self.current_char.isalnum() or self.current_char in ['_', '.']):
      result += self.current_char
      self.advance()
      
    if result[-1] == '.':
      self.error()

    self.skipspace()
    if self.current_char == '(' and result not in reserved_keyws and (self.previous_token.type != Tokens.FUNC if self.previous_token else True):
      token = Token(Tokens.FUNCCALL, result, line, column)
    elif isp:
      token = Token(Tokens.POINTER, result, line, column)
    else:
      token = reserved_keyws.get(result, Token(Tokens.ID, result, line, column))

    return token

  def string(self, char):
    line = self.line
    column = self.column
    self.advance()
    
    result = ''
    while self.current_char is not None and self.current_char != char:
      result += self.current_char
      self.advance()
        
    self.advance()

    return Token(Tokens.STRING, result, line, column)

  def fstring(self, char):
    line = self.line
    column = self.column
    self.advance()
    
    result = []
    currentstring = ''
    escaped = False
    while self.current_char is not None and (self.current_char != char or escaped):
      willadvance = True
      if escaped:
        if self.current_char == 'n':
          currentstring += '\n'
        elif self.current_char == 'r':
          currentstring += '\r'
        elif self.current_char == '\\':
          currentstring += '\\'
        elif self.current_char == '$':
          currentstring += '$'
        elif self.current_char == '\'':
          currentstring += '\''
        elif self.current_char == '"':
          currentstring += '"'
        else:
          currentstring += '\\' + self.current_char
        escaped = False
      else:
        if self.current_char == '\\':
          escaped = True
        elif self.current_char == '$':
          result += [Token(Tokens.STRING, currentstring, line, column)]
          currentstring = ''
          self.advance()
          result += [self._id()]
          willadvance = False
        else:
          currentstring += self.current_char
      if willadvance:
        self.advance()

    result += [Token(Tokens.STRING, currentstring, line, column)]
        
    self.advance()

    return Token(Tokens.FSTRING, result, line, column)

  def next_token(self):
    text = self.text
    self.previous_token = self.current_token

    while self.current_char is not None:
      line = self.line
      column = self.column
      
      if self.current_char.isspace():
        self.skipspace()
        continue

      elif self.current_char == '/' and self.peek() == '*':
        self.skipcomment()
        continue

      elif self.current_char.isdigit():
        self.current_token = Token(Tokens.INTEGER, self.integer(), line, column)
        
      elif self.current_char == "'":
        self.current_token = self.string("'")
        
      elif self.current_char == "\"":
        self.current_token = self.string("\"")
        
      elif self.current_char == "%":
        self.advance()
        if self.current_char == "'":
          self.current_token = self.fstring("'")
          
        elif self.current_char == "\"":
          self.current_token = self.fstring("\"")

      elif self.current_char == '+' and self.peek() == '=':
        self.advance()
        self.advance()
        self.current_token = Token(Tokens.ADD, '+=', line, column)

      elif self.current_char == '+':
        self.advance()
        self.current_token = Token(Tokens.PLUS, '+', line, column)

      elif self.current_char == '-':
        self.advance()
        self.current_token = Token(Tokens.MINUS, '-', line, column)

      elif self.current_char == '*' and self.peek() == '*':
        self.advance()
        self.advance()
        self.current_token = Token(Tokens.POWER, '**', line, column)

      elif self.current_char == '*':
        self.advance()
        self.current_token = Token(Tokens.MULTIPLY, '*', line, column)

      elif self.current_char == '/':
        self.advance()
        self.current_token = Token(Tokens.DIVIDE, '/', line, column)

      elif self.current_char == '(':
        self.advance()
        self.current_token = Token(Tokens.LPAREN, '(', line, column)

      elif self.current_char == ')':
        self.advance()
        self.current_token = Token(Tokens.RPAREN, ')', line, column)

      elif self.current_char == '&' and self.peek() == '&':
        self.advance()
        self.advance()
        self.current_token = Token(Tokens.AND, '&&', line, column)
      
      elif self.current_char == '|' and self.peek() == '|':
        self.advance()
        self.advance()
        self.current_token = Token(Tokens.OR, '||', line, column)
      
      elif self.current_char.isalpha() or self.current_char == '_' or self.current_char == '&':
        self.current_token = self._id()

      elif self.current_char == '=' and self.peek() == '=':
        self.advance()
        self.advance()
        self.current_token = Token(Tokens.EQUAL, '==', line, column)

      elif self.current_char == '=':
        self.advance()
        self.current_token = Token(Tokens.ASSIGN, '=', line, column)

      elif self.current_char == '<' and self.peek() == '=':
        self.advance()
        self.advance()
        self.current_token = Token(Tokens.LESS_EQUAL, '<=', line, column)

      elif self.current_char == '>' and self.peek() == '=':
        self.advance()
        self.advance()
        self.current_token = Token(Tokens.GREATER_EQUAL, '>=', line, column)

      elif self.current_char == '!' and self.peek() == '=':
        self.advance()
        self.advance()
        self.current_token = Token(Tokens.NOT_EQUAL, '!=', line, column)

      elif self.current_char == ';':
        self.advance()
        self.current_token = Token(Tokens.SEMI, ';', line, column)

      elif self.current_char == '{':
        self.advance()
        self.current_token = Token(Tokens.BEGIN, '{', line, column)

      elif self.current_char == '}':
        self.advance()
        self.current_token = Token(Tokens.END, '}', line, column)

      elif self.current_char == ':':
        self.advance()
        self.current_token = Token(Tokens.COL, ':', line, column)

      elif self.current_char == ',':
        self.advance()
        self.current_token = Token(Tokens.COMMA, ',', line, column)

      elif self.current_char == '[':
        self.advance()
        self.current_token = Token(Tokens.SBRACKETL, '[', line, column)

      elif self.current_char == ']':
        self.advance()
        self.current_token = Token(Tokens.SBRACKETR, ']', line, column)

      elif self.current_char == '<':
        self.advance()
        self.current_token = Token(Tokens.LESS_THAN, '<', line, column)

      elif self.current_char == '>':
        self.advance()
        self.current_token = Token(Tokens.GREATER_THAN, '>', line, column)
      
      else:
        self.error()
      
      return self.current_token
    self.current_token = Token(Tokens.EOF, None, self.line, self.column)
    return self.current_token
