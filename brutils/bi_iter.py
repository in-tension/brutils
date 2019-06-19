"""
BiIter(Biderectional Iterator) ->
"""


class BiIterIndex :
    def __init__(self, end, start=0) :
        ## start_with - 1 so that first call to next(+1) returns start
        self.cur = start - 1
        self.end = end

    def next(self, direction=1) :
        self.cur = (self.cur + direction) % self.end
        return self.cur



# class BiIter :
#
#     def __init__(self, data, start_index=0, get_max=__len__, iget=__getitem__) :
#
#         self.data = data
#         self.index_iter = BiIterIndex(self.data.get_max(), start=start_index)
#
#     def next(self, direction=1) :
#         """ direction = +/-1 """
#         return self.data.iget(self.index_iter.next(direction))


class BiIterSeq :

    def __init__(self, data, start_index=0) :
        self.data = data
        self.index_iter = BiIterIndex(len(self.data), start=start_index)

    def next(self, direction=1) :
        """ direction = +/-1 """
        return self.data[self.index_iter.next(direction)]

class BiIterFunc :
    def __init__(self, data, get_max, iget, start_index=0) :
        self.data = data
        max_index = self.data.get_max()
        self.index_iter = BiIterIndex(max_index, start=start_index)
        self.iget = iget

    def next(self, direction=1) :
        """ direction = +/-1 """
        return self.iget(self.index_iter.next(direction))



class TestClass :

    def __init__(self, data) :
        self.data = data

    def a(self) :
        return len(self.data)

    def b(self, index) :
        return self.data[index]

l = [x*x for x in range(20)]

tc = TestClass(l)

b = BiIterFunc(tc, a, b)