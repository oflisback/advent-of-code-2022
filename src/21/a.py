lines = open("input.txt").read().splitlines()
from collections import defaultdict

values = {}
subscriptions = defaultdict(lambda: [])
resolution_stack = []


def expression_is_resolved(expression):
    parts = expression.split(" ")
    return all(value.isdigit() for value in [parts[0], parts[2]])


for line in lines:
    line = line.replace("/", "//")
    [name, expression] = line.split(":")
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
    print("Applying resolution for: ", resolved_name)
    value = resolution["value"]
    values[resolved_name] = value
    print("Subscribers: ", subscriptions[resolved_name])
    for subscription in subscriptions[resolved_name]:
        expression = subscription["expression"]
        expression_symbol = subscription["name"]
        print("Replacing ", resolved_name, " in ", expression)
        expression = expression.replace(resolved_name, str(value))
        if expression_is_resolved(expression):
            print("Expression", expression_symbol, "is resolved")
            resolution_stack.append(
                {"name": expression_symbol, "value": eval(expression)}
            )
            subscriptions[resolved_name].remove(subscription)
        else:
            print("Expression", expression, "is not yet fully resolved")
            subscription["expression"] = expression


print(values)
