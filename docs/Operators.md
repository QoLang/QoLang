# Operators - QoLang Documentation

Categories:
* [Logical Operators](#logical-operators)
* [Comparison Operators](#comparison-operators)
* [Arithmetic Operators](#arithmetic-operators)

## Logical Operators
### `&&` operator ("and")
Returns `True` if both statements are `True`.

Example code:
```
a = True;
b = False;

println(a && b);

b = True;

println(a && b);
```
Output:
```
False
True
```

### `||` operator ("or")
Returns `True` if at least one of the statements are `True`.

Example code:
```
a = True;
b = False;

println(a || b);

a = False;

println(a || b);
```
Output:
```
True
False
```

### `??` operator ("TIN" or "This if not")
When used as a binary operator, returns the right value if the left value is `None`.
When used as an unary operator, returns the first non-None value from the list.

Example code:
```
a = [None, None, None, 74, 53];

println(??a);

a = None;
b = 13;

println(a ?? b);

a = 42;

println(a ?? b);
```
Output:
```
74
13
42
```

*New in 0.9*

## Comparison Operators
### `<` operator ("less than")
Returns `True` if left statement is smaller than the right one.

Example code:
```
a = 20;
b = 10;

println(a < b);

a = 5;

println(a < b);
```
Output:
```
False
True
```

### `>` operator ("greater than")
Returns `True` if left statement is bigger than the right one.

Example code:
```
a = 20;
b = 10;

println(a > b);

a = 5;

println(a > b);
```
Output:
```
True
False
```

### `==` operator ("equal to")
Returns `True` if left statement is equal to the right one.

Example code:
```
a = 20;
b = 10;

println(a == b);

a = 10;

println(a == b);
```
Output:
```
False
True
```

### `<=` operator ("less or equal")
Returns `True` if left statement is equal to/less than the right one.

Example code:
```
a = 5;
b = 10;

println(a <= b);

a = 20;

println(a <= b);
```
Output:
```
True
False
```

### `>=` operator ("greater or equal")
Returns `True` if left statement is equal to/greater than the right one.

Example code:
```
a = 5;
b = 10;

println(a >= b);

a = 20;

println(a >= b);
```
Output:
```
False
True
```

### `!=` operator ("not equal")
Returns `True` if left statement is not equal to the right one.

Example code:
```
a = 5;
b = 10;

println(a != b);

a = 10;

println(a != b);
```
Output:
```
True
False
```

## Arithmetic Operators
### `+` operator ("plus")
Adds two numbers.

Example code:
```
println(20 + 22);
```
Output:
```
42
```

### `-` operator ("minus")
Subtracts the value on right from the value on left.

Example code:
```
println(47 - 36);
```
Output:
```
11
```

### `*` operator ("multiply")
Multiplies two numbers.

Example code:
```
println(5 * 46);
```
Output:
```
230
```

### `/` operator ("divide")
Divides the value on left by the value on right.

Example code:
```
println(91 / 13);
```
Output:
```
7.0
```

### `**` operator ("exponentiation")
Returns the left value to the power of the right value.

Example code:
```
println(2 ** 20);
```
Output:
```
1048576
```

### `%` operator ("modulus")
Returns the remainer from the division of the left value by the right value.

Example code:
```
println(75427 % 4424);
```
Output:
```
219
```
