'''
Used in getting the intrinsics of the pretrain dataset
'''
import argparse
import numpy as np
import os
import glob



def get_intrinsics(base_dir):
    '''
    description: generate and save all the intrinsics and camera places
    parameter: the base dir of dataset
    return: empty
    '''
    all_filenames = glob.glob(os.path.join(base_dir, 'image', '*.jpg'))
    for filename in all_filenames:
        name = filename.split(os.sep)[-1]
        base_name = name[:-9]
        group_name = name[-7]
        ins_name = name[-5]
        pre_name = base_name + '_intrinsics_' + group_name  + '.txt'
        the_name = base_name + '_pose_' + group_name + '_' + ins_name + '.txt'

        f = open(os.path.join(base_dir, 'camera_pre', pre_name), 'r')
        words = f.read().split()
        fx = float(words[2])
        fy = float(words[3])
        cx = float(words[4])
        cy = float(words[5])
        f.close()

        f = open(os.path.join(base_dir, 'intrinsic', the_name), 'w')
        f.write(str(fx) + ' ' + str(fy) + ' ' + str(cx) + ' ' + str(cy))
        f.close()

def main():
    '''
    description: the main function of data preprocessing
    parameter: empty
    return: empty
    '''
    parser = argparse.ArgumentParser(description = '')
    parser.add_argument('--base_dir', default = '/home/shenguanlin/geolayout_pretrain', type = str)
    args = parser.parse_args()

    get_intrinsics(args.base_dir)


if __name__ == "__main__":
    main()