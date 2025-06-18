import random

OPERATOR = ["+", "-", "/", "*"]

def generate_expression(min, max):
    left = random.randint(min, max)
    right = random.randint(min, max)
    operator = random.choice(OPERATOR)

    expr = str(left) + " " + operator + " " + str(right)
    result = eval(expr)
    return expr, result

min_operand = int(input("Enter min operand: "))
max_operand = int(input("Enter max operand: "))
expr, result = generate_expression(min_operand, max_operand)
print(expr, "=", result)