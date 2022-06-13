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
  IN            = "IN"
  FOREACH       = "FOREACH"
  NONE          = "NONE"
  ADD           = "ADD"
  INCLUDE       = "INCLUDE"
  DEFINE        = "DEFINE"
  POWER         = "POWER"

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
  def __init__(self, token, name, node, args):
    self.token = token
    self.name = name
    self.node = node
    self.args = args

class FncCall(AST):
  def __init__(self, token, name, args):
    self.token = token
    self.name = name
    self.args = args
    self.value = None

class PythonFunc(AST):
  def __init__(self, token, name, func):
    self.token = token
    self.name = name
    self.func = func
    self.args = list(func.__code__.co_varnames)[1:]

class PythonFuncCall(AST):
  def __init__(self, token, func, args):
    self.token = token
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
  def __init__(self, token, condition, consequences, alternatives):
    self.token = token
    self.condition = condition
    self.consequences = consequences
    self.alternatives = alternatives

class For_St(AST):
  def __init__(self, token, initial, condition, everyiter, statements):
    self.token = token
    self.initial = initial
    self.condition = condition
    self.everyiter = everyiter # statement to run after every iteration
    self.statements = statements

class While_St(AST):
  def __init__(self, token, condition, statements):
    self.token = token
    self.condition = condition
    self.statements = statements

class Times_St(AST):
  def __init__(self, token, times, statements, _as = None):
    self.token = token
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

class Foreach_St(AST):
  def __init__(self, token, pointer, llist, statements):
    self.token = token
    self.pointer = pointer
    self.llist = llist
    self.statements = statements

class None_Type(AST):
  pass

class Add(AST):
  def __init__(self, left, op, right):
    self.left = left
    self.token = self.op = op
    self.right = right

class Include(AST):
  def __init__(self, token):
    self.token = token
    self.incfile = token.value

class Unique(AST): # str but not equal to str
  def __init__(self, value):
    self.value = value
    
  def __str__(self):
    return self.value

class Define(AST):
  def __init__(self, token):
    self.token = token
    self.value = Unique(token.value)
    
  def __str__(self):
    return str(self.value)

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
  
  def setAttr(self, root, var, val):
    # This function will not be available in QoLang, so we can just don't care about VarFnc.
    if callable(val):
      added = PythonFunc(Token(Tokens.FUNC, f"{root}.{var}", 0, 0), f"{root}.{var}", val)
    else:
      added = VarVal(f"{root}.{var}", val)
    self.setVar(added)
  
  def hasAttr(self, root, var):
    for vvar in self.vars:
      if vvar.name.split('.') == [root, var]:
        return True
    return False
  
  def hasAnyAttr(self, root):
    for vvar in self.vars:
      if '.' in vvar.name and vvar.name.split('.')[0] == root:
        return True
    return False
  
  def exists(self, root):
    for var in self.vars:
      if var.name == name:
        return True
    return False
  
  def remove(self, root):
    i = 0
    for vvar in self.vars:
      if vvar.name == root or ('.' in vvar.name and vvar.name.split('.')[0] == root):
        del self.vars[i]
      i += 1
  
  def move(self, source, newname):
    i = 0
    for vvar in self.vars:
      if vvar.name == source:
        vvar.name = newname
      elif '.' in vvar.name and vvar.name.split('.')[0] == source:
        vvar.name = newname + '.' + '.'.join(vvar.name.split('.')[1:])
      i += 1

#endregion
