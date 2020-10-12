import json
import os

import pandas as pd
from vedo import Plotter, load, interactive, Points

from it_clearance.testing.tester import TesterClearance
from si.fulldataclearancescores import FullDataClearanceScores
from si.fulldatascores import FullDataScores

if __name__ == '__main__':
    directory_of_trainings = "./output/descriptors_repository/IBSMesh_400_4_OnGivenPointCloudWeightedSampler_5_500_PropagateNormalObjectPoissonDiscSamplerClearance_256"
    # json_conf_execution_file = "./data/test_configs/single_testing_standing_up.json"
    json_conf_execution_file = "./data/test_configs/single_testing_sitting.json"
    # json_conf_execution_file = "./data/test_configs/single_testing_laying.json"
    # json_conf_execution_file = "./data/test_configs/single_testing_child_laying.json"
    # json_conf_execution_file = "./data/test_configs/single_testing_placing_small_box.json"
    # json_conf_execution_file = "./data/test_configs/single_testing_placing_large_box.json"
    # json_conf_execution_file = "./data/test_configs/single_testing_ride_motorbike.json"
    # directory_of_trainings = "./output/descriptors_repository/IBSMesh_2000_2_OnGivenPointCloudWeightedSampler_5_500_PropagateNormalObjectPoissonDiscSamplerClearance_256"
    # json_conf_execution_file = "./data/test_configs/single_testing_reaching_out_low.json"
    # jsqon_conf_execution_file = "./data/test_configs/single_testing_reaching_out_mid_low.json"
    # json_conf_execution_file = "./data/test_configs/single_testing_reaching_out_mid_up.json"
    # json_conf_execution_file = "./data/test_configs/single_testing_hanging_sloped_hat.json"
    # directory_of_trainings = "./output/descriptors_repository/IBSMesh_2000_2_OnGivenPointCloudWeightedSampler_5_1500_PropagateNormalObjectPoissonDiscSamplerClearance_256"
    # json_conf_execution_file = "./data/test_configs/single_testing_reaching_out_up.json"
    # directory_of_trainings = "./output/descriptors_repository/IBSMesh_400_4_OnGivenPointCloudWeightedSampler_5_1500_PropagateNormalObjectPoissonDiscSamplerClearance_256"
    # json_conf_execution_file = "./data/test_configs/single_testing_hanging_umbrella.json"

    directory_env_test_results = "./output/testing_env_single/scene0000_00/filled"
    directory_of_prop_configs = "./output/propagators_configs/scene0000_00/filled"



    # #################################################################################################################

    tester = TesterClearance(directory_of_trainings, json_conf_execution_file)
    affordance_name = tester.affordances[0][0]
    affordance_object = tester.affordances[0][1]
    subdir_name = affordance_name + "_" + affordance_object
    env_test_results = os.path.join(directory_env_test_results, subdir_name)
    file_mesh_env = os.path.join(env_test_results, "test_environment.ply")

    propagation_settings_file = os.path.join(directory_of_prop_configs, subdir_name, 'propagation_data.json')
    with open(propagation_settings_file) as json_file:
        propagation_settings = json.load(json_file)
    max_limit_score = propagation_settings['max_limit_score']
    max_limit_missing = propagation_settings['max_limit_missing']
    max_limit_cv_collided = propagation_settings['max_limit_cv_collided']

    df_scores_data = pd.read_csv(os.path.join(env_test_results, "test_scores.csv"))

    vp = Plotter(size=(1200, 800), pos=(100, 250), shape=(1,2))
    vedo_file_env = load(file_mesh_env).c("gray").lighting("plastic")

    scores_data = FullDataClearanceScores(df_scores_data, affordance_name)
    np_points, np_scores, np_missings, np_cv_collided = scores_data.filter_data_scores(
        max_limit_score,
        max_limit_missing,
        max_limit_cv_collided)
    pts = Points(np_points, r=5)
    pts.cellColors(np_scores, cmap='jet', vmin=0, vmax=max_limit_score)
    pts.addScalarBar(pos=(0.8, 0.25), nlabels=5, title="PV alignment distance", titleFontSize=10)
    # vp.add(pts, at=0)
    # vp.add(vedo_file_env, at=0)
    vp.show([pts, vedo_file_env], 'With Clearance Vectors', at=0)

    naive_score_data = FullDataScores(df_scores_data, affordance_name)
    np_points, np_scores, np_missings = naive_score_data.filter_data_scores(max_limit_score, max_limit_missing)
    pts = Points(np_points, r=5)
    pts.cellColors(np_scores, cmap='jet', vmin=0, vmax=max_limit_score)
    pts.addScalarBar(pos=(0.8, 0.25), nlabels=5, title="PV alignment distance", titleFontSize=10)
    # vp.add(pts, at=1)
    # vp.show(vedo_file_env, 'Without Clearance Vectors', at=1)
    vp.show([pts, vedo_file_env], 'Without Clearance Vectors', at=1)

    interactive()

    # view.add_point_cloud(np_points, np_scores)
