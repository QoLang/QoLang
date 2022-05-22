import qstd

#region Tokens

class Tokens:
  INTEGER       = "INTEGER"
  EOF           = "EOF"
  PLUS          = "PLUS"
  MINUS         = "MINUS"
  MULTIPLY      = "MULTIPLY"
  DIVIDE        = "DIVIDE"
  LPAREN        = "LPAREN"
  RPAREN        = "RPAREN"
  BEGIN         = "BEGIN"
  END           = "END"
  ASSIGN        = "ASSIGN"
  SEMI          = "SEMI"
  ID            = "ID"
  FUNC          = "FUNC"
  COL           = "COL"
  FUNCCALL      = "FUNCCALL"
  COMMA         = "COMMA"
  SBRACKETL     = "SBRACKETL"
  SBRACKETR     = "SBRACKETR"
  STRING        = "STRING"
  LESS_THAN     = "LESS_THAN"
  GREATER_THAN  = "GREATER_THAN"
  EQUAL         = "EQUAL"
  LESS_EQUAL    = "LESS_EQUAL"
  GREATER_EQUAL = "GREATER_EQUAL"
  NOT_EQUAL     = "NOT_EQUAL"
  TRUE          = "TRUE"
  FALSE         = "FALSE"
  POINTER       = "POINTER"
  IF_ST         = "IF_ST"
  ELIF_ST       = "ELIF_ST"
  ELSE_ST       = "ELSE_ST"
  FOR_ST        = "FOR_ST"
  WHILE_ST      = "WHILE_ST"
  TIMES_ST      = "TIMES_ST"
  AS            = "AS"
  AND           = "AND"
  OR            = "OR"
  FSTRING       = "FSTRING"
  RETURN        = "RETURN"
  LISTITEM      = "LISTITEM"

class Token:
  def __init__(self, type, value, line, col):
    self.type = type
    self.value = value
    self.line = line
    self.col = col

  def __str__(self):
    return f"Token({self.type}, '{self.value}', {self.line}, {self.col})"

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

class Boolean(AST):
  def __init__(self, token):
    self.token = token
    self.value = token.value == "True"

class Pointer(AST):
  def __init__(self, token):
    self.token = token
    self.value = token.value

class If_St(AST):
    def __init__(self, condition, consequences, alternatives):
        self.condition = condition
        self.consequences = consequences
        self.alternatives = alternatives

class For_St(AST):
    def __init__(self, initial, condition, everyiter, statements):
        self.initial = initial
        self.condition = condition
        self.everyiter = everyiter # statement to run after every iteration
        self.statements = statements

class While_St(AST):
    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements

class Times_St(AST):
    def __init__(self, times, statements, _as = None):
        self.times = times # run `times` times
        self._as = _as # how many times did we run yet
        self.statements = statements

class Fstring(AST):
  def __init__(self, token):
    self.token = token
    self.nodes = token.value

class Return(AST):
  def __init__(self, token, value):
    self.token = token
    self.value = value

class List(AST):
  def __init__(self, token, values):
    self.token = token
    self.values = values

class ListItem(AST):
  def __init__(self, token, item):
    self.token = token
    self.value = token.value
    self.item = item

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
