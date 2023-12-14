import os
import shutil

# 2. Skullstrip all the N4 corrected T1w images - Note that the paper does not specify this step.

#An 'ignore' function to copy the directory tree without any of the files (nabbed from https://stackoverflow.com/questions/15663695/shutil-copytree-without-files)
def ig_f(dir, files):
    return [f for f in files if os.path.isfile(os.path.join(dir, f))]

shutil.copytree("./tessa-etal-2014/ANTs-derivatives/N4/pre_processing", "./tessa-etal-2014/ANTs-derivatives/SS", ignore=ig_f)

num_done = 0

# Loop over all the corrected T1w images and skullstrip them
for root, dirs, files in os.walk("./tessa-etal-2014/ANTs-derivatives/N4/pre_processing"):
    for file in files:
        if file.endswith("corrected_T1w.nii.gz"):
            raw_input = root + "/" + file
            output_path = raw_input.replace("N4/pre_processing", "SS")
            output_path = output_path.replace("corrected_T1w.nii.gz", "SS_corrected_T1w")
            command = "singularity run singuant_img.simg antsBrainExtraction.sh -d 3 -a " + raw_input + " -e ./OASIS-30_Atropos_template/OASIS-30_Atropos_template/T_template0.nii.gz -m ./OASIS-30_Atropos_template/OASIS-30_Atropos_template/T_template0_BrainCerebellumProbabilityMask.nii.gz -o " + output_path + " -f ./OASIS-30_Atropos_template/OASIS-30_Atropos_template/T_template0_BrainCerebellumRegistrationMask.nii.gz"
            num_done += 1
            print("Number done: " + str(num_done))
            print(command)
            print("\n")
            os.system(command)