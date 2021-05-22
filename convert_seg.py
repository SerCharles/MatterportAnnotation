'''
Used in getting the converting the segmentation data and getting the segmentation accuracy, based on the human-made geolayout data
'''
import argparse
import numpy as np
import os
import glob
import scipy.io as sio
from torch.autograd import Variable
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import glob
import PIL



def load_image(file_name):
    '''
    description: used in loading RGB image
    parameter: filename
    return: image info of PIL
    '''
    fp = open(file_name, 'rb')
    pic = Image.open(fp)
    pic_array = np.array(pic)
    fp.close()
    return pic_array
      
def load_seg(file_name):
    '''
    description: used in loading segmentation images
    parameter: filename
    return: info of PIL
    '''
    fp = open(file_name, 'rb')
    pic = Image.open(fp)
    pic_array = np.array(pic)
    fp.close()
    pic = Image.fromarray(pic_array)
    pic = pic.convert("I")
    pic_array = np.array(pic)
    return pic_array

def save_seg(data, file_name):
    '''
    description: used in saving segmentation images
    parameter: data, filename
    return: empty
    '''
    if os.path.exists(file_name):
        return
    seg_image = Image.fromarray(np.uint8(data)).convert('I')
    seg_image.save(file_name)

def convert_segs(base_dir):
    '''
    description: converting segmentation files
    parameter: the base dir of pretrained data
    return: empty
    '''
    for dir_name in glob.glob(os.path.join(base_dir, 'segs', '*')):
        for file_name in glob.glob(os.path.join(dir_name, '*.png')):
            name = file_name.split(os.sep)[-1]
            base_name = name[:-9]
            group_name = name[-7]
            ins_name = name[-5]
            full_name = base_name + '_s' + group_name + '_' + ins_name + '.png'
            original_place = os.path.join(base_dir, 'segs', dir_name, full_name)
            save_place = os.path.join(base_dir, 'seg', full_name)
            original_array = load_image(original_place)
            original_array_sum = np.sum(original_array, axis = 2)
            seg = (original_array_sum == 0)
            save_seg(seg, save_place)
            print('written', save_place)



def get_seg_accuracy(base_dir, base_dir_geolayout):
    ''' 
    description: get the accuracy of segmentations
    parameter: the base dir of pretrained data, the base_dir of geolayout data
    return: empty
    '''
    total_same = 0
    total_num = 0
    for name in glob.glob(os.path.join(base_dir_geolayout, 'training', 'image', '*.jpg')):
        filename = name.split(os.sep)[-1]
        base_name = filename[:-9]
        group_name = filename[-7]
        ins_name = filename[-5]

        seg_name_mine = base_name + '_s' + group_name + '_' + ins_name + '.png'
        seg_name_geolayout = base_name + '_i' + group_name + '_' + ins_name + '.png'
        seg_place_mine = os.path.join(base_dir, 'seg', seg_name_mine)
        seg_place_geolayout = os.path.join(base_dir_geolayout, 'training', 'init_label', seg_name_geolayout)

        seg_mine = load_seg(seg_place_mine)
        seg_geolayout = load_seg(seg_place_geolayout)
        H, W = seg_mine.shape

        mask_geolayout = (seg_geolayout != 0)
        same_num = float(np.sum(seg_geolayout == mask_geolayout))
        acc = same_num / (H * W)
        total_same += acc 
        total_num += 1
        print('Accuracy: {:.4f}'.format(acc))

    for name in glob.glob(os.path.join(base_dir_geolayout, 'validation', 'image', '*.jpg')):
        filename = name.split(os.sep)[-1]
        base_name = filename[:-9]
        group_name = filename[-7]
        ins_name = filename[-5]

        seg_name_mine = base_name + '_s' + group_name + '_' + ins_name + '.png'
        seg_name_geolayout = base_name + '_i' + group_name + '_' + ins_name + '.png'
        seg_place_mine = os.path.join(base_dir, 'seg', seg_name_mine)
        seg_place_geolayout = os.path.join(base_dir_geolayout, 'validation', 'init_label', seg_name_geolayout)

        seg_mine = load_seg(seg_place_mine)
        seg_geolayout = load_seg(seg_place_geolayout)
        H, W = seg_mine.shape

        mask_geolayout = (seg_geolayout != 0)
        same_num = float(np.sum(seg_geolayout == mask_geolayout))
        acc = same_num / (H * W)
        total_same += acc 
        total_num += 1    
        print('Accuracy: {:.4f}'.format(acc))
    
    accuracy = total_same / total_num
    print('Total Accuracy: {:.4f}'.format(accuracy))


def main():
    '''
    description: the main function of data clearing
    parameter: empty
    return: empty
    '''
    parser = argparse.ArgumentParser(description = '')
    #parser.add_argument('--base_dir', default = '/home/shenguanlin/geolayout_pretrain', type = str)
    parser.add_argument('--base_dir', default = '/data/sgl/geolayout_pretrain', type = str)
    parser.add_argument('--base_dir_geolayout', default = '/home/shenguanlin/geolayout', type = str)
    args = parser.parse_args()

    convert_segs(args.base_dir)
    get_seg_accuracy(args.base_dir, args.base_dir_geolayout)
    

if __name__ == "__main__":
    main()