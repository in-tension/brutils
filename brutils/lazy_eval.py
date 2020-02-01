import functools


class RaisingLazyEvalException(Exception) :
    def __init__(self, exc_or_message) :
        super(Exception, self).__init__('')

        if isinstance(exc_or_message, Exception) :
            self.message = type(exc_or_message).__name__ + ': ' + str(exc_or_message)
        else :
            self.message = exc_or_message

    def __str__(self) :
        return type(self).__name__ + ': ' + self.message

class LazyEvalException(Exception) :

    def __init__(self, raising_function, message) :
        super(Exception, self).__init__('')

        self.raising_function = raising_function
        self.message = message
        self.calling_function = None


    # def __str__(self) :
    #     print(self.calling_function)
    #     # s = type(self).__name__ + ': '
    #     s = LazyEvalException.func_to_str(self.calling_function)
    #     s += ' -> '
    #     s += LazyEvalException.func_to_str(self.raising_function)
    #     s += ' -> '
    #     s += self.message
    #
    #     return s

    def __str__(self) :

        s = self.message
        s += ' -> raised by: '
        s += LazyEvalException.func_to_str(self.raising_function)
        s += ' -> called by: '
        s += LazyEvalException.func_to_str(self.calling_function)

        return s

    @staticmethod
    def func_to_str(func) :
        if isinstance(func, str) :
            return func + '()'
        else :
            return str(func) + '()'


def lazy_eval_or_except(func) :
    """@lazy_eval -> a decorator used on a class instance method,
    it tests to see if inst._<func_name> exists
    if it doesn't, it calls the decorated func on inst, which it assumes creates the variable of that name, after the func finishes the decorator again attempts to returns that variable

    + try except LazyEvalException stuff
    """
    @functools.wraps(func)
    def wrapper(*args) :
        inst = args[0]
        attr_name = '_' + func.__name__

        try :
            return inst.__dict__[attr_name]
        except KeyError :

            try :
                func(inst)
                return inst.__dict__[attr_name]
            except RaisingLazyEvalException as rlee :
                # print('lazy_eval_or_except: caught rlee')
                try :
                    fname = func.__qualname__
                except :
                    fname = func.__name__

                lee = LazyEvalException((func.__module__,fname), rlee.message)
                lee.calling_function = (func.__module__,fname)
                raise lee

            except LazyEvalException as lee :
                # print('lazy_eval_or_except: caught lee')
                try :
                    fname = func.__qualname__
                    mname = func.__module__
                except :
                    fname = func.__name__
                    mname = str(inst.__class__).split('.')[-1]

                # print(inst.__class__)
                lee.calling_function = (mname, fname)
                raise lee

    return wrapper


def lazy_eval(func) :
    """ a decorator used on a class instance method,
    it tests to see if inst._<func_name> exists
    if it doesn't, it calls the decorated func on inst and which it assumes creates the variable of that name, after the func finishes the decorator again returns that variable"""
    @functools.wraps(func)
    def wrapper(*args) :
        inst = args[0]
        attr_name = '_' + func.__name__


        try :
            return inst.__dict__[attr_name]
        except KeyError :
            func(inst)
            return inst.__dict__[attr_name]

    return wrapper



def lazy_eval_dict(func) :
    """ a decorator used on a class instance method,
    it tests to see if inst._<func_name>[key] exists
    if it doesn't, it calls func(inst, key) and which it assumes creates the variable of that name, after the func finishes the decorator again returns that variable"""
    @functools.wraps(func)
    def wrapper(*args) :
        inst = args[0]
        key = args[1]
        dict_name = '_' + func.__name__

        if dict_name not in inst.__dict__ :
            inst.__dict__[dict_name] = {}
        # try :
        #     inst.__dict__[dict_name]
        # except KeyError :
        #     inst.__dict__[dict]


        try :
            return inst.__dict__[dict_name][key]
        except KeyError :
            func(inst, key)
            return inst.__dict__[dict_name][key]

    return wrapper
