from pprint import pprint
import types


def attr_keys(obj) :
    return obj.__dict__.keys()

def attr_values(obj) :
    return obj.__dict__.values()

def attr_items(obj) :
    return obj.__dict__.items()

def get_attrs(obj,show_hidden=False) :
    """
    obj -> package, class, variable,
        really anything with __dict__
    returns a list
    """
    #return obj.__dict__.keys()
    if show_hidden :
        return list(obj.__dict__.keys())
    else :
        attrs = []
        for k in obj.__dict__.keys() :
            if not k.startswith('_') :
                attrs.append(k)
        return attrs

def get_attr_items(obj, show_hidden=False) :
    if show_hidden :
        return obj.__dict__.items()
    else :
        attr_items = {}
        for k, v in obj.__dict__.items() :
            if not k.startswith('_') :
                attr_items[k] = v
        return attr_items


def pprint_attrs(obj, show_hidden=False) :
    # for key in getattrs(obj) :
    #     print(key)
    pprint(get_attrs(obj, show_hidden=show_hidden))


def pprint_attr_types(obj, show_hidden=False) :

    if show_hidden :
        for k, v in  obj.__dict__.items() :
            print('{:20} : {}'.format(k,str(type(v))))
    else :
        for k, v in  obj.__dict__.items() :
            if not k.startswith('_') :
                print('{:20} : {}'.format(k,str(type(v))))


def print_any_class(obj) :
    obj_attrs = get_attr_items(obj)
    for k, v in obj_attrs :
        print('{:20} : {}'.format(k,v))

def print_any_class_str(obj) :
    obj_attrs = get_attr_items(obj)
    obj_str = ''
    for k, v in obj_attrs :
        obj_str += '{:20} : {}\n'.format(k,v)
    return obj_str



def get_funcs_clsmethods(obj, show_hidden=False) :
    """take """
    if type(obj) == type :
        obj_cls = obj
    else :
        obj_cls = type(obj)

    funcs = []
    clsmethods = []
    if show_hidden :
        for key, value in obj_cls.__dict__.items() :
            if type(value) == types.FunctionType:
                funcs.append(key)
            elif type(value) == types.MethodType:
                clsmethods.append(key)

    else :
        for key, value in obj_cls.__dict__.items() :
            if key.startswith('_') :
                continue
            if type(value) == types.FunctionType  :
                funcs.append(key)
            elif type(value) == types.MethodType :
                clsmethods.append(key)

    return funcs, clsmethods

# def get_all_funcs(obj, show_hidden=False) :


def get_funcs(obj, show_hidden=False) :
    funcs, clsmethods = get_funcs_clsmethods(obj, show_hidden=show_hidden)
    return funcs

def get_clsmethods(obj, show_hidden=False) :
    funcs, clsmethods = get_funcs_clsmethods(obj, show_hidden=show_hidden)
    return clsmethods