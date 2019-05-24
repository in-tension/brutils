
from collections.abc import MutableMapping

class SupDict(MutableMapping) :


    def __init__(self, *args, **kwargs) :
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
        module.class_name(dict_repr)
        """
        return '{}.{}({})'.format(self.__class__.__module__, self.__class__.__name__, repr(self.dict))