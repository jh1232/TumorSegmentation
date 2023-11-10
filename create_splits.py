import os
import random
import shutil

from utils import get_output_sub_dir, get_file_names_in_dir, get_sample_paths_from_fold_num, write_list_to_file, get_sample_dir_name_from_path, get_nifti_file_name
from constants import *

def get_combined_file_names(root_dir, sub_dirs):
    combined_files = []

    for d in sub_dirs:
        full_dir_path = os.path.join(root_dir, d)
        combined_files.extend(get_file_names_in_dir(full_dir_path))
    
    return combined_files

def generate_splits():
    combined_file_names = get_combined_file_names(TRAIN_DIR, TRAIN_SUB_DIRS)
    assert(len(combined_file_names) == 285) # 210 HGG + 75 LGG

    random.Random(SEED).shuffle(combined_file_names)

    split_size = len(combined_file_names)//K_FOLDS

    for i in range(K_FOLDS):
        file_name_subset = combined_file_names[split_size*i:split_size*(i + 1)]
        assert(len(file_name_subset) == len(combined_file_names)//K_FOLDS)

        output_sub_dir = get_output_sub_dir(i)

        if os.path.isdir(output_sub_dir):
            shutil.rmtree(output_sub_dir)

        os.makedirs(output_sub_dir, exist_ok=True)

        write_list_to_file(os.path.join(output_sub_dir, FOLD_SAMPLES_FILE_NAME), file_name_subset)



def copy_splits():
    for i in range(K_FOLDS):
        curr_samples = get_sample_paths_from_fold_num(i)
        output_sub_dir = get_output_sub_dir(i)

        for sample in curr_samples:
            sample_dir_name = os.path.join(output_sub_dir, get_sample_dir_name_from_path(sample))
            os.makedirs(sample_dir_name)
            shutil.copytree(sample, sample_dir_name, dirs_exist_ok=True)

        

def validate_splits():
    total_samples = 0
    for i in range(K_FOLDS):
        curr_split_sample_names = get_sample_paths_from_fold_num(i)
        total_samples += len(curr_split_sample_names)

        curr_samples = get_file_names_in_dir(get_output_sub_dir(i))

        assert(len(curr_samples) == len(curr_split_sample_names))

        for s in curr_split_sample_names:
            assert(any(get_sample_dir_name_from_path(s) in get_sample_dir_name_from_path(sample_name) for sample_name in curr_samples))

        for s in curr_samples:
            nii_files = os.listdir(s)
            sample_name = get_sample_dir_name_from_path(s)
            assert(len(nii_files) == 5)
            assert(get_nifti_file_name(sample_name, GROUND_TRUTH_FILE_TAG) in nii_files)
            for seq in ALL_SEQUENCES:
                assert(get_nifti_file_name(sample_name, seq) in nii_files)

        # Check no duplicates across splits
        for j in range(i):
            prev_split_sample_names = get_sample_paths_from_fold_num(j)
            assert(not any(ii in prev_split_sample_names for ii in curr_split_sample_names))
            assert(not any(jj in curr_split_sample_names for jj in prev_split_sample_names))

    assert(total_samples == 285)

if __name__ == "__main__":
    generate_splits()
    copy_splits()
    validate_splits()