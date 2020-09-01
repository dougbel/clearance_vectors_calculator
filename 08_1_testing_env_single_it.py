import logging
import math
import time
import os
import json
import trimesh
import numpy as np
import pandas as pd
import open3d as o3d

from tqdm import trange
from transforms3d.affines import compose
from transforms3d.derivations.eulerangles import z_rotation

import it.util as util
from it_clearance.testing.envirotester import EnviroTesterClearance

if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    logging.info('Reading configuration interactions to test')

    # ON HANGING RACK
    # file_env = './data/hanging-rack.ply'
    # testing_radius = 0.005
    # directory_of_trainings = "./output/descriptors_repository/IBSMesh_400_4_OnGivenPointCloudWeightedSampler_5_1500"
    # json_conf_execution_file = "./data/single_testing_hanging_umbrella.json"
    # output_dir = './output/testing_env_single/hanging_rack'

    # ON SCENE_0000_00
    env_file = './data/scenes/scene0000_00_vh_clean.ply'
    testing_radius = 0.05

    ####################################
    # 8 orientations
    # directory_of_trainings = "./output/descriptors_repository/IBSMesh_400_4_OnGivenPointCloudWeightedSampler_5_500_PropagateNormalObjectPoissonDiscSamplerClearance_256"
    # json_conf_execution_file = "./data/test_configs/single_testing_standing_up.json"
    # json_conf_execution_file = "./data/test_configs/single_testing_sitting.json"
    # json_conf_execution_file = "./data/test_configs/single_testing_laying.json"
    # json_conf_execution_file = "./data/test_configs/single_testing_child_laying.json"
    # json_conf_execution_file = "./data/test_configs/single_testing_placing_small_box.json"
    # json_conf_execution_file = "./data/test_configs/single_testing_placing_large_box.json"
    directory_of_trainings = "./output/descriptors_repository/IBSMesh_2000_2_OnGivenPointCloudWeightedSampler_5_500_PropagateNormalObjectPoissonDiscSamplerClearance_256"
    json_conf_execution_file = "./data/test_configs/single_testing_reaching_out_low.json"
    # json_conf_execution_file = "./data/test_configs/single_testing_reaching_out_mid_low.json"
    # json_conf_execution_file = "./data/test_configs/single_testing_reaching_out_mid_up.json"
    # directory_of_trainings = "./output/descriptors_repository/IBSMesh_2000_2_OnGivenPointCloudWeightedSampler_5_1500_PropagateNormalObjectPoissonDiscSamplerClearance_256"
    # json_conf_execution_file = "./data/test_configs/single_testing_reaching_out_up.json"
    output_dir = './output/testing_env_single/scene0000_00'

    tri_mesh_env = trimesh.load_mesh(env_file)

    start = time.time()  # timing execution
    np_test_points, np_env_normals = util.sample_points_poisson_disk_radius(tri_mesh_env, radius=testing_radius)
    end = time.time()  # timing execution
    print("Sampling 1 Execution time: ", end - start)

    start = time.time()  # timing execution
    sampling_size = np_test_points.shape[0]
    np_test_points = util.sample_points_poisson_disk(tri_mesh_env, sampling_size)
    np_env_normals = util.get_normal_nearest_point_in_mesh(tri_mesh_env, np_test_points)
    end = time.time()  # timing execution
    print("Sampling 2 Execution time: ", end - start)

    tester = EnviroTesterClearance(directory_of_trainings, json_conf_execution_file)

    affordance_name = tester.affordances[0][0]
    affordance_object = tester.affordances[0][1]
    tri_mesh_object_file = tester.objs_filenames[0]

    tri_mesh_obj = trimesh.load_mesh(tri_mesh_object_file)

    start = time.time()  # timing execution
    # Testing iT
    full_data_frame = tester.start_full_test(tri_mesh_env, np_test_points, np_env_normals)
    end = time.time()  # timing execution
    time_exe = end - start
    print("Testing execution time: ", time_exe)

    # ##################################################################################################################
    # SAVING output

    output_dir = os.path.join(output_dir, affordance_name + '_' + affordance_object)

    logging.info('Saving results on ' + output_dir)

    data = {'execution_time_it_test': time_exe,
            'num_points_tested': np_test_points.shape[0],
            'testing_radius': testing_radius,
            'tester_info': tester.configuration_data,
            'directory_of_trainings': directory_of_trainings,
            'file_env': env_file
            }

    with open(os.path.join(output_dir, 'test_data.json'), 'w') as outfile:
        json.dump(data, outfile, indent=4)

    tri_mesh_env.export(output_dir + "/test_environment.ply", "ply")
    tri_mesh_obj.export(output_dir + "/test_object.ply", "ply")

    # test points
    o3d_test_points = o3d.geometry.PointCloud()
    o3d_test_points.points = o3d.utility.Vector3dVector(np_test_points)
    o3d.io.write_point_cloud(output_dir + "/test_tested_points.pcd", o3d_test_points)

    # it test
    filename = os.path.join(output_dir, "test_scores.csv")  # "%s/test_scores.csv" % output_dir
    full_data_frame.to_csv(filename)
