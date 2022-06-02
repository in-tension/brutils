"""
Amelia **Br**\ own **Util**\ ities


"""
## brutils -> (amelia) BRown UTILities




import os
import sys
import math
import importlib as imp
from datetime import datetime
# import functools



def is_py2() :
    return sys.version_info < (3,0)


from .arrs import csv_to_rows, rotate

from .tic_toc import dtic, dtoc


## <dev>


def exception_str(e) :
    return '{} : {}'.format(type(e).__name__, str(e))

def dated_output_dir(root_dir) :
    folder_name = '_'.join(['output', datetime.today().strftime('%y-%m-%d')])

    folder_path = os.path.join(root_dir, folder_name)
    ensure_dir(folder_path)
    return folder_path

def dated_file_path(root_dir, file_name) :
    file_name_parts = file_name.split('.')
    file_name_txt = file_name_parts[0]
    file_name_ext = '.'.join(file_name_parts[1:])
    dated_file_txt = '_'.join([file_name_txt, datetime.today().strftime('%y-%m-%d')])
    dated_file_name = '.'.join([dated_file_txt, file_name_ext])

    dated_file_path = os.path.join(root_dir, dated_file_name)
    return dated_file_path

def dict_index(some_dict, val) :
    keys = list(some_dict.keys())
    values = list(some_dict.values())

    return keys[values.index(val)]

def reverse_dict(some_dict) :
    new_dict = {}
    for key, val in some_dict.items() :
        new_dict[val] = key
    return new_dict

def str_comp_ci(str1, str2) :
    """ string compare case insensitive
    will not always work for special characters"""
    return str1.lower() == str2.lower()

def dprint(var, var_name) :
    print('{} = {}'.format(var_name, var))

def range_len(coll) :
    return range(len(coll))

def type_str(obj) :
    return type(obj).__name__


from collections import Counter
if is_py2() :
    from collections import Mapping
else :
    from collections.abc import Mapping



def print_coll_type(obj, indent_cnt=0, str_prefix='') :
    from boltons.iterutils import is_collection, is_scalar

    indent = indent_cnt*'  '
    if is_scalar(obj) :
        print('{ind}{obj_type}'.format(ind=indent, obj_type=type_str(obj)))
    else :
        if isinstance(obj, Mapping) :
            brackets = ['{','}']
        elif is_collection(obj) :
            brackets = ['[',']']

        if len(obj) == 0 :

            s = '{ind}{str_pref}{obj_type} : {brack[0]}{brack[1]}'
            print(s.format(ind=indent, str_pref=str_prefix, obj_type=type_str(obj), brack=brackets))
        else :
            s = '{ind}{str_pref}{obj_type} : {brack[0]}'
            print(s.format(ind=indent, str_pref=str_prefix, obj_type=type_str(obj), brack=brackets))


            obj_scalar_types = []
            if isinstance(obj, Mapping) :
                for item in obj.values() :
                    if is_scalar(item) :
                        obj_scalar_types.append(type(item).__name__)
            else :
                for item in obj :
                    if is_scalar(item) :
                        obj_scalar_types.append(type(item).__name__)


            scalar_type_counts = Counter(obj_scalar_types)
            for scalar_type, cnt in scalar_type_counts.items() :
                print('{ind}{s_type}: {cnt}'.format(ind=indent+'  ', s_type=scalar_type, cnt=cnt))

            if isinstance(obj, Mapping) :
                for key, value in obj.items() :
                    if is_collection(value) :
                        str_prefix = str(key) + ': '
                        print_coll_type(value, indent_cnt=indent_cnt+1, str_prefix=str_prefix)
            else :
                for value in obj :
                    if is_collection(value) :
                        print_coll_type(value, indent_cnt=indent_cnt+1)

            print('{ind}{brack[1]}'.format(ind=indent,brack=brackets))


def temp_print(val) :
    """to distinguish from a normal print call so it's easy to find to remove"""
    print(val)


