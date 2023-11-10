import os
import glob

from constants import *

def get_output_sub_dir(fold_num):
    return os.path.join(DATA_FOLD_DIR, "fold_" + str(fold_num + 1))

def get_sample_dir_name_from_path(sample_path):
    return os.path.basename(os.path.dirname(sample_path))

def get_sample_paths_from_fold_num(fold_num):
    with open(os.path.join(get_output_sub_dir(fold_num), FOLD_SAMPLES_FILE_NAME), "r") as f:
        samples = [line.rstrip() for line in f]
    return samples

def get_file_names_in_dir(dir):
    names = sorted(glob.glob('{}/*/'.format(dir)))
    return names

def write_list_to_file(file_path, l):
    with open(file_path, "w") as f:
        for sample in l:
            print(sample, file=f)

def get_nifti_file_name(sample_name, tag):
    return sample_name + "_" + tag + ".nii.gz"