"""
Amelia **Br**\ own **Util**\ ities

"""
# brutils -> (amelia) BRown UTILities

import os
import csv
import time
import pathlib
import math
import sys
import datetime
import importlib as imp
import types

import numpy as np
import xlsxwriter
from pprint import pprint
from termcolor import colored


# __all__ = ['get_attrs','pprint_attrs']


# from .brutils_dep import  *



def reload(package) :
    for key, val in package.__dict__.items():
        if type(val) == type(os) :
            imp.reload(val)
        print(key)
    imp.reload(package)



def one_key(some_dict) :
    for key in some_dict :
        return key

def one_value(some_dict) :
    for value in some_dict.values() :
        return value




def create_df_dists(df, x_col_name, y_col_name, dist_col_name="Distance", index_col=None) :
    """ adds column to original df """
    ct = dtic('create_df_dists')
    if dist_col_name in df.columns :
        pass
    else :
        df[dist_col_name]=np.nan


    dt = dtic('create_df_dists for loop')
    for r in range(0,len(df)-1) :

        one = df.iloc[r]
        two = df.iloc[r+1]

        if one[index_col] == two[index_col] - 1 :
            df[dist_col_name].iloc[r] = distance([one[x_col_name],one[y_col_name]],[two[x_col_name],two[y_col_name]])
    dtoc(dt)
    print(df[dist_col_name])

    dtoc(ct)

def create_df_dists2(df, x_col_name, y_col_name, dist_col_name="Distance", index_col=None) :
    """ adds column to original df """
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



    for n in range(len(df.index)-1) :
        c+=1
        r = df.index[n]
        r2 = df.index[n+1]

        if df.loc[r, index_col] == df.loc[r2, index_col] - 1 :
            ct+=1

            df.loc[r, dist_col_name] = (distance([df.loc[r, x_col_name], df.loc[r, y_col_name]], [df.loc[r2, x_col_name]    , df.loc[r2, y_col_name]]))
        else :
            cf+=1


    #
    # if count == 1:
    #     print(df[[index_col, x_col_name, y_col_name, dist_col_name]])

    return df


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



def loc_print() :
    # print(locals().keys())
    # print(globals().keys())
    import inspect
    # print(inspect.getframeinfo(inspect.currentframe().f_back).function)
    cur_frame = inspect.currentframe()
    prev_frame = cur_frame.f_back
    prev_frame_info = inspect.getframeinfo(prev_frame).function
    print(inspect.getframeinfo(cur_frame).function)
    print(prev_frame_info)
    print(__name__)
    print(__package__)




def ensure_dir(path) :
    """
        if dir doensn't exist, creates it
    """
    if not os.path.exists(path):
        os.makedirs(path)



def arr_cast(arr, cast_type) :
    """
        cast_type = str, float, int...
    """
    new_arr = []
    for element in arr :
        try :
            new_element = cast_type(element)
            new_arr.append(new_element)
        except :
            new_arr.append(element)
    return new_arr

## arr_cast assumed from str
## where '' is set to None
def arr_cast_spec(arr, cast_type) :
    """
        cast_type = float, int...
    """
    new_arr = []
    for element in arr :
        try :
            new_element = cast_type(element)
            new_arr.append(new_element)
        except :
            new_arr.append(None)
    return new_arr





def avg(arr) :
    """
        .. warning:: deprecated

        uses statistics.mean() instead

        | returns the average of a given array
        | skips None values
    """
    sum = 0.0
    count = 0
    for element in arr :
        if element != None :
            sum += element
            count += 1

    if count == 0 :
        return None
    return sum/count

def mov_avg(arr, above_below=5) :
    """
        should also be able to use pandas.DataFrame.rolling(window)
    """
    new_arr = []
    for i in range(len(arr)) :

        below = i - above_below
        if below < 0 : below = 0
        above = i + above_below
        if above >= len(arr) : above = len(arr) - 1

        new_element = avg(arr[below:above])
        new_arr.append(new_element)
    return new_arr








#
# def br_pprint(obj) :
#     """
#     all interables shoulb be printed with newlines -> including dict.keys() and dict.items()
#     """
#     try :
#         iterator = iter(obj)
#     except TypeError :
#         # not iterable
#         pprint(obj)
#     else :
#         pprint(list(obj))






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



