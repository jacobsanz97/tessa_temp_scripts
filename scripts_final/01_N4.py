import os
import random
import shutil

#os.system("mkdir ./tessa-etal-2014/ANTs-derivatives")

################################################################################################################################################################################
# 1. N4 Bias Field Correction

#An 'ignore' function to copy the directory tree without any of the files (nabbed from https://stackoverflow.com/questions/15663695/shutil-copytree-without-files)
def ig_f(dir, files):
    return [f for f in files if os.path.isfile(os.path.join(dir, f))]

shutil.copytree("./tessa-etal-2014/outputs", "./tessa-etal-2014/ANTs-derivatives/N4", ignore=ig_f) #copy inputs directory tree (without T1 files) to derivatives directory
os.system("rm -r ./tessa-etal-2014/ANTs-derivatives/N4/study_files") #delete the study_files directory that is not needed right now

# loop over every directory in ./tessa-etal-2014/outputs, and run N4BiasFieldCorrection on each T1 file, store output in derivatives directory
for root, dirs, files in os.walk("./tessa-etal-2014/outputs/"):
    for file in files:
        if file.endswith(".nii.gz"):
            raw_input = root + "/" + file
            output_path = root.replace("outputs", "ANTs-derivatives/N4")
            output_param = " -o [ " + output_path+"/corrected_T1w.nii.gz, " + output_path+"/T1w_BiasField.nii.gz ]"
            command = "singularity run singuant_img.simg N4BiasFieldCorrection -d 3 -v 1 -s 4 -b [ 180 ] -c [ 50x50x50x50, 0.0 ] -i " + raw_input + output_param
            print(command)
            print("\n")
            os.system(command)