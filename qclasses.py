import qstd

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
  FUNC      = "FUNC"
  COL       = "COL"
  FUNCCALL  = "FUNCCALL"
  COMMA     = "COMMA"
  SBRACKETL = "SBRACKETL"
  SBRACKETR = "SBRACKETR"
  STRING    = "STRING"

class Token:
  def __init__(self, type, value):
    self.type = type
    self.value = value

  def __str__(self):
    return f"Token({self.type}, '{self.value}')"

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
  
  def __str__(self):
    return f"BinOp({self.left}, {self.op}, {self.right})"

class Num(AST):
  def __init__(self, token):
    self.token = token
    self.value = token.value
  
  def __str__(self):
    return f"Num({self.token}, {self.value})"

class UnaryOp(AST):
  def __init__(self, op, expr):
    self.token = self.op = op
    self.expr = expr
  
  def __str__(self):
    return f"UnaryOp({self.token}, {self.expr})"

class Compound(AST):
  def __init__(self):
    self.children = []
  
  def __str__(self):
    return f"Compound({', '.join(self.children)})"

class Assign(AST):
  def __init__(self, left, op, right):
    self.left = left
    self.token = self.op = op
    self.right = right
  
  def __str__(self):
    return f"Assign({self.left}, {self.op}, {self.right})"

class Var(AST):
  def __init__(self, token):
    self.token = token
    self.value = token.value
  
  def __str__(self):
    return f"Var({self.token}, {self.value})"

class NoOp(AST):
  pass

class FncDec(AST):
  def __init__(self, name, node, args):
    self.name = name
    self.node = node
    self.args = args

class FncCall(AST):
  def __init__(self, name, args):
    self.name = name
    self.args = args
    self.value = None

class BuiltinFunc(AST):
  def __init__(self, name, func):
    self.name = name
    self.func = func
    self.args = list(func.__code__.co_varnames)[1:]

class BuiltinFuncCall(AST):
  def __init__(self, func, args):
    self.func = func
    self.args = args
    self.value = None

class String(AST):
  def __init__(self, token):
    self.token = token
    self.value = token.value

#endregion
#region Variables

class Variable:
  pass

class VarVal(Variable):
  def __init__(self, name, value):
    self.name = name
    self.value = value
  
  def __str__(self):
    return f"VarVal({self.name}, {self.value})"

class VarFnc(Variable):
  def __init__(self, name, node):
    self.name = name
    self.node = node
  
  def __str__(self):
    return f"VarFnc({self.name})"

class Vars:
  def __init__(self):
    self.vars = []
  
  def getVar(self, name):
    for var in self.vars:
      if var.name == name:
        return var
    return None
  
  def setVar(self, var):
    i = 0
    for vvar in self.vars:
      if vvar.name == var.name:
        self.vars[i] = var
        return
      i += 1
    self.vars += [var]

Variables = Vars()

#endregion
