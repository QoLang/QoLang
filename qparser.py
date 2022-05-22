from qclasses import *

class Parser:
  def __init__(self, lexer):
    self.lexer = lexer
    self.current_token = self.lexer.next_token()
    self.next_token = self.lexer.next_token()
  
  def error(self):
    raise Exception(f'Syntax error, token: {str(self.current_token)}')

  def get_next_token(self):
    current_token = self.next_token
    self.next_token = self.lexer.next_token()
    return current_token

  def eat(self, token_type):
    if self.current_token.type == token_type:
      self.current_token = self.get_next_token()
    else:
      raise Exception(f'Syntax error: Expected {str(token_type)} but found {str(self.current_token)}')

  def factor(self):
    token = self.current_token
    match token.type:
      case Tokens.PLUS:
        self.eat(Tokens.PLUS)
        return UnaryOp(token, self.factor())
      case Tokens.MINUS:
        self.eat(Tokens.MINUS)
        return UnaryOp(token, self.factor())
      case Tokens.INTEGER:
        self.eat(Tokens.INTEGER)
        return Num(token)
      case Tokens.LPAREN:
        self.eat(Tokens.LPAREN)
        node = self.expr()
        self.eat(Tokens.RPAREN)
        return node
      case Tokens.STRING:
        self.eat(Tokens.STRING)
        return String(token)
      case Tokens.TRUE:
        self.eat(Tokens.TRUE)
        return Boolean(token)
      case Tokens.FALSE:
        self.eat(Tokens.FALSE)
        return Boolean(token)
      case Tokens.POINTER:
        self.eat(Tokens.POINTER)
        return Pointer(token)
      case Tokens.FSTRING:
        self.eat(Tokens.FSTRING)
        return Fstring(token)
      case Tokens.FUNCCALL:
        node = self.fnccall()
        return node
      case Tokens.SBRACKETL:
        node = self.list()
        return node
      case _:
        node = self.variable()
        return node

  def term(self):
    node = self.factor()

    while self.current_token.type in (Tokens.MULTIPLY, Tokens.DIVIDE):
      token = self.current_token
      match token.type:
        case Tokens.MULTIPLY:
          self.eat(Tokens.MULTIPLY)
        case Tokens.DIVIDE:
          self.eat(Tokens.DIVIDE)
      node = BinOp(node, token, self.factor())
    
    return node

  def expr(self):
    return self.mulrel()

  def mulrel(self):
    node = self.relation()
    if self.current_token.type in (Tokens.AND, Tokens.OR):
      token = self.current_token
      match self.current_token.type:
        case Tokens.AND:
          self.eat(Tokens.AND)
        case Tokens.OR:
          self.eat(Tokens.OR)
      node = BinOp(node, token, self.relation())
    return node
  
  def relation(self):
    node = self.arithmetic_expr()
    if self.current_token.type in (
      Tokens.LESS_THAN,
      Tokens.GREATER_THAN,
      Tokens.LESS_EQUAL,
      Tokens.GREATER_EQUAL,
      Tokens.EQUAL,
      Tokens.NOT_EQUAL,
    ):
      token = self.current_token
      match self.current_token.type:
        case Tokens.LESS_THAN:
          self.eat(Tokens.LESS_THAN)
        case Tokens.GREATER_THAN:
          self.eat(Tokens.GREATER_THAN)
        case Tokens.EQUAL:
          self.eat(Tokens.EQUAL)
        case Tokens.LESS_EQUAL:
          self.eat(Tokens.LESS_EQUAL)
        case Tokens.GREATER_EQUAL:
          self.eat(Tokens.GREATER_EQUAL)
        case Tokens.NOT_EQUAL:
          self.eat(Tokens.NOT_EQUAL)
      node = BinOp(left=node, op=token, right=self.arithmetic_expr())
    return node

  def arithmetic_expr(self):
    node = self.term()
    
    while self.current_token.type in (Tokens.PLUS, Tokens.MINUS, Tokens.MULTIPLY, Tokens.DIVIDE):
      token = self.current_token
      match token.type:
        case Tokens.PLUS:
          self.eat(Tokens.PLUS)
        case Tokens.MINUS:
          self.eat(Tokens.MINUS)
      node = BinOp(node, token, self.term())

    return node
  
  def program(self): # compound statement, without {}
    nodes = self.statement_list()
    root = Compound()
    for node in nodes:
      root.children.append(node)

    return root
  
  def compound_statement(self):
    self.eat(Tokens.BEGIN)
    nodes = self.statement_list()
    self.eat(Tokens.END)

    root = Compound()
    for node in nodes:
      root.children.append(node)

    return root
  
  def statement_list(self):
    node = self.statement()

    results = [node]

    while self.current_token.type == Tokens.SEMI:
      self.eat(Tokens.SEMI)
      results.append(self.statement())

    if self.current_token.type == Tokens.ID:
      self.error()
    
    if not isinstance(results[-1], NoOp):
      self.error()

    return results
  
  def statement(self):
    match self.current_token.type:
      case Tokens.BEGIN:
        node = self.compound_statement()
      case Tokens.ID:
        node = self.assignment_statement()
      case Tokens.FUNC:
        node = self.fncdec()
      case Tokens.FUNCCALL:
        node = self.fnccall()
      case Tokens.IF_ST:
        node = self.if_st()
      case Tokens.FOR_ST:
        node = self.for_st()
      case Tokens.WHILE_ST:
        node = self.while_st()
      case Tokens.TIMES_ST:
        node = self.times_st()
      case Tokens.RETURN:
        node = self._return()
      case _:
        node = self.empty()
    return node
    
  def assignment_statement(self):
    left = self.variable()
    token = self.current_token
    self.eat(Tokens.ASSIGN)
    right = self.expr()
    node = Assign(left, token, right)
    return node
  
  def variable(self):
    if self.next_token.type == Tokens.SBRACKETL:
      return self.listitem()
    node = Var(self.current_token)
    self.eat(Tokens.ID)
    return node

  def empty(self):
    return NoOp()
  
  def fncdec(self):
    self.eat(Tokens.FUNC)
    proc_name = self.current_token.value
    self.eat(Tokens.ID)
    self.eat(Tokens.LPAREN)

    if self.current_token.type == Tokens.ID:
      args = [self.variable()]
      while self.current_token.type == Tokens.COMMA:
        self.eat(Tokens.COMMA)
        args.append(self.variable())

    self.eat(Tokens.RPAREN)
    node = self.compound_statement()
    var = FncDec(proc_name, node, args)
    return var
  
  def fnccall(self):
    proc_name = self.current_token.value
    self.eat(Tokens.FUNCCALL)
    self.eat(Tokens.LPAREN)

    if self.current_token.type != Tokens.RPAREN:
      args = [self.expr()]
      while self.current_token.type == Tokens.COMMA:
        self.eat(Tokens.COMMA)
        toadd = self.expr()
        args.append(toadd)
    self.eat(Tokens.RPAREN)

    func = Variables.getVar(proc_name)
    var = None

    var = FncCall(proc_name, args)

    return var
  
  def if_st(self):
    if self.current_token.type == Tokens.IF_ST:
      self.eat(Tokens.IF_ST)                 # if
    else:                                    # *or*
      self.eat(Tokens.ELIF_ST)               # elif
    self.eat(Tokens.LPAREN)                  # (
    condition = self.expr()                  # condition
    self.eat(Tokens.RPAREN)                  # )
    consequences = self.compound_statement() # { code(); }

    alternatives = [] # else

    if (self.current_token.type == Tokens.ELSE_ST and self.next_token.type == Tokens.IF_ST) or self.next_token.type == Tokens.ELIF_ST:
      alternatives = [self.elif_st()]
    elif self.current_token.type == Tokens.ELSE_ST:
      alternatives = self.else_st()
    
    node = If_St(condition, consequences.children, alternatives)

    return node
  
  def elif_st(self):
    if self.current_token.type == Tokens.ELSE_ST:
      self.eat(Tokens.ELSE_ST)
    return self.if_st()
  
  def else_st(self):
    self.eat(Tokens.ELSE_ST)      # else
    self.eat(Tokens.BEGIN)        # {
    nodes = self.statement_list() # code();
    self.eat(Tokens.END)          # }
    return nodes

  def for_st(self):
    self.eat(Tokens.FOR_ST)
    self.eat(Tokens.LPAREN)
    init = self.statement()
    self.eat(Tokens.SEMI)
    condition = self.expr()
    self.eat(Tokens.SEMI)
    everyiter = self.statement()
    self.eat(Tokens.RPAREN)
    statements = self.compound_statement()

    node = For_St(init, condition, everyiter, statements.children)
    return node

  def while_st(self):
    self.eat(Tokens.WHILE_ST)
    self.eat(Tokens.LPAREN)
    condition = self.expr()
    self.eat(Tokens.RPAREN)
    statements = self.compound_statement()

    node = While_St(condition, statements.children)
    return node

  def times_st(self):
    self.eat(Tokens.TIMES_ST)
    times = self.arithmetic_expr()
    _as = None
    if self.current_token.type == Tokens.AS:
      self.eat(Tokens.AS)
      _as = self.current_token.value
      self.eat(Tokens.POINTER)
    statements = self.compound_statement()

    node = Times_St(times, statements.children, _as)
    return node

  def _return(self):
    token = self.current_token
    self.eat(Tokens.RETURN)
    value = self.expr()
    node = Return(token, value)
    return node

  def list(self):
    token = self.current_token
    self.eat(Tokens.SBRACKETL)

    result = []

    if self.current_token.type != Tokens.SBRACKETR:
      result = [self.expr()]
      while self.current_token.type == Tokens.COMMA:
        self.eat(Tokens.COMMA)
        result.append(self.expr())
    
    self.eat(Tokens.SBRACKETR)
    node = List(token, result)
    return node

  def listitem(self):
    token = self.current_token
    token.type = Tokens.LISTITEM
    self.eat(Tokens.LISTITEM)
    self.eat(Tokens.SBRACKETL)
    item = self.expr()    
    self.eat(Tokens.SBRACKETR)
    node = ListItem(token, item)
    return node

  def parse(self):
    node = self.program()

    if self.current_token.type != Tokens.EOF:
      self.error()
    
    return node