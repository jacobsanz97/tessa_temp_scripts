#Register WR to GT: Reusing BL mat and warp

import os
import shutil
import logging

def ig_f(dir, files):
    return [f for f in files if os.path.isfile(os.path.join(dir, f))]


fixed_GT = "./tessa-etal-2014/ANTs-derivatives/GT/GT_template0.nii.gz"
input_dir = "./tessa-etal-2014/ANTs-derivatives/WR"
transform_dir = "./tessa-etal-2014/ANTs-derivatives/BL_to_GT"
output_dir = "./tessa-etal-2014/ANTs-derivatives/WR_to_GT"

shutil.copytree("./tessa-etal-2014/ANTs-derivatives/SS", output_dir, ignore=ig_f)


for root, dirs, files in os.walk(input_dir):
    for file in files:
        if 'ses-BL' in root and file.endswith("InverseWarp_jacobian_WR.nii.gz"):

            moving_t1 = root + "/" + file

            output_path = moving_t1.replace("/WR/", "/WR_to_GT/")
            output_path = output_path.replace("FU2BL_1InverseWarp_jacobian_WR.nii.gz", "WR2GT_1InverseWarp_jacobian_WR.nii.gz")

            warp_t = moving_t1.replace("/WR/", "/BL_to_GT/")
            warp_t = warp_t.replace("FU2BL_1InverseWarp_jacobian_WR.nii.gz", "BL2GT_1Warp.nii.gz")

            affine_t = moving_t1.replace("/WR/", "/BL_to_GT/")
            affine_t = affine_t.replace("FU2BL_1InverseWarp_jacobian_WR.nii.gz", "BL2GT_0GenericAffine.mat")
            
            command = "singularity run ./singuant_img.simg antsApplyTransforms -d 3 -i FU2BL_1InverseWarp_jacobian_WR.nii.gz -r GT_template0.nii.gz -o result.nii.gz -t Warp.nii.gz -t GenericAffine.mat -n NearestNeighbor"
            
            command = command.replace("FU2BL_1InverseWarp_jacobian_WR.nii.gz",  moving_t1)
            command = command.replace("GT_template0.nii.gz", fixed_GT)
            command = command.replace("result.nii.gz", output_path)
            command = command.replace("Warp.nii.gz", warp_t)
            command = command.replace("GenericAffine.mat", affine_t)

            print(command)
            os.system(command)
            print(" ")
