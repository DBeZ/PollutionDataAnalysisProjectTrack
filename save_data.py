import datetime as dt
import os

#################
# File handling #
#################

# Create folder
def create_output_folder(foldername):
    if not os.path.isdir(foldername):  # os.path.exists('mydirectory')
        os.mkdir(foldername)


# Export a dataframe to csv
def export_to_csv(dataframe, save_file_name, output_folder_name=os.getcwd(), encoding='utf-8-sig'):
    if not os.path.isdir(output_folder_name):
        os.mkdir(output_folder_name)
    os.chdir(output_folder_name)
    now = str(dt.datetime.now().strftime("%y%m%d %H_%M"))
    if not os.path.isdir("Output_files"):
        os.mkdir("Output_files")
    os.chdir("Output_files")
    dataframe.to_csv(os.getcwd() + "\\" + save_file_name + now + ".csv", index=True, header=True, encoding=encoding)
    os.chdir("..")
    print("Results saved as csv")


# Picke a dataframe
def save_as_pickel(dataframe, save_file_name, output_folder_name=os.getcwd()):
    if not os.path.isdir(output_folder_name):
        os.mkdir(output_folder_name)
    os.chdir(output_folder_name)
    dataframe.to_pickle("./" + save_file_name + ".pkl")  # Can be skipped after sucessful query and pickle save
    os.chdir("..")
    print("Results pickled")
