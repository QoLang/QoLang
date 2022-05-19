from qclasses import *

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
        return left < right
      case Tokens.GREATER_THAN:
        return left > right
      case Tokens.EQUAL:
        return left == right
      case Tokens.LESS_EQUAL:
        return left <= right
      case Tokens.GREATER_EQUAL:
        return left >= right
      case Tokens.NOT_EQUAL:
        return left != right
  
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
    global Variables
    Variables.setVar(node)

  def visit_FncCall(self, node):
    var = Variables.getVar(node.name)
    if var is None:
      var = Variables.getVar("func_" + node.name)
      if var is None:
        raise Exception("Function not found")
      else:
        var = BuiltinFuncCall(var.func, node.args)
        return self.visit(var)
    if not len(node.args) == len(var.args):
      raise Exception(f"Expected {str(len(node.args))} args, got {str(len(var.args))}")
    
    i = 0
    for arg in node.args:
      toadd = arg
      if isinstance(arg, Var):
        toadd = Variables.getVar(arg.value).value
      nvar = VarVal(var.args[i].value, toadd)
      Variables.setVar(nvar)
      i += 1
    
    nnode = self.visit(var.node)
    return nnode

  def visit_BuiltinFuncCall(self, node):
    global Variables
    args = []
    i = 0
    for arg in node.args:
      toadd = self.visit(arg)
      if isinstance(toadd, VarVal):
        toadd = toadd.value
      args += [toadd]
      i += 1

    Variables = node.func(Variables, args)

  def visit_String(self, node):
    return node.value

  def visit_Boolean(self, node):
    return node.value

  def visit_Pointer(self, node):
    return node.value

  def visit_If_St(self, node):
    if self.visit(node.condition) == True:
      for statement in node.consequences:
        self.visit(statement)
    else:
      for statement in node.alternatives:
        self.visit(statement)

  def visit_For_St(self, node):
    self.visit(node.initial)
    while self.visit(node.condition):
      for statement in node.statements:
        self.visit(statement)
      self.visit(node.everyiter)

  def interpret(self):
    tree = self.parser.parse()
    if tree is None:
      return ''
    return self.visit(tree)