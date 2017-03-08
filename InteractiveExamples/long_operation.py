import time

def long_operation(interactive):
    interactive.print("Starting long operation.")
    for i in range(200):
        time.sleep(1)
        interactive.print("Tick " + str(i))
        if interactive.cancelled:
            break

def script_main(api_broker):
    interactive = api_broker.get_interactive(version="1")
    long_operation(interactive)
