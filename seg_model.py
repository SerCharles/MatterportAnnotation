'''
Segmentation of the ply file into 2 types: background or not
'''

import argparse
import numpy as np
import os
import glob
import json
from plyfile import *

def write_ply(filename, points, faces):
    '''
    description: write one ply file
    parameter: the filename, vertexs, faces
    return: empty
    '''
    with open(filename, 'w') as f:
        header = "ply\n" + \
                "format ascii 1.0\n" + \
                "element vertex " + \
                str(len(points)) + '\n' + \
                "property float x\n" + \
                "property float y\n" + \
                "property float z\n" + \
                "property uchar red\n" + \
                "property uchar green\n" + \
                "property uchar blue\n" + \
                "element face " + \
                str(len(faces)) + "\n" + \
                "property list uchar int vertex_index\n" + \
                "end_header\n"

        f.write(header)
        for point in points:
            for value in point[:3]:
                f.write(str(value) + ' ')
                continue
            for value in point[3:]:
                f.write(str(int(value)) + ' ')
                continue
            f.write('\n')
            continue
        for face in faces:
            f.write('3 ' + str(face[0]) + ' ' + str(face[1]) + ' ' + str(face[2]) + '\n')
            continue     
        f.close()
        pass
    return

def seg_one_ply(base_dir, scene_id):
    '''
    description: segmentation of one ply file
    parameter: base dir, scene id
    return: empty
    '''
    ply_name = os.path.join(base_dir, scene_id + '.ply')
    instance_descriptor_name = os.path.join(base_dir, scene_id + '.semseg.json') 
    face_info_name = os.path.join(base_dir, scene_id + '.fsegs.json')

    plydata = PlyData.read(ply_name)
    vertexs = plydata['vertex']
    faces = plydata['face']
    num_vertexs = vertexs.count
    num_faces = faces.count
    
    with open(instance_descriptor_name, 'r', encoding = 'utf8')as fp:
        instance_info = json.load(fp)
        instances = instance_info['segGroups']

    with open(face_info_name, 'r', encoding = 'utf8')as fp:
        face_info_total = json.load(fp)
        face_info = face_info_total['segIndices']
    
    background_types = [1, 2, 3, 4, 5, 6, 8, 18]

    whether_background = [False] * num_vertexs
    segment_type = {}


    for i in range(len(instances)):
        instance = instances[i]
        type = instance['label_index']
        if type in background_types:
            for id in instance['segments']:
                segment_type[id] = True 
        else:
            for id in instance['segments']:
                segment_type[id] = False

    for i in range(num_faces):
        seg_id = face_info[i]
        a = faces[i][0][0]
        b = faces[i][0][1]
        c = faces[i][0][2]

        if segment_type[seg_id] == True:
            whether_background[a] = True 
            whether_background[b] = True 
            whether_background[c] = True 
    
    my_vertex = np.zeros((num_vertexs, 6), dtype = float)
    my_face = np.zeros((num_faces, 3), dtype = int)

    for i in range(num_vertexs):
        my_vertex[i][0] = vertexs[i][0]
        my_vertex[i][1] = vertexs[i][1]
        my_vertex[i][2] = vertexs[i][2]
        
        if whether_background[i] == True:
            my_vertex[i][3] = 0
            my_vertex[i][4] = 0
            my_vertex[i][5] = 0
        else:
            my_vertex[i][3] = 255
            my_vertex[i][4] = 255
            my_vertex[i][5] = 255
        

    for i in range(num_faces):
        my_face[i][0] = faces[i][0][0]
        my_face[i][1] = faces[i][0][1]
        my_face[i][2] = faces[i][0][2]
    save_place = os.path.join(base_dir, scene_id + '_seg.ply')
    write_ply(save_place, my_vertex, my_face)
    print('written', save_place)







def main():
    '''
    description: the main function of data preprocessing
    parameter: empty
    return: empty
    '''
    parser = argparse.ArgumentParser(description = '')
    parser.add_argument('--base_dir', default = '/home/shenguanlin/geolayout_pretrain', type = str)
    args = parser.parse_args()

    base_dir = os.path.join(args.base_dir, 'seg')
    filenames = glob.glob(os.path.join(base_dir, '*.ply'))
    for full_name in filenames:
        scene_id = full_name.split(os.sep)[-1][:-4]
        seg_one_ply(base_dir, scene_id)



if __name__ == "__main__":
    main()