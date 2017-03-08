def add_three(interactive):
    n1 = interactive.get_integer("Please enter a number.", 1)
    interactive.print("You entered {}.".format(n1))
    n2 = interactive.get_integer("Please enter another number.", 2)
    interactive.print("You entered {}.".format(n2))
    n3 = interactive.get_integer("Please enter the last number.", 3)
    interactive.print("You entered {}.".format(n3))
    interactive.print("The sum is {}.".format(n1 + n2 + n3))

def script_main(api_broker):
    interactive = api_broker.get_interactive(version="1")
    add_three(interactive)