## </dev>



def is_hashable(obj) :
    try :
        hash(obj)
    except TypeError :
        return False
    return True


def reload(package) :
    """ does this work? seems to
    I don't think it works for fiji tho
    """
    for key, val in package.__dict__.items():
        if type(val) == type(os) :
            imp.reload(val)
        # print(key)
    imp.reload(package)



def one_key(some_dict) :
    for key in some_dict :
        return key

def one_value(some_dict) :
    for value in some_dict.values() :
        return value



def distance(p0, p1):
    """
    | p0 = [x0, y0], p1 = [x1, y1]
    | calculates distance between p0 and p1
    """
    return math.sqrt((p0[0] - p1[0]) ** 2 + (p0[1] - p1[1]) ** 2)


def read_plate_map(pm_file_path) :
    """

    assumes rows go from B-P, and cols from 2-24

    return table_types, well_dicts, condit_dict
    conditi_dict -> key = tuple representing condit
    value = list of well names
    table_types describes the meaning of each element in condit tuples
    """

    pm_rows = csv_to_rows(pm_file_path)

    row_ranges = []
    for i in range(len(pm_rows)) :
        if pm_rows[i][0] == 'B' :
            row_ranges.append([i])
        elif pm_rows[i][0] == 'P' :
            row_ranges[-1].append(i)

    tables = []


    for start, stop in row_ranges :
        tables.append(pm_rows[start-1:stop+1])

    well_dicts = {}
    table_types = []
    for table in tables :
        table_type, well_dict = process_pm_table(table)
        well_dicts[table_type] = well_dict
        table_types.append(table_type)


    well_names = well_dicts[table_types[0]].keys()

    condit_table_names = []
    for table_type in table_types :
        if well_dicts[table_type].keys() != well_names :
            ### improve this
            print("shit, some tables in plate-map have data in more wells than other tables\ncode assumes that this isn't the case and will likely cause issues if not\n\twill only look at wells that are in the very first table\n\twill crash if later table does not have a well in first table")

        ## could use startswith('condit') or split('_')[0] == 'condit'
        if table_type.startswith('condit') :
             condit_table_names.append(table_type)

    condit_dict = {}

    for well_name in well_names :
        condit_name = ()
        for condit_table_name in condit_table_names :
            name_part = well_dicts[condit_table_name][well_name]
            if 'num' in condit_table_name :
                try :
                    name_part = float(name_part)
                except :
                    pass
                    ### improve this
                    #print("poop, issue in plate-map, table supposed to contain numbers\nbut well {0} can't be converted to a number, well {0} = {1}".format(well_name,name_part))

            condit_name = condit_name + (name_part,)
        if condit_name in condit_dict :
            condit_dict[condit_name].append(well_name)
        else :
            condit_dict[condit_name] = [well_name]

    return table_types, well_dicts, condit_dict

def process_pm_table(pm_table) :
    """
        used by read_plate_map
        | takes pm_table, a table from the plate-map file and
    """

    if not len(pm_table) == 16 :
        ### fix this
        print('brutils.proces_pm_table: crap, this shouldnt happen')
    elif not len(pm_table[0]) == 24 :
        ### fix this
        print('brutils.proces_pm_table: crap, this shouldnt happen')

    table_type = pm_table[0][0]

    col_names = pm_table[0][1:]

    pm_table = pm_table[1:]
    table_as_cols = rotate(pm_table)
    row_names = table_as_cols[0]

    table_as_cols = table_as_cols[1:]


    well_dict = {}
    for c in range(len(table_as_cols)) :
        for r in range(len(table_as_cols[c])) :
            col_name = col_names[c]
            while len(col_name) < 2 :
                col_name = '0' + col_name

            well_name = row_names[r] + col_name

            well_value = table_as_cols[c][r]
            if well_value != '' :
                well_dict[well_name] = well_value

    return table_type, well_dict



