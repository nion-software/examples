import numpy

def show_data(interactive):
    interactive.alert("Ready?")
    data = numpy.random.randn(200, 200)
    interactive.show_ndarray(data, "Random")

def script_main(api_broker):
    interactive = api_broker.get_interactive(version="1")
    show_data(interactive)
