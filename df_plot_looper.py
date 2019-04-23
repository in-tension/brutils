import matplotlib
from matplotlib import pyplot as plt
from matplotlib.widgets import Button

class DfPlotLooper :

    def __init__(self, grouped_df, x_name, y_name, title_col=None) :
        self.grouped_df = grouped_df
        self.group_names = list(self.grouped_df.groups.keys())
        self.ind = 0
        self.max_ind = len(self.group_names)



        self.x_name = x_name
        self.y_name = y_name
        self.title_col = title_col



        self.fig = plt.figure(figsize=(10, 5))
        self.fig.show()

        self.ax = plt.gca()
        print('okay')



        ax_prev = plt.axes([0.7, 0.05, 0.1, 0.075])
        ax_next = plt.axes([0.81, 0.05, 0.1, 0.075])

        self.b_next = Button(ax_next, 'Next')
        self.b_prev = Button(ax_prev, 'Prev')
        self.b_next.on_clicked(self.next)
        self.b_prev.on_clicked(self.prev)

        matplotlib.rcParams['keymap.back'].remove('left')
        matplotlib.rcParams['keymap.forward'].remove('right')

        self.fig.canvas.mpl_connect("key_press_event", self.on_key_press)

        self.plot()
        plt.show() # I think this might prevent python interpreter from closing
                    # also prevents interactive interpreter from continuing
    def plot(self) :

        print('plot')
        self.ax.cla()

        if self.title_col == None :
            self.ax.set_title("Group {}".format(self.ind))
        else :
            #self.ax.set_title("{} : {}".format(self.title_col, self.cur_group_col(self.title_col)[0]))
            self.ax.set_title("{} : {}".format(self.title_col, self.group_names[self.ind]))
        # print(self.cur_group_col(self.title_col))

        # print(self.x_name)
        # print(self.y_name)
        # plt.plot([1,2,3],[1,2,3])
        # print(self.cur_group())
        self.cur_group().plot(self.x_name, self.y_name, kind='scatter', ax=self.ax)

        self.ax.set_xlim(0, 120)
        self.ax.set_ylim(-1, 100)
        plt.draw()
        plt.show()


    def incr(self) :
        print('incr, ind=' + str(self.ind))
        self.ind += 1
        if self.ind >= self.max_ind :
            self.ind = 0
        print('ind=' + str(self.ind))


    def decr(self) :
        self.ind -= 1
        if self.ind <= 0 :
            self.ind = self.max_ind


    def test_for(self,direct) :
        some_condition = False      # replace False with some condition such as num of data point inside cur_group
        if direct == 1 :
            while some_condition :
                self.incr()
        elif direct == -1 :
            while some_condition :
                self.decr()


    def on_key_press(self, event) :
        if event.key == "left":
            self.next(self, event)
        elif event.key == "right":
            self.prev(self, event)

    def next(self, event):
        self.incr()
        self.test_for(1)

        print('next, ind={}'.format(self.ind))

        self.plot()

    def prev(self, event):
        print('prev, ind={}'.format(self.ind))
        self.decr()
        self.test_for(-1)

        self.plot()

    def cur_group(self) :
        return self.grouped_df.get_group(self.group_names[self.ind])

    def cur_group_col(self, col_name) :
        return self.cur_group()[col_name]

    def __str__(selfs) :
        pass


