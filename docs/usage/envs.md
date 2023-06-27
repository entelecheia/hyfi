# Environment variables

## Utils

Here's an example of how you can use the expand_posix_vars function in a Python script:

```python
from hypi.utils.envs import ENVs

# Define a POSIX expression with variables
posix_expr = "The current working directory is $PWD and the user is $USER."

# Call the expand_posix_vars function with the POSIX expression
expanded_expr = ENVs.expand_posix_vars(posix_expr)

# Print the expanded expression
print(expanded_expr)
```

In this example, we import the `expand_posix_vars` function from the env module. We then define a POSIX expression with two variables, `$PWD` and `$USER`. We call the `expand_posix_vars` function with the POSIX expression as an argument, which expands the variables using the current working directory and the current user. Finally, we print the expanded expression, which should output something like:

```bash
The current working directory is /home/user and the user is user.
```

You can also pass in a dictionary of additional variables to be used in the expansion, like this:

```python
from hypi.utils.envs import ENVs

# Define a POSIX expression with variables
posix_expr = "The value of MY_VAR is $MY_VAR."

# Define a dictionary of additional variables
context = {"MY_VAR": "hello world"}

# Call the expand_posix_vars function with the POSIX expression and context
expanded_expr = ENVs.expand_posix_vars(posix_expr, context)

# Print the expanded expression
print(expanded_expr)
```

In this example, we define a POSIX expression with a single variable, `$MY_VAR`. We also define a dictionary of additional variables with a key of `MY_VAR` and a value of hello world. We call the `expand_posix_vars` function with the POSIX expression and context as arguments, which expands the `$MY_VAR` variable to hello world. Finally, we print the expanded expression, which should output:

```bash
The value of MY_VAR is hello world.
```
