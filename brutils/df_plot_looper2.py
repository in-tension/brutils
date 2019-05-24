import matplotlib
from matplotlib import pyplot as plt
from matplotlib.widgets import Button

class DfPlotLooper2 :
    """subclasses can override `plot` function and change how the group(df) is plotted"""

    DEFAULTS = {'next_button_loc' : [0.7, 0.05, 0.1, 0.075],
                'prev_button_loc' : [0.81, 0.05, 0.1, 0.075],
                'figsize' : [10, 5],
                'xlim' : [0, 120],
                'ylim' : [-1, 100]}

    @staticmethod
    def init_with_df(self, df, group_by_col,  x_name, y_name, title_col=None, override_defaults=None) :

        grouped_df = df.groupby(group_by_col)
            # self.group_by_col = group_by_col
        return DfPlotLooper2(grouped_df, x_name, y_name, title=None, override_defaults=None, some_condition=None)


    # def __init__(self, grouped_df, x_name, y_name, title_col=None, override_defaults=None) :
    def __init__(self, grouped_df, x_name, y_name, title=None, override_defaults=None, some_condition=None) :
        """
            | :param: override_defaults : `dict` with keys of settings to override and the desired values
            | :param: some_condition : a function which takes the `cur_group()` and returns False if it should not be plotted and `incr`/`decr` should be called again,
            | when equal None, doesn't do the test and plots every group
        """

        self.settings = DfPlotLooper2.DEFAULTS
        if override_defaults != None :
            for key in override_defaults :
                self.settings[key] = override_defaults[key]

        # self.df = df
        self.grouped_df = grouped_df
        self.group_names = list(self.grouped_df.groups.keys())
        self.ind = 0
        self.max_ind = len(self.group_names)

        self.x_name = x_name
        self.y_name = y_name
        self.title = title
        self.some_condition = some_condition


        # self.fig = plt.figure(figsize=self.settings['figsize'],tight_layout=True)
        self.fig = plt.figure(figsize=self.settings['figsize'])#,tight_layout=True)
        if self.title != None :
            self.fig.suptitle(self.title)
        self.fig.show()

        #self.ax = plt.gca()

        self.ax_prev = plt.axes(self.settings['next_button_loc'])
        self.ax_next = plt.axes(self.settings['prev_button_loc'])
        self.b_next = Button(self.ax_next, 'Next')
        self.b_prev = Button(self.ax_prev, 'Prev')
        self.b_next.on_clicked(self.next)
        self.b_prev.on_clicked(self.prev)

        self.b_next.set_visible(False)

        try :
            matplotlib.rcParams['keymap.back'].remove('left')
            matplotlib.rcParams['keymap.forward'].remove('right')
        except Exception : pass
        self.fig.canvas.mpl_connect("key_press_event", self.on_key_press)

        self.plot()

        # plt.show() # I think this might prevent python interpreter from closing
                    # also prevents interactive interpreter from continuing
                    # comment out if using -i

    # def sub_class_init(self) :
    #     pass]
    def plot(self) :
        ax = plt.gca()
        ax.cla()

        ax.set_title("{} : {}".format(self.group_by_col, self.group_names[self.ind]))

        self.cur_group().plot(self.x_name, self.y_name, kind='scatter', ax=ax)

        ax.set_xlim(self.settings['xlim'])
        ax.set_ylim(self.settings['ylim'])
        plt.draw()
        # plt.show()



    def next(self, event):
        print('next()')
        self.incr()
        self.test_for(1)
        self.plot()

    def prev(self, event):
        print('prev()')
        self.decr()
        self.test_for(-1)
        self.plot()

    def on_key_press(self, event) :
        print('on_key_press()')
        if event.key == "left":
            self.prev(event)
        elif event.key == "right":
            self.next(event)

    def incr(self) :
        """increase ind"""
        self.ind += 1
        if self.ind >= self.max_ind :
            self.ind = 0

    def decr(self) :
        """decrease ind"""
        self.ind -= 1
        if self.ind < 0 :
            self.ind = self.max_ind - 1

    def test_for(self, direct):
        # some_condition = False  # replace False with some condition such as num of data point inside cur_group
        if self.some_condition == None :
            return
        if direct == 1:
            while not self.some_condition(self.cur_group()) :
                self.incr()
        elif direct == -1:
            while not self.some_condition(self.cur_group()) :
                self.decr()

    def cur_group(self) :
        return self.grouped_df.get_group(self.group_names[self.ind])

    def cur_group_col(self, col_name) :
        return self.cur_group()[col_name]

    def __str__(self) :
        if self.title == None :
            return 'DfPlotLooper : ' + str(self.group_names)
        else :
            return '{} (DfPlotLooper1 : {}'.format(self.title, str(self.group_names))


