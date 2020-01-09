
## todo has not really been tested since some refactoring and renaming

import csv


import sys
if sys.version_info < (3,0) :
    PY_2 = True
else :
    PY_2 = False





### <arrs manipulation> ###

def is_rec(arrs) :
    """
        | checks whether 2D list :term:`arrs` is a rectangle -
        | checks that all inner arrays are the same length
        | returns a boolean

    """
    length = len(arrs[0])
    for arr in arrs :
        if len(arr) != length :
            return False
    return True


def is_rec_arr_dict(arr_dict) :
    """
        | checks whether 2D list :term:`arrs` is a rectangle -
        | checks that all inner arrays are the same length
        | returns a boolean

    """
    from .misc import one_value
    length = len(one_value(arr_dict))
    for arr in arr_dict.values() :
        if len(arr) != length :
            return False
    return True


def make_rec(arrs, blank=None) :
    """
        | takes a 2D list :term:`arrs` and makes sure it's a rectangle -
        | makes sures all inner lists are the same length

        | changes original :term:`arrs`
        | ``blank`` = value added to end of inner arrays if not long enough

    """
    if not is_rec(arrs) :
        longest = 0
        for arr in arrs :
            if len(arr) > longest :
                longest = len(arr)

        for arr in arrs :
            while len(arr) < longest :
                arr.append(blank)


def rotate(arrs, blank=None) :
    """
        | takes a 2D list :term:`arrs` and switches the inner and outer arrays
        | i.e. rows_to_cols or cols_to_rows

        makes :term:`arrs` a rectangle using make_rec - which changes oringinal :term:`arrs`)

        blank is used in make_rec
    """
    make_rec(arrs,blank=blank)

    rotated_arrs = [[arr[i] for arr in arrs] for i in range(len(arrs[0]))]
    return rotated_arrs


def arr_dict_to_arrs(arr_dict) :
    arrs = []
    for key in arr_dict.keys() :
        arrs.append(arr_dict[key])
    return arrs


def rotate_arr_dict(arr_dict) :
    """
        returns 2D list (arrs/rows)
        not a rotated dict

        :term:`arr` labels are lost
    """
    cols = arr_dict_to_arrs(arr_dict)
    rows = rotate(cols)
    return rows


### </arrs manipulation> ###



# def out_col_dict()




### <arrs fio> ###

def csv_to_rows(csv_path, cast_type=None) :
    """
    """
    rows = []
    with open(csv_path,'rU') as csv_file :
        csv_reader = csv.reader(csv_file)
        for row in csv_reader :
            rows.append(row)

    if cast_type is not None :
        rows = arrs_cast_spec(rows, cast_type=cast_type)

    return rows






def csv_to_col_dict(csv_path, cast_type=str) :
    """
    | reads a csv file and creates a dict of cols
    | assumes first row is col names and that all are unique
    """
    rows = csv_to_rows(csv_path)
    # print(rows)
    # print('\n\n')

    if cast_type is not None :
        temp = [rows[0]]
        temp.extend(arrs_cast_spec(rows[1:], cast_type=cast_type))
        rows = temp

    # print(rows)

    cols = rotate(rows)


    col_dict = {}
    for col in cols :
        col_dict[col[0]] = col[1:]

    return col_dict



def rows_to_csv(rows, csv_path) :
    """
        writes a 2D list of rows to a csv
    """
    if PY_2 :
        #print(rows)
        with open(csv_path, 'wb') as csv_file :
            csv_writer = csv.writer(csv_file)
            for row in rows :
                csv_writer.writerow(row)
    else :
        with open(csv_path, 'w', newline='') as csv_file :
            csv_writer = csv.writer(csv_file)
            for row in rows :
                csv_writer.writerow(row)




def col_dict_to_csv(arr_dict, csv_path) :
    """
        writes a dict of columns to a csv
    """

    arrs = []
    for arr_key in arr_dict :
        temp_arr = [arr_key] + list(arr_dict[arr_key])
        arrs.append(temp_arr)
    rows = rotate(arrs)
    rows_to_csv(rows, csv_path)