def ensure_dir(path) :
    """
        if dir doensn't exist, creates it
    """
    if not os.path.exists(path):
        os.makedirs(path)





def flt_rng(*args):
    if len(args) == 1:
        start = 0
        stop = args[0]
        step = 1

    elif len(args) == 2:
        start = args[0]
        stop = args[1]
        step = 1

    elif len(args) == 3:
        start = args[0]
        stop = args[1]
        step = args[2]
    else:
        raise TypeError('flt_rng only takes up to 3 arguments')

    vals = []
    i = start
    while i < stop:
        vals.append(i)
        i += step

    return vals




def pattern_in_list(some_list, pattern) :
    """
        this can't be the right way to do this
        assumes list does not contain commas
        only finds first instance
    """
    split_char = ','

    str_list = ''
    for element in some_list :
        str_list += str(element) + split_char

    str_pattern = ''
    for element in pattern :
        str_pattern += str(element) + split_char

    str_index = str_list.find(str_pattern)
    if str_index != -1 :
        index = str_list[:str_index].count(split_char)
        return index
    else :
        return -1



def tuple_to_str(tup, delim='_') :
    """
    """
    temp = []
    for term in tup :
        temp.append(str(term))
    return delim.join(temp)


class Pnt:

    def __init__(self,x,y):
        self.x = x
        self.y = y

    @property
    def xy(self):
        return self.x, self.y

    @xy.setter
    def xy(self, val):
        self.x, self.y = val

    def __iter__(self):
        return iter([self.x, self.y])


class Lims:

    def __init__(self,min,max):
        self._min = min
        self._max = max

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, value):
        if value > self._max:
            raise TypeError('trying to set {} to min when max is {}, min cannot be set to value larger than max'.format(value, self._max))
        else:
            self._min = value

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, value):
        if value < self._min:
            raise TypeError('trying to set {} to max when min is {}, max cannot be set to value smaller than min'.format(value, self._min))
        else:
            self._max = value

    @property
    def min_max(self):
        return self.min, self.max

    @min_max.setter
    def min_max(self, value):
        self.min, self.max = value

    def __iter__(self):
        return iter([self.min, self.max])









import platform
if platform.system() != 'Java' :
    import numpy as np


    def create_df_dists(df, x_col_name, y_col_name, dist_col_name="Distance", index_col=None):
        """


        """




        ct = dtic('create_df_dists')
        if dist_col_name in df.columns:
            pass
        else:
            df[dist_col_name] = np.nan

        dt = dtic('create_df_dists for loop')
        for r in range(0, len(df) - 1):

            one = df.iloc[r]
            two = df.iloc[r + 1]

            if one[index_col] == two[index_col] - 1:
                df[dist_col_name].iloc[r] = distance([one[x_col_name], one[y_col_name]],
                                                     [two[x_col_name], two[y_col_name]])
        dtoc(dt)
        print(df[dist_col_name])

        dtoc(ct)


    def create_df_dists2(df, x_col_name, y_col_name, dist_col_name="Distance", index_col=None):
        """


        """
        # """ adds column to original df """
        # global count
        # count+=1

        # if count == 1 :
        #     print(df[[index_col,x_col_name,y_col_name,dist_col_name]])

        if dist_col_name in df.columns:
            pass
        else:
            df[dist_col_name] = np.nan

        c = 0
        ct = 0
        cf = 0

        for n in range(len(df.index) - 1):
            c += 1
            r = df.index[n]
            r2 = df.index[n + 1]

            if df.loc[r, index_col] == df.loc[r2, index_col] - 1:
                ct += 1

                df.loc[r, dist_col_name] = (distance([df.loc[r, x_col_name], df.loc[r, y_col_name]],
                                                     [df.loc[r2, x_col_name], df.loc[r2, y_col_name]]))
            else:
                cf += 1

        #
        # if count == 1:
        #     print(df[[index_col, x_col_name, y_col_name, dist_col_name]])

        return df
