"""
BiIter(Biderectional Iterator) ->
"""
import abc

class BiIterIndex :
    def __init__(self, end, start=0) :
        ## start_with - 1 so that first call to next(+1) returns start
        self.cur = start - 1
        self.end = end

    def next(self, direction=1) :
        self.cur = (self.cur + direction) % self.end
        return self.cur



class BiIterB :
    """ B -> using builtins `len` and `[]`"""
    def __init__(self, data: list, start_index=0) :
        """
        | data must be able to
        | len(data)
        | data[index: int]

        | direction of first call should be 1
        """
        self.data = data
        self.index_iter = BiIterIndex(len(self.data), start=start_index)

    def next(self, direction=1) :
        """ direction = +/-1 """
        return self.data[self.index_iter.next(direction)]



class BiIterM :
    """ M -> using methods `get_max()` and `iget()`"""
    def __init__(self, data, start_index=0) :
        """ data must have functions get_max() and iget(index: int) """
        self.data = data
        self.index_iter = BiIterIndex(self.data.get_max(), start=start_index)

    def next(self, direction=1) :
        """ direction = +/-1 """
        return self.data.iget(self.index_iter.next(direction))



class BiIterB_MixIn(metaclass=abc.ABCMeta) :
    """ B -> using builtins `len` and `[]`"""
    def __init__(self, start_index=0) :
        """
        | data must be able to
        | len(data)
        | data[index: int]

        | direction of first call should be 1
        """
        #self.data = data
        self.index_iter = BiIterIndex(len(self), start=start_index)

    def next(self, direction=1) :
        """ direction = +/-1 """
        return self[self.index_iter.next(direction)]


    @abc.abstractmethod
    def __len__(self) :
        pass

    @abc.abstractmethod
    def __getitem__(self, index) :
        pass



class BiIterM_MixIn(metaclass=abc.ABCMeta) :
    """ M -> using methods `get_max()` and `iget()`"""
    def __init__(self, start_index=0) :
        """ data must have functions get_max() and iget(index: int) """
        self.index_iter = BiIterIndex(self.get_max(), start=start_index)

    def next(self, direction=1) :
        """ direction = +/-1 """
        return self.iget(self.index_iter.next(direction))

    @abc.abstractmethod
    def get_max(self) :
        """
        should return the max possible index + 1

        """
        pass

    @abc.abstractmethod
    def iget(self, index) :
        """
        should return the element/object at that index
        """
        pass


class BiIter(metaclass=abc.ABCMeta) :
    @abc.abstractmethod
    def next(self, direction=1) :
        pass
