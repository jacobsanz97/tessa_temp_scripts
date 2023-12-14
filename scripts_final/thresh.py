import nibabel as nib  
import numpy as np
import os

def niftii_threshold(niftii_path, threshold, output_path):
    # Load the niftii file
    niftii = nib.load(niftii_path)
    affine = niftii.affine
    header = niftii.header
    # Get the data from the niftii file
    data = niftii.get_fdata()
    # Apply the threshold to the data
    data[data <= threshold] = 0
    # Save the data back to the niftii file
    niftii2 = nib.Nifti1Image(data, niftii.affine, niftii.header)
    # Save the niftii file to disk
    nib.save(niftii2, output_path)
    print("Saved thresholded niftii file to " + output_path)

input_path = "/home/jacob/Desktop/analysis/map2mni_nn"
output_path = "/home/jacob/Desktop/analysis/map2mni_nn_thresh"

#loop through all files in input_path, and apply threshold to the ones ending in 'Warped.nii.gz', save to output_path
for root, dirs, files in os.walk(input_path):
    for file in files:
        if file.endswith("Warped.nii.gz"):
            print("Thresholding " + file)
            niftii_threshold(input_path + "/" + file, 0.95, output_path + "/" + file)