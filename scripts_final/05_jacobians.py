import os
import shutil

#An 'ignore' function to copy the directory tree without any of the files (nabbed from https://stackoverflow.com/questions/15663695/shutil-copytree-without-files)
def ig_f(dir, files):
    return [f for f in files if os.path.isfile(os.path.join(dir, f))]

#######################################################################################################################
#BL_to_GT: Calculate Jacobian Determinant of the nonlinear component of the warpfield

input_dir = "./tessa-etal-2014/ANTs-derivatives/BL_to_GT"
output_path = "./tessa-etal-2014/ANTs-derivatives/jacobian_BL_to_GT"
shutil.copytree("./tessa-etal-2014/ANTs-derivatives/SS", output_path, ignore=ig_f)

for root, dirs, files in os.walk(input_dir):
    for file in files:
        if 'ses-BL' in root and file.endswith("BL2GT_1Warp.nii.gz"):
            input_t1 = root + "/" + file
            output_t1 = input_t1.replace("BL_to_GT", "jacobian_BL_to_GT")
            output_t1 = output_t1.replace("BL2GT_1Warp.nii.gz", "BL2GT_1Warp_jacobian.nii.gz")
            command = "singularity run ../singuant_img.simg CreateJacobianDeterminantImage 3 " + input_t1 + " " + output_t1
            os.system(command)


#######################################################################################################################
#FU_to_BL: Calculate Jacobian Determinant for nonlinear component of the inverse warpfield

input_dir = "./tessa-etal-2014/ANTs-derivatives/FU_to_BL"
output_path = "./tessa-etal-2014/ANTs-derivatives/jacobian_FU_to_BL"
shutil.copytree("./tessa-etal-2014/ANTs-derivatives/SS", output_path, ignore=ig_f)

for root, dirs, files in os.walk(input_dir):
    for file in files:
        if 'ses-BL' in root and file.endswith("FU2BL_1InverseWarp.nii.gz"):
            input_t1 = root + "/" + file
            output_t1 = input_t1.replace("FU_to_BL", "jacobian_FU_to_BL")
            output_t1 = output_t1.replace("FU2BL_1InverseWarp.nii.gz", "FU2BL_1InverseWarp_jacobian.nii.gz")
            command = "singularity run ../singuant_img.simg CreateJacobianDeterminantImage 3 " + input_t1 + " " + output_t1
            os.system(command)