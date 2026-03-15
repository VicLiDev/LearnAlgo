#!/usr/bin/env bash
#########################################################################
# File Name: build_opencv_contrib.sh
# Author: LiHongjin
# mail: 872648180@qq.com
# Created Time: Sun 14 Dec 2025 12:49:21 PM CST
#########################################################################

# run this tool in dir of opencv/opencv_contrib up
# usage: <exe> pfx/sys/all

cur_root_dir=`pwd`

build_pfx_dir="${cur_root_dir}/build_pfx"
build_sys_dir="${cur_root_dir}/build_sys"

[ ! -e ${build_pfx_dir} ] && mkdir -p ${build_pfx_dir}
[ ! -e ${build_sys_dir} ] && mkdir -p ${build_sys_dir}

opencv_dir="${cur_root_dir}/opencv"
opencv_ctb_dir="${cur_root_dir}/opencv_contrib/modules"

cmd_install_loc="sys"

[ -n "$1" ] && cmd_install_loc="$1"

# # 一般不写开启ppf也会自动开启，但明确写上更安全。
# cmake ${opencv_dir}/ \
#     -DCMAKE_BUILD_TYPE=Release \
#     -DCMAKE_INSTALL_PREFIX=/${cur_root_dir}/install \
#     -DOPENCV_EXTRA_MODULES_PATH=${opencv_ctb_dir} \
#     -DBUILD_opencv_ppf=ON \
#     -DBUILD_EXAMPLES=ON

# ==============================================================================
# instasll to prefix
# ==============================================================================

if [[ "${cmd_install_loc}" == "pfx" || "${cmd_install_loc}" == "all" ]]
then
    echo "======> install to ${cur_root_dir}/install"
    cd ${build_pfx_dir}
    cmake ${opencv_dir}/ \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=${cur_root_dir}/install \
        -DOPENCV_EXTRA_MODULES_PATH=${opencv_ctb_dir} \
        -DBUILD_EXAMPLES=ON
    [ "$?" == "0" ] && make -j$(nproc) && make install
fi

# ==============================================================================
# instasll to sys
# ==============================================================================

if [[ "${cmd_install_loc}" == "sys" || "${cmd_install_loc}" == "all" ]]
then
    echo "======> install to sys"
    cd ${build_sys_dir}
    cmake ${opencv_dir}/ \
        -DOPENCV_EXTRA_MODULES_PATH=${opencv_ctb_dir} \
        -DBUILD_EXAMPLES=ON
    [ "$?" == "0" ] && make -j$(nproc) && sudo make install
fi
