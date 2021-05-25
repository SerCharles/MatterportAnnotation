'''
Used in clearing the data of the pretrain dataset
'''
import argparse
import numpy as np
import os
import glob




def save_remove(name):
    '''
    description: remove a file safely
    parameter: file name
    return: empty
    '''
    try: 
        os.remove(name)
        print('removed', name)
    except: 
        pass

def clear_one(base_dir, base_dir_geolayout, type):
    ''' 
    description: clearing the data in geolayout dataset
    parameter: the base dir of pretrained data, the base_dir of geolayout data, the type of data
    return: empty
    '''
    for name in glob.glob(os.path.join(base_dir_geolayout, type, 'image', '*.jpg')):
        filename = name.split(os.sep)[-1]
        base_name = filename[:-9]
        group_name = filename[-7]
        ins_name = filename[-5]
        image_name = base_name + '_i' + group_name + '_' + ins_name + '.jpg'
        depth_name = base_name + '_d' + group_name + '_' + ins_name + '.png'
        nx_name = base_name + '_d' + group_name + '_' + ins_name + '_nx.png'
        ny_name = base_name + '_d' + group_name + '_' + ins_name + '_ny.png'
        nz_name = base_name + '_d' + group_name + '_' + ins_name + '_nz.png'
        boundary_name = base_name + '_d' + group_name + '_' + ins_name + '_boundary.png'
        radius_name = base_name + '_d' + group_name + '_' + ins_name + '_radius.png'
        intrinsic_name = base_name + '_pose_' + group_name + '_' + ins_name + '.txt'
        seg_name = base_name + '_s' + group_name + '_' + ins_name + '.png'

        save_remove(os.path.join(base_dir, 'image', image_name))
        save_remove(os.path.join(base_dir, 'depth', depth_name))
        save_remove(os.path.join(base_dir, 'norm', nx_name))
        save_remove(os.path.join(base_dir, 'norm', ny_name))
        save_remove(os.path.join(base_dir, 'norm', nz_name))
        save_remove(os.path.join(base_dir, 'norm', boundary_name))
        save_remove(os.path.join(base_dir, 'norm', radius_name))
        save_remove(os.path.join(base_dir, 'intrinsic', intrinsic_name))
        save_remove(os.path.join(base_dir, 'seg', seg_name))

def clear_noisy_data(base_dir):
    '''
    description: remove useless noisy data from the dataset
    parameter: the base dir of dataset
    return: empty
    '''
    remove_list = ['B6ByNegPMKs', 'vyrNrziPKCB']
    for scene_id in remove_list:
        conf_name = os.path.join(base_dir, 'data_list', scene_id + '.conf')
        f = open(conf_name, 'r')
        lines = f.read().split('\n')
        f.close()
        for line in lines:
            words = line.split()
            if len(words) >  0 and words[0] == 'scan':
                base_name = words[1][:-9]
                group_name = words[1][-7]
                ins_name = words[1][-5]
                image_name = base_name + '_i' + group_name + '_' + ins_name + '.jpg'
                depth_name = base_name + '_d' + group_name + '_' + ins_name + '.png'
                nx_name = base_name + '_d' + group_name + '_' + ins_name + '_nx.png'
                ny_name = base_name + '_d' + group_name + '_' + ins_name + '_ny.png'
                nz_name = base_name + '_d' + group_name + '_' + ins_name + '_nz.png'
                boundary_name = base_name + '_d' + group_name + '_' + ins_name + '_boundary.png'
                radius_name = base_name + '_d' + group_name + '_' + ins_name + '_radius.png'
                intrinsic_name = base_name + '_pose_' + group_name + '_' + ins_name + '.txt'
                seg_name = base_name + '_s' + group_name + '_' + ins_name + '.png'
                
                save_remove(os.path.join(base_dir, 'image', image_name))
                save_remove(os.path.join(base_dir, 'depth', depth_name))
                save_remove(os.path.join(base_dir, 'norm', nx_name))
                save_remove(os.path.join(base_dir, 'norm', ny_name))
                save_remove(os.path.join(base_dir, 'norm', nz_name))
                save_remove(os.path.join(base_dir, 'norm', boundary_name))
                save_remove(os.path.join(base_dir, 'norm', radius_name))
                save_remove(os.path.join(base_dir, 'intrinsic', intrinsic_name))
                save_remove(os.path.join(base_dir, 'seg', seg_name))



def clear_norm(base_dir):
    ''' 
    description: clearing the useless norm data
    parameter: the base dir of pretrained data
    return: empty
    '''
    for name in glob.glob(os.path.join(base_dir, 'depth', '*.png')):
        filename = name.split(os.sep)[-1]
        base_name = filename[:-9]
        group_name = filename[-7]
        ins_name = filename[-5]
        boundary_name = base_name + '_d' + group_name + '_' + ins_name + '_boundary.png'
        radius_name = base_name + '_d' + group_name + '_' + ins_name + '_radius.png'
        save_remove(os.path.join(base_dir, 'norm', boundary_name))
        save_remove(os.path.join(base_dir, 'norm', radius_name))

def data_split(base_dir):
    ''' 
    description: split the train and valid data
    parameter: the base dir of pretrained data
    return: empty
    '''
    image_filenames = glob.glob(os.path.join(base_dir, 'image', '*.jpg'))
    length = len(image_filenames)
    threshold = int(length * 0.9)

    f_train = open(os.path.join(base_dir, 'training.txt'), 'w')
    f_valid = open(os.path.join(base_dir, 'validation.txt'), 'w')


    for i in range(length):
        the_name = image_filenames[i].split(os.sep)[-1]
        if i < threshold:
            f_train.write(the_name + '\n')
        else: 
            f_valid.write(the_name + '\n')
    f_train.close()
    f_valid.close()




def main():
    '''
    description: the main function of data clearing
    parameter: empty
    return: empty
    '''
    parser = argparse.ArgumentParser(description = '')
    parser.add_argument('--base_dir', default = '/home/shenguanlin/geolayout_pretrain', type = str)
    parser.add_argument('--base_dir_geolayout', default = '/home/shenguanlin/geolayout', type = str)
    args = parser.parse_args()

    
    clear_noisy_data(args.base_dir)
    clear_one(args.base_dir, args.base_dir_geolayout, 'training')
    clear_one(args.base_dir, args.base_dir_geolayout, 'validation')
    clear_one(args.base_dir, args.base_dir_geolayout, 'testing')
    clear_norm(args.base_dir)
    data_split(args.base_dir)
    

if __name__ == "__main__":
    main()