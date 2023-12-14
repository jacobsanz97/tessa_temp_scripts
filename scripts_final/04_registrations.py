import os
import shutil

import logging 
logging.basicConfig(filename="std.log", 
					format='%(asctime)s %(message)s', 
					filemode='w') 
logger=logging.getLogger()
logger.setLevel(logging.DEBUG) 



#An 'ignore' function to copy the directory tree without any of the files (nabbed from https://stackoverflow.com/questions/15663695/shutil-copytree-without-files)
def ig_f(dir, files):
    return [f for f in files if os.path.isfile(os.path.join(dir, f))]

################################################################################################################################################################################
# Register all the corrected, skullstripped, T1w BaseLine images to the Group Template (BL_to_GT)
logger.info("Starting BL_to_GT") 

GT_path = "./tessa-etal-2014/ANTs-derivatives/GT/GT_template0.nii.gz"
input_dir = "./tessa-etal-2014/ANTs-derivatives/SS"

output_path = "./tessa-etal-2014/ANTs-derivatives/BL_to_GT"
shutil.copytree("./tessa-etal-2014/ANTs-derivatives/SS", output_path, ignore=ig_f)

counter = 0

for root, dirs, files in os.walk(input_dir):
    for file in files:
        if 'ses-BL' in root and file.endswith("BrainExtractionBrain.nii.gz"):
            counter += 1
            input_t1 = root + "/" + file
            output_reg_path = input_t1.replace("SS", "BL_to_GT")
            output_reg_path1 = output_reg_path.replace("BL_to_GT_corrected_T1wBrainExtractionBrain.nii.gz", "BL2GT_")
            output_reg_path2 = output_reg_path.replace("BL_to_GT_corrected_T1wBrainExtractionBrain.nii.gz", "BL2GT_Warped.nii.gz")
            command = "singularity run ./singuant_img.simg antsRegistration --dimensionality 3 --float 0 --output ["+output_reg_path1+","+output_reg_path2+"] --interpolation Linear --winsorize-image-intensities [0.005,0.995] --use-histogram-matching 0 --initial-moving-transform [$template,t1_biascorr.nii.gz,1] --transform Affine[0.1] --metric MI[$template,t1_biascorr.nii.gz,1,32,Regular,0.25] --convergence [1000x500x250x100,1e-6,10] --shrink-factors 8x4x2x1 --smoothing-sigmas 3x2x1x0vox --transform SyN[0.1,3,0] --metric CC[$template,t1_biascorr.nii.gz,1,4] --convergence [200x140x100x40,1e-6,10] --shrink-factors 8x4x2x1 --smoothing-sigmas 3x2x1x0vox -v"
            command = command.replace("$template", GT_path)
            command = command.replace("t1_biascorr.nii.gz", input_t1)

            launch_script = "launch" + str(counter) + ".sh"
            os.system("echo '#!/bin/bash' >> " + launch_script)
            os.system("echo '#SBATCH --time=120:00:00' >> " + launch_script)
            os.system("echo '#SBATCH --account=def-jbpoline' >> " + launch_script)
            os.system("echo '#SBATCH --mem-per-cpu=32768M' >> " + launch_script)
            os.system("echo 'module load apptainer/1.1'  >> " + launch_script)
            os.system("""echo 'export APPTAINER_BIND="/lustre04/scratch/jacobsr"' >> """ + launch_script)

            os.system("echo '" + command + "' >> " + launch_script)
            os.system("sbatch " + launch_script)
            logger.info(input_t1)   

################################################################################################################################################################################
# Register all the N4 corrected, skullstripped, T1w FollowUp images to the BaseLine images (intra-subject) (FU_to_BL)
logger.info("Starting FU_to_BL") 

input_dir = "./tessa-etal-2014/ANTs-derivatives/SS"
output_path = "./tessa-etal-2014/ANTs-derivatives/FU_to_BL"
shutil.copytree("./tessa-etal-2014/ANTs-derivatives/SS", output_path, ignore=ig_f)

for root, dirs, files in os.walk(input_dir):
    for file in files:
        if 'ses-BL' not in root and file.endswith("BrainExtractionBrain.nii.gz"):
            counter += 1
            moving_t1 = root + "/" + file
            if 'ses-V06' in moving_t1:
                fixed_t1 = moving_t1.replace("ses-V06", "ses-BL")
            if 'ses-V10' in moving_t1:
                fixed_t1 = moving_t1.replace("ses-V10", "ses-BL")
            output_reg_path = fixed_t1.replace("SS", "FU_to_BL")
            output_reg_path1 = output_reg_path.replace("FU_to_BL_corrected_T1wBrainExtractionBrain.nii.gz", "FU2BL_")
            output_reg_path2 = output_reg_path.replace("FU_to_BL_corrected_T1wBrainExtractionBrain.nii.gz", "FU2BL_Warped.nii.gz")
            command = "singularity run ./singuant_img.simg antsRegistration --dimensionality 3 --float 0 --output ["+output_reg_path1+","+output_reg_path2+"] --interpolation Linear --winsorize-image-intensities [0.005,0.995] --use-histogram-matching 0 --initial-moving-transform [$template,t1_biascorr.nii.gz,1] --transform Affine[0.1] --metric MI[$template,t1_biascorr.nii.gz,1,32,Regular,0.25] --convergence [1000x500x250x100,1e-6,10] --shrink-factors 8x4x2x1 --smoothing-sigmas 3x2x1x0vox --transform SyN[0.1,3,0] --metric CC[$template,t1_biascorr.nii.gz,1,4] --convergence [200x140x100x40,1e-6,10] --shrink-factors 8x4x2x1 --smoothing-sigmas 3x2x1x0vox -v"
            command = command.replace("$template", fixed_t1)
            command = command.replace("t1_biascorr.nii.gz", moving_t1)

            launch_script = "launch" + str(counter) + ".sh"
            os.system("echo '#!/bin/bash' >> " + launch_script)
            os.system("echo '#SBATCH --time=120:00:00' >> " + launch_script)
            os.system("echo '#SBATCH --account=def-jbpoline' >> " + launch_script)
            os.system("echo '#SBATCH --mem-per-cpu=32768M' >> " + launch_script)
            os.system("echo 'module load apptainer/1.1'  >> " + launch_script)
            os.system("""echo 'export APPTAINER_BIND="/lustre04/scratch/jacobsr"' >> """ + launch_script)
            os.system("echo '" + command + "' >> " + launch_script)
            os.system("sbatch " + launch_script)
            logger.info(moving_t1)          
