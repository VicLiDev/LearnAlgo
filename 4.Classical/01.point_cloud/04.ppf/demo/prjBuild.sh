#!/usr/bin/env bash
#########################################################################
# File Name: prjBuild.sh
# Author: LiHongjin
# mail: 872648180@qq.com
# Created Time: Sun 30 Nov 2025 08:59:39 AM CST
#########################################################################

set -e

build_type="$1"

[ -z "${build_type}" ] && build_type="Makefile"

if [ "${build_type}" == "CMake" ]
then
    # CMake
    [ ! -e "build" ] && mkdir build
    cd build
    cmake .. && make -j$(nproc)

    ./ppf_demo_gpt ../../data_gpt/model_cube.ply ../../data_gpt/scene_cube.ply
    # ./ppf_demo_gpt ../../data_gpt/complex_model.ply ../../data_gpt/complex_scene.ply
    ./ppf_load_match ../../data_opencv/parasaurolophus_6700.ply ../../data_opencv/rs22_proc2.ply
    ./ppf_normal_computation ../../data_opencv/parasaurolophus_6700.ply ./output
elif [ "${build_type}" == "Makefile" ]
then
    make

    ./ppf_demo_gpt ../data_gpt/model_cube.ply ../data_gpt/scene_cube.ply
    # ./ppf_demo_gpt ../data_gpt/complex_model.ply ../data_gpt/complex_scene.ply
    ./ppf_load_match ../data_opencv/parasaurolophus_6700.ply ../data_opencv/rs22_proc2.ply
    ./ppf_normal_computation ../data_opencv/parasaurolophus_6700.ply ./output
fi

set +e
