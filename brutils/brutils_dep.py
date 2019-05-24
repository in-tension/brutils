import os
import csv
import time
import pathlib

import numpy as np
import xlsxwriter

## except for functions noted otherwise,


def col_dict_to_cols(col_dict) :
    """
    .. warning:: deprecated - use pandas

    """
    cols = []
    for key in col_dict.keys() :
        cols.append(col_dict[key])
    return cols

def col_dict_to_rows(col_dict) :
    """
    .. warning:: deprecated - use pandas

    """

    # cols = []
    # for key in col_dict.keys() :
    #     cols.append(col_dict[key])
    cols = col_dict_to_cols(col_dict)
    rows = ap.ap_utils.rotate(cols)
    return rows



## <arrs_spreadsheets_io>

## not excluded from documentation
def csv_to_rows(csv_path) :
    """
    .. warning:: deprecated - use pandas

    """
    rows = []
    with open(csv_path,'rU') as csv_file :
        csv_reader = csv.reader(csv_file)
        for row in csv_reader :
            rows.append(row)

    return rows

## not excluded from documentation
def csv_to_dict(csv_path) :
    """
    .. warning:: deprecated - use pandas

    | reads a csv file and creates a dict of cols
    | assumes first row is col names and that all are unique
    """
    rows = csv_to_rows(csv_path)
    cols = rotate(rows)

    col_dict = {}
    for col in cols :
        col_dict[col[0]] = col[1:]

    return col_dict

## not excluded from documentation
def rows_to_csv(rows, csv_path) :
    """
    .. warning:: deprecated - use pandas

    writes a 2D list of rows to a csv
    """
    with open(csv_path, 'w', newline='') as csv_file :
        csv_writer = csv.writer(csv_file)
        for row in rows :
            csv_writer.writerow(row)

def col_dict_to_csv(col_dict, csv_path) :
    """
    .. warning:: deprecated - use pandas


    writes a dict of columns to a csv
    """
    cols = []
    for col_key in col_dict :
        temp_col = [col_key] + col_dict[col_key]
        cols.append(temp_col)
    rows = rotate(cols)
    rows_to_csv(rows, csv_path)

def col_dict_to_sheet(col_dict, w_sheet, col_num=0) :
    """
    .. warning:: deprecated - use pandas

    """
    # col_num = 0
    for key in col_dict :
        if(type(key) == tuple) :
            key_str = tuple_to_str(key)
        elif(type(key) == str) :
            key_str = key
        else :
            key_str = str(key)



        w_sheet.write_string(0, col_num, key_str)
        w_sheet.write_column(1, col_num, col_dict[key])

        col_num += 1
    return col_num


def col_dict_to_xlsx(out_file, col_dict, col_num=0) :
    """
    .. warning:: deprecated - use pandas

    """

    with xlsxwriter.Workbook(out_file, {'nan_inf_to_errors': True}) as w_book :
        w_sheet = w_book.add_worksheet('')
        col_dict_to_sheet(col_dict, w_sheet)
## </arrs_spreadsheets_io>
