



from collections.abc import MutableMapping

class BaseDict(MutableMapping) :
    """
        a class with all the functionality of a `dict`
        but that can also be used as a parent class and all that functionality will be inherited

        defines the functions needed to use the `MutableMapping` mixin
        and other functions not defined with `MutableMapping` (like `__str__`)
        by calling the associated function of a `dict` attribute

        all functions
            from `BaseDict`
                `__init__(self, *args, **kwargs)`
                `__getitem__(self, key)`
                `__setitem__(self, key, value)`
                `__delitem__(self, key)`
                `__len__(self)`
                `__iter__(self)`
                `__str__(self)`
                `__repr__(self)`
            from `MutableMapping` mixin
                `__contains__(self, key)`
                `__eq__(mapping)`
                `get(self, key, default=None)`
                `keys()`
                `values()`
                `items()`
                `pop(self, key, default=None)`
                `popitem()`
                `clear()`
                `update(self, mapping)`
                `setdefault(self, key, default=None)`
            possibly?
                `copy()`
            # todo test BaseDict.copy()
    """


    def __init__(self, *args, **kwargs) :
        """
            `BaseDict(**kwarg)`
            `BaseDict(mapping, **kwarg)`
            `BaseDict(iterable, **kwarg)`
            iterable which yields another iterable with exactly 2 objects
        """
        self.dict = dict(*args, **kwargs)


    def __getitem__(self, key) :
        return self.dict[key]

    def __setitem__(self, key, value) :
        self.dict[key] = value

    def __delitem__(self, key) :
        del self.dict[key]

    def __len__(self) :
        return len(self.dict)

    def __iter__(self) :
        return iter(self.dict)


    def __str__(self) :
        return str(self.dict)

    def __repr__(self) :
        """
            prints module.class_name(repr(dict))
            should work for sub classes as well
            # todo test __repr__ on a subclass
        """
        return '{}.{}({})'.format(self.__class__.__module__, self.__class__.__name__, repr(self.dict))