import suslib

while True:
  try:
    expression = input("> ")
  except EOFError:
    break
  lexer = suslib.Lexer(expression)
  parser = suslib.Parser(lexer)
  interpreter = suslib.Interpreter(parser)
  print(interpreter.visit(parser.parse()))