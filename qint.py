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
        return str(left < right)
      case Tokens.GREATER_THAN:
        return str(left > right)
      case Tokens.EQUAL:
        return str(left == right)
      case Tokens.LESS_EQUAL:
        return str(left <= right)
      case Tokens.GREATER_EQUAL:
        return str(left >= right)
      case Tokens.NOT_EQUAL:
        return str(left != right)
  
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
    Variables.setVar(node)

  def visit_FncCall(self, node):
    var = Variables.getVar(node.name)
    if var is None:
      raise Exception("Function not found")
    if not len(node.args) == len(var.args):
      raise Exception(f"Expected {str(len(node.args))} args, got {str(len(var.args))}")
    
    i = 0
    for arg in node.args:
      nvar = VarVal(var.args[i].value, arg.token)
      Variables.setVar(nvar)
      i += 1
    
    nnode = self.visit(var.node)
    return nnode

  def visit_BuiltinFuncCall(self, node):
    global Variables
    args = []
    i = 0
    for arg in node.args:
      args += [self.visit(arg)]
      i += 1

    Variables = node.func(Variables, args)

  def visit_String(self, node):
    return node.value

  def visit_Boolean(self, node):
    return node.value

  def visit_Pointer(self, node):
    return node.value

  def interpret(self):
    tree = self.parser.parse()
    if tree is None:
      return ''
    return self.visit(tree)