import sys
import numpy as np
import sys
import skimage.io as sio
import os
import argparse
import glob
import lib.render as render
import data_loader

def read_intrinsic(full_name):
    '''
    description: read the intrinsic
    parameter: full_name
    return: fx, fy, cx, cy
    '''
    f = open(full_name, 'r')
    words = f.read().split()
    fx = float(words[0])
    fy = float(words[1])
    cx = float(words[2])
    cy = float(words[3])
    f.close()
    return fx, fy, cx, cy

def read_pose(full_name):
    '''
    description: read the extrinsic
    parameter: full_name
    return: numpy array of extrinsic
    '''
    pose = np.zeros((4, 4), dtype = np.float32)
    f = open(full_name, 'r')
    lines = f.read().split('\n')
    
    for i in range(4):
        words = lines[i].split()
        for j in range(4):
            word = float(words[j])
            pose[i][j] = word

    pose = pose.astype(np.float32)
    f.close()
    return pose

def render_one_scene(base_dir, scene_name, picture_name_list):
    '''
    description: render one scene
    parameter: the base dir of data, the scene name, the list of picture name lists
    return: empty
    '''
    input_name = os.path.join(base_dir, 'mesh', scene_name + '_seg.ply')
    V, VC, F = data_loader.LoadPLY(input_name)
    
    for i in range(len(picture_name_list)):
        picture_name = picture_name_list[i]
        base_name = picture_name[:-9]
        group_name = picture_name[-7]
        ins_name = picture_name[-5]
        full_name = base_name + '_pose_' + group_name + '_' + ins_name + '.txt'

        full_name_intrinsic = os.path.join(base_dir, 'intrinsic', full_name)
        full_name_pose = os.path.join(base_dir, 'pose', full_name)
        fx, fy, cx, cy = read_intrinsic(full_name_intrinsic)
        pose = read_pose(full_name_pose)

        info = {'Height':1024, 'Width':1280, 'fx':fx, 'fy':fy, 'cx':cx, 'cy':cy}
        render.setup(info)
        context = render.SetMesh(V, F)

        cam2world = pose 
        world2cam = np.linalg.inv(cam2world).astype('float32')
        render.render(context, world2cam)
        vindices, vweights, findices = render.getVMap(context, info)

        x_shape = findices.shape[0]
        y_shape = findices.shape[1]
        final_color = np.zeros((x_shape, y_shape, 3), dtype='float32')

        H = vindices.shape[0]
        W = vindices.shape[1]
        for k in range(vindices.shape[2]):
            indice = vindices[:, :, k]
            weight = vweights[:, :, k]
            weight = np.reshape(weight, (H, W, 1))
            weight = np.repeat(weight, 3, axis = 2)
            color = VC[indice]
            final_color = final_color + color * weight
        render.Clear()

        result_name = base_name + '_s' + group_name + '_' + ins_name + '.png'
        full_result_name = os.path.join(base_dir, 'segs', result_name)
        sio.imsave(full_result_name, final_color)
        print('written', full_result_name)

def get_scene_names(base_dir):
    '''
    description: get the names of the scenes and the relative picture names
    parameter: the base dir of data
    return: scene list and name lists
    '''
    scene_name_list = []
    picture_name_list = []
    scene_filenames = glob.glob(os.path.join(base_dir, 'data_list', '*.conf'))
    for name in scene_filenames:
        picture_list = []
        scene_name = name.split(os.sep)[-1][:-5]

        f = open(name, 'r')
        lines = f.read().split('\n')
        for line in lines:
            words = line.split()
            if len(words) > 0 and words[0] == 'scan':
                picture_list.append(words[1])
        f.close()
        scene_name_list.append(scene_name)
        picture_name_list.append(picture_list)
    return scene_name_list, picture_name_list


def main():
    '''
    description: the main function of data rendering
    parameter: empty
    return: empty
    '''
    parser = argparse.ArgumentParser(description = '')
    parser.add_argument('--base_dir', default = '/data/sgl/geolayout_pretrain', type = str)
    args = parser.parse_args()
    scene_name_list, picture_name_list = get_scene_names(args.base_dir)
    for i in range(len(scene_name_list)):
        scene_name = scene_name_list[i]
        picture_names = picture_name_list[i]
        render_one_scene(args.base_dir, scene_name, picture_names)
    

if __name__ == "__main__":
    main()