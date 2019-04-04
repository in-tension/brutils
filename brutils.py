""" brutils -> brown utils -> amelia brown utils """

import os
import csv
import time
import pathlib

import numpy as np
import xlsxwriter




def one_key(some_dict) :
    for key in some_dict :
        return key

def one_value(some_dict) :
    for value in some_dict.values() :
        return value


def col_dict_to_cols(col_dict) :
    cols = []
    for key in col_dict.keys() :
        cols.append(col_dict[key])
    return cols

def col_dict_to_rows(col_dict) :
    # cols = []
    # for key in col_dict.keys() :
    #     cols.append(col_dict[key])
    cols = col_dict_to_cols(col_dict)
    rows = ap.ap_utils.rotate(cols)
    return rows



## <arrs_spreadsheets_io>
def csv_to_rows(csv_path) :
    """
    """
    rows = []
    with open(csv_path,'rU') as csv_file :
        csv_reader = csv.reader(csv_file)
        for row in csv_reader :
            rows.append(row)

    return rows

def csv_to_dict(csv_path) :
    """
        reads a csv file and creates a dict of rows
        assumes first row is col names and that all are unique
    """
    rows = csv_to_rows(csv_path)
    cols = rotate(rows)

    col_dict = {}
    for col in cols :
        col_dict[col[0]] = col[1:]

    return col_dict

def rows_to_csv(rows, csv_path) :
    """
        writes a 2D list of rows to a csv
    """
    with open(csv_path, 'w', newline='') as csv_file :
        csv_writer = csv.writer(csv_file)
        for row in rows :
            csv_writer.writerow(row)

def col_dict_to_csv(col_dict, csv_path) :
    """
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
    with xlsxwriter.Workbook(out_file, {'nan_inf_to_errors': True}) as w_book :
        w_sheet = w_book.add_worksheet('')
        col_dict_to_sheet(col_dict, w_sheet)
## </arrs_spreadsheets_io>




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
        table_type, well_dict = Exper.process_pm_table(table)
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

## <arrs_manip>
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

def is_rec_col_dict(col_dict) :
    """
        | checks whether 2D list ``arrs`` is a rectangle -
        | checks that all inner arrays are the same length
        | returns a boolean

    """
    length = len(one_value(col_dict))
    for col in col_dict.values() :
        if len(col) != length :
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
            while(len(arr) < longest) :
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
## </arrs_manip>





def ensure_dir(dir) :
    """
        if dir doensn't exist, creates it
    """
    if not os.path.exists(dir):
        os.makedirs(dir)

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

def arr_np_nan(arr, blank=None) :
    """ replaces blank values in arr with np.nan """
    for i in range(len(arr)) :
        if arr[i] == blank :
            arr[i] = np.nan


def col_dict_np_nan(col_dict, blank=None) :
    """ replaces blank values in cols of col_dict with np.nan """
    for col_name in col_dict :
        arr_np_nan(col_dict[col_name],blank=blank)

def col_dict_row_nanmed(col_dict) :
    """
        .. note: asumes col_dict is rec
    """
    col_dict_np_nan(col_dict)
    for col_name in col_dict :
        h = len(col_dict[col_name])
        break

    med_col = []
    for r in range(h) :
        temp_row = []
        for col_name in col_dict :
            temp_row.append(col_dict[col_name][r])
        med = np.nanmedian(temp_row)
        med_col.append(med)



    return med_col

def col_dict_row_nanmean(col_dict) :
    """
        .. note: asumes col_dict is rec
    """

    col_dict_np_nan(col_dict)

    for col_name in col_dict :
        h = len(col_dict[col_name])
        break

    mean_col = []
    for r in range(h) :
        temp_row = []
        for col_name in col_dict :
            temp_row.append(col_dict[col_name][r])
        mean = np.nanmean(temp_row)
        mean_col.append(mean)



    return mean_col




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

## <tic_toc>
def tic() :
    """
    """
    return time.time()

def toc(start_time) :
    """
    """
    end_time = time.time()
    return (end_time-start_time)

def toc2(start_time, descrip='') :
    """
    """
    elapsed_time = toc(start_time)
    print('{} : {} seconds'.format(descrip, elapsed_time))

## ptoc = print_toc
def ptic(descrip) :
    """
    """
    return [descrip,time.time()]

def ptoc(descrip_n_time) :
    """
    """
    elapsed_time = time.time() - descrip_n_time[1]
    print('{} : {:.2f} seconds'.format(descrip_n_time[0], elapsed_time))
## </tic_toc>
