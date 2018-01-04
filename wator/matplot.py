import matplotlib.pyplot
from wator import WaTor

def print_plot():
    """
    Print graphs while simulation is running on.
    
    :return: ``None``
    """

    with open('wator/gui/simulations/logmatplot.txt', 'r+') as f:
        lines = f.readlines()
    x = [line.split()[0] for line in lines]
    y = [line.split()[1] for line in lines]
    a = [line.split()[2] for line in lines]
    b = [line.split()[3] for line in lines]


    fig = pyplot.figure()

    ax1 = fig.add_subplot(111)
    
    ax1.set_title("xxx")    
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Count')
    
    ax1.subplot(x, y, c='r', label='Actual')
    ax1.bar(a, b, c='r', label='Optimalization')
    
    leg = ax1.legend()
    
    pyplot.show()
