def add_two(interactive):
    # raise Exception("Run Exception")
    name = interactive.get_string("Please enter your name.", "Your Name")
    interactive.print("You entered {}.".format(name))
    interactive.confirm_yes_no("Is that correct?")

def script_main(api_broker):
    interactive = api_broker.get_interactive(version="1")
    add_two(interactive)

# // parse error
