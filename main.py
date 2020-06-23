from save_data import create_output_folder
from load_data import load_data_from_pickle
from data_cleaning import data_value_cleaining, data_cleaning, shorten_product_name
import generators
import os



#########################
# Data Analysis project #
# Project Course        #
# Doreen Ben-Zvi PhD    #
# Jun 2020              #
#########################

def main():
    file_name = "MIFLAS_data.csv"
    pickel_name = "cleanData"
    output_folder_name = "Output_files"
    working_direcotry = os.getcwd()
    create_output_folder(foldername=output_folder_name)
    # check if pickle file exists.
    if os.path.isfile(os.getcwd() + "\\" + output_folder_name + "\\" + pickel_name + ".pkl"):
        data_df = load_data_from_pickle(pickle_file_name=pickel_name, output_folder_name=output_folder_name)
    else:

        data_cleaning(file_to_load=file_name, pickel_name=pickel_name,
                      output_folder_name=output_folder_name)  # Removes columns and adjusts data types
        data_df = load_data_from_pickle(pickle_file_name=pickel_name, output_folder_name=output_folder_name)

    data_df = shorten_product_name(dataframe=data_df, product_col="SugPeilutAtarSvivati")
    cleaned_df = data_value_cleaining(data_df)

    os.chdir(output_folder_name)
    ## Initial visualization of accidental and non accidental emissions- shotgun approach
    # generators.accidents_non_accidents_shotgun(data=data_df,x_val_col='SugPeilutAtarSvivati', is_log=False)
    # generators.accidents_non_accidents_shotgun(data=data_df,x_val_col=x_val_col='TchumPeilutAtarSvivati', is_log=False)
    # generators.accidents_non_accidents_shotgun(data=data_df,x_val_col='SugPeilutAtarSvivati', is_log=True)
    # generators.accidents_non_accidents_shotgun(data=data_df,x_val_col=x_val_col='TchumPeilutAtarSvivati', is_log=True)

    ## Industries with most accidents
    # generators.accident_analysis_ui(data=cleaned_df)

    os.chdir(working_direcotry)


    ## Industial geographical clusters
    generators.industry_geoloc(data=cleaned_df, city_col="YeshuvAtarSvivatiMenifa", industry_col="AnafAtarSvivati", pivot_by="YeshuvAtarSvivatiMenifa", values="AnafAtarSvivati")
    generators.industry_geoloc(data=cleaned_df, city_col="YeshuvAtarSvivatiMenifa", industry_col="TchumPeilutAtarSvivati", pivot_by="YeshuvAtarSvivatiMenifa", values="AnafAtarSvivati")



    print("Done")


# Make sure main cannot be called from other functions
if __name__ == "__main__":
    main()
