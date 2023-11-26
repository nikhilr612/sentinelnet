import matplotlib.pyplot as plt
import numpy as np
import time

# TODO change to other library with support with gui
class RealTimePlot:
    def __init__(self, num_subplots=2):
        self.num_subplots = num_subplots
        self.x_data = [np.linspace(0, 10, 100), np.linspace(0, 10, 100)]
        self.y_data = [np.sin(self.x_data[0]), np.cos(self.x_data[1])]
        self.is_running = True

        # Set up the subplots
        plt.ion()  # Turn on interactive mode
        self.fig, self.axes = plt.subplots(num_subplots, 1, sharex=True)

        # Initialize lines for each subplot
        self.lines = [ax.plot(x_data, y_data)[0]
                      for ax, y_data, x_data in zip(self.axes, self.y_data, self.x_data)]

        # Register the event handler for window close event
        self.fig.canvas.mpl_connect('close_event', self.on_close)

    def update(self):
        for line, y_data in zip(self.lines, self.y_data):
            line.set_ydata(y_data)

        plt.xlabel('X-axis')
        plt.title('Real-time Plot')
        plt.pause(0.1)

    def on_close(self, event):
        print("Plotting stopped by closing the window")
        self.is_running = False

    def run(self):
        try:
            while self.is_running:
                self.x_data[0] += 0.1
                self.x_data[1] += 0.1
                self.y_data = [np.sin(self.x_data[0]), np.cos(self.x_data[1])]
                self.update_plot()
        except KeyboardInterrupt:
            pass

        plt.show()


if __name__ == '__main__':
    real_time_plot = RealTimePlot(num_subplots=2)
    real_time_plot.run()