def col_dict_to_sheet(arr_dict, w_sheet, arr_num=0) :
    from .misc import tuple_to_str
    try :
        import xlsxwriter
    except ModuleNotFoundError as err :
        raise ImportError('ImportError: package xlswriter needed for brutils.arrs_manip.col_dict_to_xlsx ')

    for key in arr_dict :
        if type(key) == tuple  :
            key_str = tuple_to_str(key)
        elif type(key) == str :
            key_str = key
        else :
            key_str = str(key)

        w_sheet.write_string(0, arr_num, key_str)
        w_sheet.write_arrumn(1, arr_num, arr_dict[key])

        arr_num += 1
    return arr_num


def col_dict_to_xlsx(out_file, arr_dict, arr_num=0) :
    try :
        import xlsxwriter
    except ModuleNotFoundError :
        raise ImportError('ImportError: package xlswriter needed for brutils.arrs_manip.col_dict_to_xlsx ')

    with xlsxwriter.Workbook(out_file, {'nan_inf_to_errors': True}) as w_book :
        w_sheet = w_book.add_worksheet('')
        col_dict_to_sheet(arr_dict, w_sheet, arr_num=arr_num)







### </arrs fio> ###



def arr_cast(arr, cast_type) :
    """
        loops through arr and casts each element to cast_type
        copies origialnal element if cast fails
    """
    new_arr = []
    for element in arr :
        try :
            new_element = cast_type(element)
            new_arr.append(new_element)
        except :
            new_arr.append(element)
    return new_arr


def arrs_cast(arrs, cast_type) :
    """
        loops through all elements in arrs and casts each to cast_type
        copies original element if cast fails
    """
    arrs2 = []
    for arr in arrs :
        temp = arr_cast(arr, cast_type=cast_type)
        arrs2.append(temp)

    return arrs2



## arr_cast assumed from str
## where '' is set to None
def arr_cast_spec(arr, cast_type) :
    """
        loops through arr and casts each element to cast_type
        replaces empty strings ``''`` with None
        copies original element if cast fails

    """
    new_arr = []
    for element in arr :
        # print(element)
        if element == '' :
            new_arr.append(None)
        else :
            try :
                new_element = cast_type(element)

                new_arr.append(new_element)
            except Exception:
                new_arr.append(element)

        # print(new_arr[-1])
    return new_arr


def arrs_cast_spec(arrs, cast_type):
    """
        loops through all elements in arrs and casts each to cast_type
        replaces empty strings ``''`` with None
        copies original element if cast fails
    """
    arrs2 = []
    for arr in arrs:
        temp = arr_cast_spec(arr, cast_type=cast_type)
        arrs2.append(temp)

    return arrs2






def avg(arr) :
    """
        .. warning:: deprecated
        uses statistics.mean() instead

        | returns the average of a given array
        | skips None values
    """
    tot = 0.0
    count = 0
    for element in arr :
        if element is not None :
            tot += element
            count += 1

    if count == 0 :
        return None
    return tot/count


if not PY_2 :
    import statistics
    def normalize(arr) :
        """
            divides each element in arr by average and returns the results
        """
        average = statistics.mean(arr)

        arr2 = []
        for num in arr :
            arr2.append(num/average)

        return arr2





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


import platform
if platform.system() != 'Java' :
    import numpy as np


    def arr_np_nan(arr, blank=None):
        """
            replaces blank values in arr with np.nan
        """
        for i in range(len(arr)):
            if arr[i] == blank:
                arr[i] = np.nan


    def col_dict_np_nan(col_dict, blank=None):
        """
            replaces blank values in cols of col_dict with np.nan
        """
        for col_name in col_dict:
            arr_np_nan(col_dict[col_name], blank=blank)


    def col_dict_row_nanmed(col_dict):
        """
            assumes col_dict is rec

            pandas can do similar things but the also comes with more overhead

        """
        col_dict_np_nan(col_dict)
        for col_name in col_dict:
            h = len(col_dict[col_name])
            break

        med_col = []
        for r in range(h):
            temp_row = []
            for col_name in col_dict:
                temp_row.append(col_dict[col_name][r])
            med = np.nanmedian(temp_row)
            med_col.append(med)

        return med_col


    def col_dict_row_nanmean(col_dict):
        """
            asumes col_dict is rec

            pandas can do similar things but the also comes with more overhead
        """

        col_dict_np_nan(col_dict)

        for col_name in col_dict:
            h = len(col_dict[col_name])
            break

        mean_col = []
        for r in range(h):
            temp_row = []
            for col_name in col_dict:
                temp_row.append(col_dict[col_name][r])
            mean = np.nanmean(temp_row)
            mean_col.append(mean)

        return mean_col
