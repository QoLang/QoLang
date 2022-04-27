import suslib

while True:
  try:
    expression = input("> ")
  except EOFError:
    break
  interpreter = suslib.Interpreter(expression)
  print(interpreter.expr())