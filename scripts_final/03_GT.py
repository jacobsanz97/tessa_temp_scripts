import os
import random
import shutil

# 2. Create Group Template

# Patient numbers for PD and HC groups
PD_patno_list = [3123, 3124, 3127, 3128, 3179, 3556, 3585, 3778, 3787, 3831, 3832, 3869, 4005, 4013, 4020, 4021, 4026, 4030, 4037, 4083, 40366, 59507]
HC_patno_list = [3106, 3301, 3316, 3350, 3353, 3357,3369, 3563, 3565, 3569, 3571, 3851, 3852, 3853, 3855, 3857, 4085]

# Watch out! Upon manual inspection 3869-V06 and 3857-BL raw scans are corrupted.
# remove 3857 from HC_patno_list, 3869 from PD_patno_list
HC_patno_list.remove(3857)
PD_patno_list.remove(3869)

# Choose 17 random subjects from PD_patno_list --> choose 16 due to corrupted 3869
random.seed(1)
PD_patno_subset_rndm = random.sample(PD_patno_list, 16)

GT_input_list = HC_patno_list + PD_patno_subset_rndm
GT_input_root = "./SS"

for patno in GT_input_list:
    GT_input_list[GT_input_list.index(patno)] = GT_input_root + "/" + "sub-" + str(patno) + "/ses-BL/anat/" + "SS_corrected_T1wBrainExtractionBrain.nii.gz"

GT_input_list_string = ""
for t1 in GT_input_list:
    GT_input_list_string = t1 + " " + GT_input_list_string

os.system("mkdir ./GT")
GT_command = "singularity run singuant_img.simg antsMultivariateTemplateConstruction.sh -d 3 -c 0 -n 0 -i 5 -o " + "./GT/GT_ " + GT_input_list_string
os.system(GT_command)
