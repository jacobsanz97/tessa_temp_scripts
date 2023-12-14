import nibabel as nib
import numpy as np
import os
import shutil

input_dir = "./tessa-etal-2014/ANTs-derivatives/jacobian_FU_to_BL"
output_dir = "./tessa-etal-2014/ANTs-derivatives/WR"

def WR_calc(jacobian_filepath, output_filepath, t):
    jacobian = nib.load(jacobian_filepath)
    data = jacobian.get_fdata()
    data = data - 1
    data = np.divide(data, t)
    new_img = nib.Nifti1Image(data, jacobian.affine, jacobian.header)
    nib.save(new_img, output_filepath)

def ig_f(dir, files):
    return [f for f in files if os.path.isfile(os.path.join(dir, f))]

shutil.copytree("./tessa-etal-2014/ANTs-derivatives/SS", output_dir, ignore=ig_f)

count = 0

for root, dirs, files in os.walk(input_dir):
    for file in files:
        if 'ses-BL' in root and file.endswith("InverseWarp_jacobian.nii.gz"):
            input_jacobian = root + "/" + file
            print("input_jacobian: " + input_jacobian)
            output_wr = input_jacobian.replace("jacobian_FU_to_BL", "WR")
            output_wr = output_wr.replace("FU2BL_1InverseWarp_jacobian.nii.gz", "FU2BL_1InverseWarp_jacobian_WR.nii.gz")
            if os.path.isdir(root.replace("ses-BL", "ses-V06")):
                t=2
            if os.path.isdir(root.replace("ses-BL", "ses-V10")):
                t=4
            print("t: " + str(t))
            WR_calc(input_jacobian, output_wr, t)
            print("outputted WR: " + output_wr)
            #add a line with total succesful
            count += 1
            print("count: " + str(count))
            print(" ")
