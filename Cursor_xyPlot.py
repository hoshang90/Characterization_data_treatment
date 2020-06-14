class Cursor(object):
    def __init__(self, ax):
        self.ax = ax
        self.lx = ax.axhline(linewidth=1,color='r')  # the horiz line
        self.ly = ax.axvline(linewidth=1,color='r')  # the vert line

        # text location in axes coords
        self.txt = ax.text(0.7, 0.9, '', transform=ax.transAxes)

    def mouse_move(self, event):
        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata
        # update the line positions
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)

        self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))#right x and y value in the plot
        self.ax.figure.canvas.draw()