'''
    Analysis of Israel Pollutant Release and Transfer Register (PRTR)
    Copyright (C) 2020  Doreen S. Ben-Zvi, PhD

    Full license is locates in License.txt at project root folder.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import numpy as np
import pandas as pd


# Displaying data overview by describe and column names
def observe_data(data):
    desired_width = 230
    pd.set_option('display.width', desired_width)
    pd.set_option('display.max_columns', len(data.columns))
    print("Numeric Data Description:")
    description_numeric = data.describe(include=[np.number])
    print(description_numeric)
    print("Text Data Description:")
    description_object = data.describe(include=[np.object])
    print(description_object)
    print("Data columns:")
    column_names = data.columns
    print(column_names)
    print("pause")


# Removes columns which empty or binary values
def remove_low_variety_columns(data):
    columns_deleted = []
    for col_name in data.columns:
        if len(data[col_name].unique()) < 2 or data[col_name].isnull().all() == True:
            columns_deleted.append(col_name)
            data.drop([col_name], axis=1, inplace=True)
    # print("Deleted Colums: " + str(columns_deleted))
    with open('Output_files/deletedColumns.txt', 'w') as file1:
        for item in columns_deleted:
            file1.write("%s\n" % item)
    file1.close()
    return data, columns_deleted


# UI for choosing what to do with a column
def user_action_select_ui(flag):
    switcher = {
        1: "remain unchanged",
        2: "int",
        3: "bool",
        4: "date",
        5: "category",
        6: "Add to list for manual correction",
        7: "Remove"
    }
    print(switcher)
    while flag == 0:
        try:
            input_val = int(input())
            if input_val > 0 and input_val < 8: flag = 1
        except ValueError:
            print("Input should be a number between 1 and 6")
    return input_val


# Saves all column names which have NaN values for considering how to cope with them
# Note that binary removal is specifically adequate for this dataset which uses explicite categories and no dummy columns
def identify_cols_with_nan(data):
    columns_with_nan = []
    for col_name in data.columns:
        if data[col_name].isnull().any() == True:
            columns_with_nan.append(col_name)
    # print("Columns that have NaNs: " + str(columns_with_nan))
    with open('Output_files/columsWithNan.txt', 'w') as file2:
        for item in columns_with_nan:
            file2.write("%s\n" % item)
    file2.close()
    return data, columns_with_nan


# Converts data in dataframe columns to the datatype chosen by the user
def convert_datatype_ui(data):
    data_dict = data.dtypes.to_dict()
    columns_for_manual_correction = []
    columns_deleted = []

    for key in data_dict:
        unique_vals = data[key].unique()
        unique_no = len(unique_vals)
        print(str(key) + " is type " + str(data_dict[key]) + " with " + str(unique_no) + " values")
        print(*unique_vals[0:min(unique_no, 10)], sep=", ")
        if data[key].isnull().any() == True: print("***Conatins NaNs***")
        print("It should:")
        input_val = user_action_select_ui(flag=0)
        if input_val == 2:
            try:
                data[key] = pd.to_numeric(data[key])
            except:
                print("%s column cannot be converted to int" % key)
                columns_for_manual_correction.append(key + " cannot be converted into int")
        elif input_val == 3:
            try:
                data[key] = data[key].astype('bool')
            except:
                print("%s column cannot be converted to boolean" % key)
                columns_for_manual_correction.append(key + " cannot be converted into boolean")
        elif input_val == 4:
            try:
                data[key] = pd.to_datetime(data[key], format='%d/%m/%Y')
            except:
                print("%s column cannot be converted to d/m/Y" % key)
            columns_for_manual_correction.append(key + " cannot be converted into d/m/Y")
        elif input_val == 5:
            try:
                data[key].astype('category')
            except:
                print("%s column cannot be converted to category" % key)
                columns_for_manual_correction.append(key + " cannot be converted into category")
        elif input_val == 6:
            columns_for_manual_correction.append(key)
        elif input_val == 7:
            try:
                data.drop([key], axis=1, inplace=True)
                columns_deleted.append(key)
                with open("Output_files/deletedColumns.txt", "a") as file3:
                    file3.write("%s\n" % key)
                file3.close()
            except:
                print("%s column cannot be deleted" % key)
            #
        else:
            continue

    # print("Columns for manual correction: "+ str(columns_for_manual_correction))
    with open('Output_files/ForManual.txt', 'w') as file4:
        for item in columns_for_manual_correction:
            file4.write("%s\n" % item)
    file4.close()
    return data, columns_for_manual_correction, columns_deleted


# Removes binary columns and empty columns, outputs all columns with nan into a file,
# descrives each column and opens a UI asking what to do with it, and displays
# summary of all user induced actions
def clean_data_ui(data):
    observe_data(data)
    [data, columns_deleted1] = remove_low_variety_columns(data)
    [data, columns_manual, columns_deleted2] = convert_datatype_ui(data)
    [data, columns_nan] = identify_cols_with_nan(data)
    print("Summery:")
    print("Deleted Columns: " + str(columns_deleted1 + columns_deleted2))
    print("Columns for manual correction: " + str(columns_manual))
    print("Columns that have NaNs: " + str(columns_nan))
    return data
