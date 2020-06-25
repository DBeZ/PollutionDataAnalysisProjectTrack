'''
    Analysis of Israel Pollutant Release and Transfer Register (PRTR)
    Copyright (C) 2020  Doreen S. Ben-Zvi, PhD

    Full license is locates in License.txt at project root folder.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import os

import numpy as np
import pandas as pd

import data_conversion as dataconv
from load_data import load_data_from_csv
from save_data import save_as_pickel


# Returns column names with high number of unique values and ones with lower,
# as well as a dataframe with the unique values
def value_variability_check(dataframe, low_medium_variable_cutoff, medium_high_variable_cutoff):
    dataframe_value_dict = {}
    variable_columns = []
    highly_variable_columns = []
    for col in dataframe:
        unique_values = pd.unique(dataframe[col])
        unique_value_no = len(unique_values)
        if unique_value_no <= low_medium_variable_cutoff:
            dataframe_value_dict[col] = unique_values
        elif low_medium_variable_cutoff < unique_value_no and unique_value_no <= medium_high_variable_cutoff:
            variable_columns.append(col)
        else:
            highly_variable_columns.append(col)

    return dataframe_value_dict, variable_columns, highly_variable_columns


## Recursively finds the distinct values in a column,
## then separates the dataframe with the first value.
## and continues until each value has a new dataframe.
## Returns the list of sperate dataframes as well as the values
## used for separation.
def two_group_separator(dataframe, col, dataframes_list, rename_df=True):
    values = pd.unique(dataframe[col])
    if len(values) > 1:
        with_value = np.array(values[0] == dataframe[col])
        without_value = ~with_value
        df_with_value = dataframe.loc[with_value, :]
        df_without_value = dataframe.loc[without_value, :]
        # df_with_value = df_with_value.rename_axis(values[0], axis=1)
        if rename_df:
            df_with_value.name = values[0]
        else:
            df_with_value.name = dataframe.name
        dataframes_list.append(df_with_value)
        df = two_group_separator(df_without_value, col, dataframes_list)
    else:
        dataframes_list.append(dataframe)
        if rename_df:
            dataframe.name = values[0]
        else:
            dataframe.name = dataframe.name
        return dataframes_list
    return df


## Takes a dataframe and returns a seperate dataframe for each value in the specified column
def dataframe_by_column_value_separator(dataframe, col, rename_df=True):
    dataframes_list = []
    data_frame = pd.DataFrame()
    values = pd.unique(dataframe[col])
    if len(values) > 1:
        two_group_separator(dataframe, col, dataframes_list, rename_df)
        return dataframes_list, values
    else:
        return dataframe, values


# Searches if all values are in a given list
def are_all_values_in_list(value_list, list):
    counter = 0
    for value in value_list:
        if value in list:
            counter += 1
    if counter == len(value_list):
        return True
    else:
        return False


# Searches for values from a given list, in a given list
def are_values_in_list(value_list, list):
    counter = 0
    for value in value_list:
        if value in list:
            counter += 1
    if counter > 0:
        return True
    else:
        return False


## Finds values form the dictionary in the list
## Returns a list with the dictionary values found in the list
def values_which_are_in_list(dict_of_lists, value_list):
    result_dict = {}
    for k, values in enumerate(dict_of_lists):
        for value in dict_of_lists[values]:
            if value in value_list:
                if k not in result_dict:
                    result_dict[values + " " + str(k)] = [value]
                else:
                    result_dict[values + " " + str(k)].append(value)
        if result_dict == {}:
            return False
        else:
            return result_dict


## Finds the values which are non numbers in a df column
## reutrns the values in a list form
def find_non_number_values_in_column(series):
    non_num_values = []
    for entry in pd.unique(series):
        try:
            entry = entry.replace(',', '')
        except AttributeError:
            if isinstance(entry, str):
                non_num_values.append(entry)
        try:
            float(entry)
        except ValueError:
            non_num_values.append(entry)
    return non_num_values


## Finds the values which are non numbers in several df columns
## returns the values in a dictionary, one key for each column
def find_non_number_values_in_columns(dataframe, col_list):
    values_dict = {}
    for col in col_list:
        non_num_values = find_non_number_values_in_column(dataframe[col])
        if non_num_values != []:
            values_dict[col] = non_num_values
    return values_dict


# Removes comma from numbers
def comma_removal(dataframe, columns):
    comma_removed_from_col = []
    for col in columns:
        if (col in dataframe.columns) and (dataframe[col].dtype == np.object):
            dataframe.loc[dataframe[col].isnull(), col] = "נתון לא זמין"
            dataframe[col] = dataframe[col].map(lambda x: x.replace(",", ""))
            comma_removed_from_col.append(col)
    return dataframe, comma_removed_from_col


# Convert dataframe columns to float
def convert_to_numeric(dataframe, column_list):
    for col in column_list:
        if col in dataframe.columns:
            dataframe[col] = pd.to_numeric(dataframe[col], downcast="float")
    return dataframe


# Corrects Nans and specific emission column data
def data_value_cleaining(all_data):
    all_data["KamutPlitaLoBeTeunot"] = 0
    all_data["PsoletMesukenetTotal"] = np.NaN
    all_data["PsoletLoMesukenetTotal"] = np.NaN

    # df_categories, variable_columns, highly_variable_columns = value_variability_check(dataframe=all_data,
    #                                                                                    low_medium_variable_cutoff=20,
    #                                                                                    medium_high_variable_cutoff=200)

    # Remove comma from number values
    cols_for_comma_removal = ["KamutPlita", "KamutPlitaBeTeunot"]
    all_data, comma_removed_from_col = comma_removal(dataframe=all_data, columns=cols_for_comma_removal)

    column_list = ["KamutPlita", "KamutPlitaBeTeunot"]
    # KamutPlita is Total emissions
    # KamutPlitaBeTeunot is emissions in accidents
    non_nums_in_cols_dict = find_non_number_values_in_columns(dataframe=all_data, col_list=column_list)
    # non_nums_in_cols_dict contains two special types of values.
    values_dict = {
        "too_low_values": ['פליטה נמוכה מכמות הסף', 'הזרמה נמוכה מכמות הסף'],
        "non_accident_values": ['לא נפלט בתקלה', 'לא הוזרם בתקלה'],
        "unavailable": ["נתון לא זמין"]
    }

    mask = (all_data["KamutPlita"] == values_dict["unavailable"][0])
    all_data.loc[mask, "KamutPlita"] = np.nan
    mask = (all_data["KamutPlitaBeTeunot"] == values_dict["unavailable"][0])
    all_data.loc[mask, "KamutPlitaBeTeunot"] = np.nan

    # if KamutPlita and KamutPlitaBeTeunot are too_low_values:
    # KamutPlita is Nan
    # KamutPlitaBeTeunot is Nan
    # KamutPlitaLoBeTeunot are Nan,
    # Accidental = 1
    mask1 = (((all_data["KamutPlita"] == values_dict["too_low_values"][0]) | (
            all_data["KamutPlita"] == values_dict["too_low_values"][1])) & (
                     (all_data["KamutPlitaBeTeunot"] == values_dict["too_low_values"][0]) | (
                     all_data["KamutPlitaBeTeunot"] == values_dict["too_low_values"][1])))

    # if KamutPlita is in too_low_values and KamutPlitaBeTeunot is non_accident_values:
    # KamutPlita is Nan
    # KamutPlitaBeTeunot is None
    # KamutPlitaLoBeTeunot are Nan,
    # Accidental = 0
    mask2 = (((all_data["KamutPlita"] == values_dict["too_low_values"][0]) | (
            all_data["KamutPlita"] == values_dict["too_low_values"][1])) & (
                     (all_data["KamutPlitaBeTeunot"] == values_dict["non_accident_values"][0]) | (
                     all_data["KamutPlitaBeTeunot"] == values_dict["non_accident_values"][1])))

    # if KamutPlita is in too_low_values and KamutPlitaBeTeunot is numeric:
    # KamutPlita is Nan
    # KamutPlitaBeTeunot is Nan
    # KamutPlitaLoBeTeunot are Nan,
    # Accidental = 1
    mask3 = ((all_data["KamutPlita"] == values_dict["too_low_values"][0]) | (
            all_data["KamutPlita"] == values_dict["too_low_values"][1]))
    mask4 = mask3 & (~(mask1 & mask2))

    # if KamutPlita is numeric and KamutPlitaBeTeunot  in too_low_values:
    # KamutPlita is unchanged
    # KamutPlitaBeTeunot is Nan
    # KamutPlitaLoBeTeunot are --> KamutPlita,
    # Accidental = 1
    mask5 = ((all_data["KamutPlitaBeTeunot"] == values_dict["too_low_values"][0]) | (
            all_data["KamutPlitaBeTeunot"] == values_dict["too_low_values"][1]))
    mask6 = mask5 & (~(mask3))

    # if KamutPlita is numeric and KamutPlitaBeTeunot  is non_accident_values:
    # KamutPlita is unchanged
    # KamutPlitaBeTeunot is Non
    # KamutPlitaLoBeTeunot are --> KamutPlita,
    # Accidental = 0
    mask7 = ((all_data["KamutPlitaBeTeunot"] == values_dict["non_accident_values"][0]) | (
            all_data["KamutPlitaBeTeunot"] == values_dict["non_accident_values"][1]))
    mask8 = mask7 & (~(mask3))

    all_data.loc[mask1, "KamutPlita"] = np.nan
    all_data.loc[mask1, "KamutPlitaBeTeunot"] = np.nan
    all_data.loc[mask1, "KamutPlitaLoBeTeunot"] = np.nan
    all_data.loc[mask1, "Accidental"] = True

    all_data.loc[mask2, "KamutPlita"] = np.nan
    all_data.loc[mask2, "KamutPlitaBeTeunot"] = np.nan  # None
    all_data.loc[mask2, "KamutPlitaLoBeTeunot"] = np.nan
    all_data.loc[mask2, "Accidental"] = False

    all_data.loc[mask4, "KamutPlita"] = np.nan
    all_data.loc[mask4, "KamutPlitaBeTeunot"] = np.nan
    all_data.loc[mask4, "KamutPlitaLoBeTeunot"] = np.nan
    all_data.loc[mask4, "Accidental"] = True

    all_data.loc[mask6, "KamutPlitaBeTeunot"] = np.nan
    all_data.loc[mask6, "KamutPlitaLoBeTeunot"] = all_data.loc[mask6, "KamutPlita"]
    all_data.loc[mask6, "Accidental"] = True

    all_data.loc[mask8, "KamutPlitaBeTeunot"] = np.nan  # None
    all_data.loc[mask8, "KamutPlitaLoBeTeunot"] = all_data.loc[mask8, "KamutPlita"]
    all_data.loc[mask8, "Accidental"] = False

    columns_to_convert = comma_removed_from_col + ["KamutPlitaLoBeTeunot"]

    all_data = convert_to_numeric(dataframe=all_data, column_list=columns_to_convert)

    all_data["PsoletMesukenetTotal"] = all_data["SachTipulPsoletMesukenet"] + all_data["SachSilukPsoletMesukenet"]
    all_data["PsoletLoMesukenetTotal"] = all_data["SachTipulPsoletLoMesukenet"] + all_data["SachSilukPsoletLoMesukenet"]

    return all_data


# Loads data, cleans it and pickles the result
def data_cleaning(file_to_load, pickel_name, output_folder_name):
    data_df = load_data_from_csv(file_to_load)
    data_df = dataconv.clean_data_ui(data_df)  # Removes columns and adjusts data types
    save_as_pickel(dataframe=data_df, output_folder_name=output_folder_name, save_file_name=pickel_name)


# Load dataframe from csv, clean it and immediately pickle it
def load_csv_then_pickle(csv_file_name, output_folder_name, pickle_file_name):
    working_direcotry = os.getcwd()
    os.chdir(output_folder_name)
    data = load_data_from_csv(csv_file_name)
    data = dataconv.clean_data_ui(data)
    save_as_pickel(data, output_folder_name, pickle_file_name)
    os.chdir(working_direcotry)


# shorten name for display
def shorten_name(dataframe, col, how_short):
    dataframe[col] = dataframe[col].str[:how_short]
    return dataframe


# Shorten product names for display
def shorten_product_name(dataframe, product_col):
    keys = [
        "74 - טיפול ועיבוד חלב בלבד, אם כמות תשומת החלב עולה על 200 טון ליום",
        "72 - שחיטה של בעלי חיים בקיבולת של 50 טון ליום",
        "20 - ייצור מלט באמצעות כבשנים סובבים (Rotary Kilns) בעלי כושר ייצור של 500 טון ליום, או בכבשנים אחרים (furnaces) בעלי כושר ייצור של 50 טון ליום",
        "19 - ייצור אספלט",
        "14 - ייצור והפקה של מתכות לא ברזיליות גולמיות ממחצבים, עופרות, תרכיזים, או חומרי גלם שניוניים על ידי תהליכים מטאלורגיים, כימיים או אלקטרוליטיים",
        "56 - פעילות שנעשה בה שימוש במיתקנים לטיפול או סילוק של שפכים בספיקה של 1,000 מטר מעוקב ליום",
        "52 - טיפול או שילוב של טיפול וסילוק, של פסולת לא מסוכנת בקיבולת של 50 טון ליום הכוללת אחת או יותר מפעילויות המנויות, למעט טיפול בשפכים שאינם שפכי תעשייה",
        "28 - ייצור פחממנים המכילים חמצן כגון אלכוהולים, אלדהידים, קטונים, חומצות קרבוקסיליות, אסטרים, אצטטים, אתרים, פרוקסידים, שרפים אפוקסים",
        "53 - תפעול מטמנות בקיבולת של 10 טון ליום או בקיבולת כללית העולה על 25,000 טון",
        "54 - מיתקן נייח וקבוע שבו נעשת העברה של פסולת או מיון של פסולת לרכיביה",
        "70 - מיתקנים לגידול עופות בקיבולת של 40,000 עופות",
        "41 - ייצור מלחים כגון אמוניום כלוריד, פוטסיום כלורט, פוטסיום קרבונט, סודיום קרבונט, פרבורט, ניטרט כסף (Silver nitrate)",
        "68 - התפלת מים בספיקה של 30 מיליון מטר מעוקב בשנה",
        "16 - טיפול פני השטח של מתכות וחומרים פלסטיים על ידי תהליך כימי או אלקטרוליטי באמבטיות טיפול שנפחן הכולל 30 מטר מעוקב",
        "59 - ייצור נייר וקרטון בכושר ייצור העולה על 20 טון ליום",
        "21 - ייצור סיד בכבשנים בעלי כושר ייצור של  50 טון ליום",
        "55 - פעילות שנעשה בה שימוש במיתקנים לכילוי או מיחזור של פגרי בעלי חיים ופסדים, בקיבולת של 10 טון ליום",
        "18 - מחצבות פתוחות (Open cast mining),",
        "73 - טיפול ועיבוד, של חומרי גלם מהחי או מהצומח, בין אם עובדו קודם לכן ובין אם לא, המיועדים לייצור מוצרי מזון, משקאות או מזון לבעלי חיים",
        "47 - טיפול או סילוק של פסולת מסוכנת בכמות של 10 טון ליום באמצעות הפעילויות המנויות",
        "02 - הפקת דלקים במצב צבירה גז, נוזל או מוצק, בקנה מידה תעשייתי",
        "45 - תהליכים כימיים וביולוגיים לייצור מוצרים  פרמצבטיים כולל חומרי ביניים",
        "15 - התכה, כולל סגסוגות (alloyage), של מתכות לא ברזיליות, כולל מוצרים מוחזרים והפעלת בתי יציקה למתכות לא ברזיליות בכושר התכה העולה על 4 טון ליום לעופרת וקדמיום ו-20 טון ליום לכל שאר המתכות",
        "64 - טיפול פני שטח של חומרים, רכיבים או מוצרים, באמצעות  ממיסים אורגניים בכמות של 150 קילוגרם לשעה או 200 טון לשנה, במיוחד להדפסה, ציפוי, ניקוי משמנים, עמידות למים, צביעה, ניקוי או אימפרגנציה וכדומה",
        "06 - פעילות שנעשה בה שימוש במיתקן שריפה בהספק תרמי של  50 מגה וואט",
        "09 - פעילות שנעשה בה שימוש במיתקנים לייצור ברזל גולמי או פלדה (התכה ראשונית או שניונית) ובכלל זה יציקה רציפה, בעלי כושר ייצור של 2.5 טון לשעה",
        "51 - סילוק של פסולת לא מסוכנת בקיבולת של 50 טון ליום הכוללת אחת או יותר מפעילויות המנויות, למעט טיפול בשפכים שאינם שפכי תעשייה:",
        "27 - ייצור פחממנים פשוטים (לינארים או ציקלים, רוויים ושאינם רוויים, אליפטים או ארומטיים)",
        "38 - ייצור גזים כגון אמוניה, כלור או מימן כלורי, פלואור או מימן פלואורי, תחמוצות פחמן, תרכובות גופרית, תחמוצות חנקן, מימן, דו-תחמוצת הגפרית, קרבוניל כלוריד",
        "69 - מיתקנים לגידול אינטנסיבי של חזירים בקיבולת של 2,000 חזירים (אשר משקלם עולה על 30 קילוגרם) או 750  חזירות (נקבות)",
        "71 - מיתקנים לגידול דגים או רכיכות בקיבולת של 1,000 טון דגים או רכיכות לשנה",
        "23 - פעילות שנעשה בה שימוש במיתקנים ליצור זכוכית כולל סיבי זכוכית, בעלי כושר המסה של 20 טון ליום",
        "44 - ייצור ביוצידים (נגד מיקרואורגניזמים) או מוצרים בסיסיים להגנת הצומח",
        "34 - ייצור חומרים פלסטיים (פולימרים, סיבים סינתטיים וסיבים המבוססים על צלולוס)",
        "39 - ייצור חומצות כגון חומצה כרומית, חומצה הידרופלואורית, חומצה זרחתית, חומצה חנקתית, חומצה הידרוכלורית, חומצה גפרתית, אולאום (Oleum), חומצות גפריתיות",
        "10 - פעילות שנעשה בה שימוש במיתקני ערגול בכושר ייצור של  20 טון פלדה גולמית לשעה",
        "26 - פעילות שנעשה בה שימוש במיתקנים ליצור מוצרים קרמים על ידי שריפה, כגון רעפים, לבנים, אריחים או פורצלן, בעלי כושר ייצור של 75 טון ליום או עם כבשנים בעלי נפח של 4 מטרים מעוקבים ועם צפיפות השמה לכבשן של 300 קילוגרם למטר מעוקב",
        "42 - ייצור תרכובות אנאורגניות לא מתכתיות או תחמוצות מתכת או תרכובות אנאורגניות אחרות כגון סידן קרביד, סיליקון, סיליקון קרביד",
        "43 - ייצור דשנים המבוססים על זרחן, חנקן או אשלגן (תרכובות פשוטות או מורכבות)",
        "57 - טיפול או סילוק של שפכים שהם תוצר של פעילויות מהסוגים המפורטים בטור ב' לתוספת זו",
        "32 - ייצור פחממנים הלוגנים",
        "01 - זיקוק גז ודלקים",
        "37 - ייצור חומרים פעילי שטח ודטרגנטים",
        "12 - יישום גלוון או ציפוי מתכת (fused metal coats) בכושר ייצור של 2 טון פלדה גולמית לשעה",
        "58 - ייצור עיסה מעץ או מחומרים סיביים אחרים",
        "50 - סילוק או טיפול בפסולת במיתקנים לשריפה או לטיפול תרמי, בפסולת לא מסוכנת – בקיבולת של 3 טון לשעה, ובפסולת מסוכנת – בקיבולת של 10 טון ליום",
        "62 - פעילויות מקדימות כגון שטיפה, הלבנה, מירצור או צביעת חוטים או טקסטיל, בכושר ייצור של 10 טון ליום",
        "13 - פעילות שנעשה בה שימוש בבתי יציקה של מתכות ברזיליות בכושר ייצור של 20 טון ליום"
    ]

    values = [
        "74- טיפול ועיבוד חלב בלבד",
        "72- שחיטה של בעלי חיים",
        "20- ייצור מלט באמצעות כבשנים סובבים או בכבשנים אחרים",
        "19- ייצור אספלט",
        "14- ייצור והפקה של מתכות לא ברזיליות גולמיות",
        "56- פעילות שנעשה בה שימוש במיתקנים לטיפול או סילוק של שפכים",
        "52- טיפול או שילוב של טיפול וסילוק, של פסולת לא מסוכנת למעט טיפול בשפכים שאינם שפכי תעשייה",
        "28- ייצור פחממנים",
        "53- תפעול מטמנות",
        "54- מיתקן נייח וקבוע שבו נעשת העברה של פסולת או מיון של פסולת לרכיביה",
        "70- מיתקנים לגידול עופות",
        "41- ייצור מלחים",
        "68- התפלת מים",
        "16- טיפול פני השטח של מתכות וחומרים פלסטיים",
        "59- ייצור נייר וקרטון",
        "21- ייצור סיד בכבשנים",
        "55- פעילות שנעשה בה שימוש במיתקנים לכילוי או מיחזור של פגרי בעלי חיים ופסדים",
        "18- מחצבות פתוחות",
        "73- טיפול ועיבוד, של חומרי גלם מהחי או מהצומח,לייצור מוצרי מזון, משקאות או מזון לבעלי חיים",
        "47- טיפול או סילוק של פסולת מסוכנת",
        "2- הפקת דלקים במצב צבירה גז, נוזל או מוצק, בקנה מידה תעשייתי",
        "45- תהליכים כימיים וביולוגיים לייצור מוצרים  פרמצבטיים כולל חומרי ביניים",
        "15- התכה, כולל סגסוגות של מתכות לא ברזיליות",
        "64- טיפול פני שטח של חומרים, רכיבים או מוצרים, באמצעות  ממיסים אורגניים",
        "6- פעילות שנעשה בה שימוש במיתקן שריפה",
        "9- פעילות שנעשה בה שימוש במיתקנים לייצור ברזל גולמי או פלדה",
        "51- סילוק של פסולת לא מסוכנת למעט טיפול",
        "27- ייצור פחממנים פשוטים",
        "38- ייצור גזים",
        "69- מיתקנים לגידול אינטנסיבי של חזירים",
        "71- מיתקנים לגידול דגים או רכיכות",
        "23- פעילות שנעשה בה שימוש במיתקנים ליצור זכוכית כולל סיבי זכוכית",
        "44- ייצור ביוצידים או מוצרים בסיסיים להגנת הצומח",
        "34- ייצור חומרים פלסטיים",
        "39- ייצור חומצות",
        "10- פעילות שנעשה בה שימוש במיתקני ערגול",
        "26- פעילות שנעשה בה שימוש במיתקנים ליצור מוצרים קרמים",
        "42- ייצור תרכובות אנאורגניות",
        "43- ייצור דשנים",
        "57- טיפול או סילוק של שפכים",
        "32- ייצור פחממנים הלוגנים",
        "1- זיקוק גז ודלקים",
        "37- ייצור חומרים פעילי שטח ודטרגנטים",
        "12- יישום גלוון או ציפוי מתכת",
        "58- ייצור עיסה מעץ או מחומרים סיביים אחרים",
        "50- סילוק או טיפול בפסולת במיתקנים לשריפה או לטיפול תרמי, בפסולת לא מסוכנת או בפסולת מסוכנת",
        "62- פעילויות מקדימות כגון שטיפה, הלבנה, מירצור או צביעת חוטים או טקסטיל",
        "13- פעילות שנעשה בה שימוש בבתי יציקה של מתכות ברזיליות"
    ]

    product_dict = dict(zip(keys, values))
    dataframe = dataframe.replace({product_col: product_dict})
    return dataframe


##############
# Archiology #
##############
# def two_group_separator(dataframe, col, values):
#     if isinstance(values,list):
#         for k, entry in enumerate(values):
#             mask=np.array(entry == dataframe[col])
#             if k==0:
#                 with_value=np.array(entry == dataframe[col])
#             else:
#                 with_value=with_value | mask
#         with_value=with_value.astype(bool)
#         without_value=~with_value
#         df_with_value = dataframe.loc[with_value, :]
#         df_without_value = dataframe.loc[without_value, :]
#         return df_with_value,df_without_value
#     if isinstance(values,dict):
#         for k, entry in enumerate(values):
#             for value in entry:
#                 mask=np.array(value == dataframe[col])
#                 if k==0:
#                     with_value=np.array(value == dataframe[col])
#                 else:
#                     with_value=with_value | mask
#         with_value=with_value.astype(bool)
#         without_value=~with_value
#         df_with_value = dataframe.loc[with_value, :]
#         df_without_value = dataframe.loc[without_value, :]
#         return df_with_value,df_without_value

# def separate_col_string_or_num(dataframe, col, non_num_values):
#     df_with_string,df_with_number=two_group_separator(dataframe=dataframe, col=col, value_list=non_num_values)
#     separate_col_string_or_num(dataframe=dataframe, col=col)
#     return df_with_string,df_with_number,
#     df_with_string, df_with_number = two_group_separator(dataframe=dataframe, col=col, value_list=non_num_values)
#     for df in ( df_with_string, df_with_number):
#         separate_col_string_or_num(df, col, )
#
#     separate_col_string_or_num()
#
#     if non_num_values == []:
#         return values_dict,

# def separate_string_rows(dataframe, col_list, significant_values_dict):
#     values_dict={}
#     for col in col_list:
#         non_num_values = find_non_number_values_in_column(dataframe[col])
#         result_dict = values_which_are_in_list(significant_values_dict, non_num_values)
#         if result_dict != {}:
#             values_dict.update(result_dict)
#         else:
#             values_dict[col] = non_num_values
#         if non_num_values == []:
#             return values_dict

if __name__ == "__main__":
    data_cleaning(file_to_load="MIFLAS_data.csv", pickel_name="testpickle", output_folder_name="Output_files")
