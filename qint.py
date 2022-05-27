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
      case Tokens.AND:
        return left and right
      case Tokens.OR:
        return left or right
  
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
    if node.left.token.type == Tokens.LISTITEM:
      llist = Variables.getVar(node.left.value)
      llist.value[self.visit(node.left.item)] = self.visit(node.right)
      Variables.setVar(llist)
    else:
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
    
    ret = 0
    for node in var.node.children:
      if isinstance(node, Return):
        return self.visit(node)
      else:
        self.visit(node)
    return node

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

    ret = None
    Variables, ret = node.func(Variables, args)
    return ret

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

  def visit_While_St(self, node):
    while self.visit(node.condition):
      for statement in node.statements:
        self.visit(statement)

  def visit_Times_St(self, node):
    global Variables
    for i in range(self.visit(node.times)):
      if node._as is not None:
        Variables.setVar(VarVal(node._as, i))
      for statement in node.statements:
        self.visit(statement)

  def visit_Fstring(self, node):
    result = ''
    for nod in node.nodes:
      match nod.type:
        case Tokens.STRING:
          result += nod.value
        case Tokens.ID:
          result += str(self.visit(Var(nod)).value)
    return result

  def visit_Return(self, node):
    return self.visit(node.value)

  def visit_List(self, node):
    return [self.visit(nnode) for nnode in node.values]

  def visit_ListItem(self, node):
    return Variables.getVar(node.value).value[self.visit(node.item)]

  def visit_Foreach_St(self, node):
    global Variables
    for item in self.visit(node.llist).value:
      Variables.setVar(VarVal(node.pointer, item))
      for statement in node.statements:
        self.visit(statement)

  def visit_None_Type(self, node):
    return None

  def visit_Add(self, node):
    if node.left.token.type == Tokens.LISTITEM:
      llist = Variables.getVar(node.left.value)
      llist.value[self.visit(node.left.item)] += self.visit(node.right)
      Variables.setVar(llist)
    else:
      var_old = Variables.getVar(node.left.value).value
      var_new = self.visit(node.right)
      var = VarVal(node.left.value, var_old + var_new)
      Variables.setVar(var)

  def interpret(self):
    tree = self.parser.parse()
    if tree is None:
      return ''
    return self.visit(tree)