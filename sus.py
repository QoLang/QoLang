import suslib

while True:
  try:
    expression = input("> ")
  except EOFError:
    break
  lexer = suslib.Lexer(expression)
  interpreter = suslib.Interpreter(lexer)
  print(interpreter.expr())