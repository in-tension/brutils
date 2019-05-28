"""
Author: Amelia Brown
today (who knows which day): 5/24/17

arr(array) -> a list -> usually represents a colulmn or row
arrs -> a 2D list -> usually represents columns or rows

row/col(column) -> same as an arr, has no technical distinction but sometimes used as a convenience
rows/cols -> same as an arrw, has no technical distinction but sometimes used as a convenience

arr_dict -> dict whos values are each an arr(/row/dict)

rec(rectangle) -> the length of all inner arrs is the same

"""
## todo has not really been tested since some refactoring and renaming

import csv


from .brutils import one_value, tuple_to_str


__all__ = [
    'is_rec',
    'is_rec_arr_dict',
    'make_rec',
    'rotate',
    'arr_dict_to_arrs',
    'rotate_arr_dict',

    'csv_to_rows',
    'csv_to_col_dict',
    'rows_to_csv',
    'col_dict_to_csv',
    'col_dict_to_sheet',
    'col_dict_to_xlsx'
]


### <arrs manipulation> ###

def is_rec(arrs) :
    """
        | checks whether 2D list ``arrs`` is a rectangle -
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
        | checks whether 2D list ``arrs`` is a rectangle -
        | checks that all inner arrays are the same length
        | returns a boolean

    """
    length = len(one_value(arr_dict))
    for arr in arr_dict.values() :
        if len(arr) != length :
            return False
    return True


def make_rec(arrs, blank=None) :
    """
        | takes a 2D list ``arrs`` and makes sure it's a rectangle -
        | makes sures all inner lists are the same length

        | changes original ``arrs``
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
        | takes a 2D list ``arrs`` and switches the inner and outer arrays
        | i.e. rows_to_cols or cols_to_rows

        makes ``arrs`` a rectangle using make_rec - which changes oringinal ``arrs``)

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

        arr labels are lost
    """
    cols = arr_dict_to_arrs(arr_dict)
    rows = rotate(cols)
    return rows


### </arrs manipulation> ###


### <arrs fio> ###

def csv_to_rows(csv_path) :
    rows = []
    with open(csv_path,'rU') as csv_file :
        csv_reader = csv.reader(csv_file)
        for row in csv_reader :
            rows.append(row)

    return rows


def csv_to_col_dict(csv_path) :
    """
    | reads a csv file and creates a dict of cols
    | assumes first row is col names and that all are unique
    """
    rows = csv_to_rows(csv_path)
    arrs = rotate(rows)

    arr_dict = {}
    for arr in arrs :
        arr_dict[arr[0]] = arr[1:]

    return arr_dict


def rows_to_csv(rows, csv_path) :
    """
        writes a 2D list of rows to a csv
    """
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
        temp_arr = [arr_key] + arr_dict[arr_key]
        arrs.append(temp_arr)
    rows = rotate(arrs)
    rows_to_csv(rows, csv_path)


def col_dict_to_sheet(arr_dict, w_sheet, arr_num=0) :
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
        col_dict_to_sheet(arr_dict, w_sheet)


### <arrs fio> ###



