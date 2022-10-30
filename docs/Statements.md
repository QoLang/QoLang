# Operators - QoLang Documentation

Categories:
* [Assignment Statements](#assigment-statements)

## Assignment Statements
There are two types of assignment statements: Basic Assigment Statements and Augmented Assignment Statements.
Currently, there are no other types of assignment statements, but Chained Assignment Statements and Parallel Assignment Statements are planned to be added before the first stable release.

### Basic Assignment Statements
Basic Assignment Statements are used to assign a value to a variable.
The syntax is as follows:
```
variable = value;
```

Example code:
```
a = 5;
b = 10;
c = a + b;
```

### Augmented Assignment Statements
Augmented Assignment Statements are used to assign a value to a variable, but the value is calculated using an operator.
The syntax is as follows:
```
variable operator= value;
```

Example code:
```
a = 5;
b = 10;
c = 0;

c += a + b;
```

Note that only `+=` and `-=` are supported in version 0.8.5, but `*=`, `/=` and `%=` have been added in version 0.9.

## Call Statements
Call Statements are used to call a function.
The syntax is as follows:
```
function(arguments);
```

Example code:
```
println("Hello, World!");
```

## Conditional Statements
Conditional Statements are used to execute a block of code if a condition is met.
The syntax is as follows:
```
if (condition) {
    # Code
}
```

Note that there had to be a semi-colon (`;`) after the statement, but this has been removed in version 0.9.
*This applies for all block statements.*

Example code:
```
a = 5;
b = 10;

if (a > b) {
    println("a is bigger than b");
}
```

### Else Statements
Else Statements are used to execute a block of code if a condition is not met.
The syntax is as follows:
```
if (condition) {
    # Code
} else {
    # Code
}
```

Example code:
```
a = 5;
b = 10;

if (a > b) {
    println("a is bigger than b");
} else {
    println("b is bigger than a");
}
```

### Else If Statements
Multiple Else Statements can be chained together using Else If Statements.
The syntax is as follows:
```
if (condition) {
    # Code
} else if (condition) {
    # Code
} else {
    # Code
}
```

Example code:
```
a = 5;
b = 10;

if (a > b) {
    println("a is bigger than b");
} else if (a == b) {
    println("a is equal to b");
} else {
    println("b is bigger than a");
}
```

## Loop Statements
Loop Statements are used to execute a block of code multiple times.

### For Loop Statements
For Loop Statements are used to run an initialization statement, then rerun the block of code until the condition is not met and run a step statement at every iteration.

The syntax is as follows:
```
for (initialization; condition; step) {
    # Code
}
```

Example code:
```
for (i = 0; i < 10; i += 1) {
    println(i);
}
```

### While Loop Statements
While Loop Statements are used to rerun the block of code until the condition is not met.

The syntax is as follows:
```
while (condition) {
    # Code
}
```

Example code:
```
i = 0;

while (i < 10) {
    println(i);
    i += 1;
}
```

### Times Statements
Times Statements are used to rerun the block of code a specified amount of times, while optionally
keeping track of the current iteration.

The syntax is as follows:
```
times amount {
    # Code
}
/* or */
times amount as &pointer {
    # Code
}
```

Example code:
```
times 10 {
    println("Hello, World!");
}

times 10 as &i {
    println(i);
}
```

### Foreach Statements
Foreach Statements are used to rerun the block of code for every element in an array.

The syntax is as follows:
```
foreach &pointer in array {
    # Code
}
```

Example code:
```
array = [1, 2, 3, 4, 5];

foreach &i in array {
    println(i);
}
```

## Special Statements
Special Statements have varying uses.

### Compound Statements
Compound Statements have no difference in the program, but they can be used to group statements together.

The syntax is as follows:
```
{
    # Code
}
```

Example code:
```
{
    a = 5;
    b = 10;
    c = a + b;
}
```

### Function Declaration Statements
Function Declaration Statements are used to declare a function.

The syntax is as follows:
```
function name(arguments) {
    # Code
}
```

Example code:
```
function sayhi() {
    println("Hello, World!");
}
```

### Return Statements
Return Statements are used to return a value from a function.

The syntax is as follows:
```
return value;
```

Example code:
```
function add(a, b) {
    return a + b;
}
```

### Include Statements
Include Statements are used to include a file or library.

The syntax is as follows:
```
include library;
```

Example code:
```
include types;
```

### Define Statements
Define Statements are used to define a variable that has no value but is different than everything else.

The syntax is as follows:
```
define variable;
```

Example code:
```
define a;
println(a);        # Prints "a"
println(a == "a"); # Prints "false"
```
