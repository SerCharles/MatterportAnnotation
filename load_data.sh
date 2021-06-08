
base_code=/home/shenguanlin/MatterportAnnotation
base_source=/data/sgl/matterport/v1/scans
base_target=/home/shenguanlin/geolayout_pretrain
base_target_geolayout=/home/shenguanlin/geolayout

mkdir $base_target
cd $base_target
mkdir norm 
mkdir depth 
mkdir image 
mkdir intrinsic
mkdir camera_pre
mkdir pose
mkdir seg
mkdir mesh
mkdir data_list


cd $base_source
files=$(ls $folder)
for file in $files
do
    sudo unzip $base_source/$file/undistorted_color_images.zip -d $base_target
    sudo unzip $base_source/$file/matterport_camera_intrinsics.zip -d $base_target
    sudo unzip $base_source/$file/matterport_camera_poses.zip -d $base_target
    sudo unzip $base_source/$file/undistorted_depth_images.zip -d $base_target
    sudo unzip $base_source/$file/undistorted_normal_images.zip -d $base_target
    sudo unzip $base_source/$file/house_segmentations.zip -d $base_target
    sudo unzip $base_source/$file/undistorted_camera_parameters.zip -d $base_target

    sudo chmod -R 777 $base_target
    cd $base_target/$file/undistorted_color_images
    images=$(ls *)
    cd $base_target/$file/matterport_camera_intrinsics
    intrinsics=$(ls *)
    cd $base_target/$file/matterport_camera_poses
    poses=$(ls *)
    cd $base_target/$file/undistorted_depth_images
    depths=$(ls *)
    cd $base_target/$file/undistorted_normal_images
    norms=$(ls *)
    cd $base_target/$file/house_segmentations
    meshs=$(ls *)
    cd $base_target/$file/undistorted_camera_parameters
    data_lists=$(ls *)

    for image in $images
    do 
        mv $base_target/$file/undistorted_color_images/$image $base_target/image/$image
    done

    for intrinsic in $intrinsics
    do 
        mv $base_target/$file/matterport_camera_intrinsics/$intrinsic $base_target/camera_pre/$intrinsic

    done

    for pose in $poses
    do 
        mv $base_target/$file/matterport_camera_poses/$pose $base_target/pose/$pose
    done

    for depth in $depths
    do 
        mv $base_target/$file/undistorted_depth_images/$depth $base_target/depth/$depth
    done

    for norm in $norms
    do 
        mv $base_target/$file/undistorted_normal_images/$norm $base_target/norm/$norm
    done

    for mesh in $meshs
    do 
        mv $base_target/$file/house_segmentations/$mesh $base_target/mesh/$mesh
    done

    for data_list in $data_lists
    do 
        mv $base_target/$file/undistorted_camera_parameters/$data_list $base_target/data_list/$data_list
    done

    rm -rf $base_target/$file
done
cd $base_code
python preprocess_data.py --base_dir=$base_target --base_dir_geolayout=$base_target_geolayout
cd $base_target
rm image/Thumbs.db
rm -rf camera_pre