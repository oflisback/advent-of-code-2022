from sympy import *

lines = open("input.txt").read().splitlines()
from collections import defaultdict

values = {}
subscriptions = defaultdict(lambda: [])
resolution_stack = []


def expression_holds_humn(expression):
    if expression.find("humn") > -1:
        return True
    return False


def expression_is_resolved(expression):
    try:
        eval(expression)
        return True
    except:
        return False


for line in lines:
    #    line = line.replace("/", "//")
    if line.startswith("humn"):
        line = "humn: humn + 0"
    [name, expression] = line.split(":")
    print(name)
    expression = expression.strip()
    if expression.isdigit():
        resolution_stack.append({"name": name, "value": int(expression)})
    else:
        provider_expression = expression.split(" ")
        providers = [provider_expression[0], provider_expression[2]]
        subscription = {"name": name, "expression": expression}
        for provider in providers:
            subscriptions[provider].append(subscription)

while len(resolution_stack) > 0:
    resolution = resolution_stack.pop()
    resolved_name = resolution["name"]
    print("Applying resolution for: ", resolved_name, "which is", resolution["value"])
    value = resolution["value"]
    values[resolved_name] = value
    for subscription in subscriptions[resolved_name]:
        expression = subscription["expression"]
        expression_symbol = subscription["name"]
        expression = expression.replace(resolved_name, "(" + str(value) + ")")
        if expression_is_resolved(expression):
            print("Expression", expression_symbol, "is resolved")
            if expression_symbol == "root":
                print(expression)
            resolution_stack.append(
                {"name": expression_symbol, "value": eval(expression)}
            )
            subscriptions[resolved_name].remove(subscription)
        elif expression_holds_humn(expression):
            resolution_stack.append({"name": expression_symbol, "value": expression})
            if expression_symbol == "root":
                print(expression)
        else:
            print("Expression", expression, "is not yet fully resolved")
            subscription["expression"] = expression

root_expr = values["root"]
root_expr = root_expr.replace("zmpt", str(values["zmpt"]))
root_expr = root_expr.replace("nzjc", str(values["nzjc"]))
root_expr = root_expr.replace("smct", str(values["smct"]))

goal = 12133706805700

left = root_expr.replace(" + rqsg", "")
right = values["rqsg"]
humn = symbols("humn")
sol = solve(Eq(eval(left), right), (humn))
print(sol)
