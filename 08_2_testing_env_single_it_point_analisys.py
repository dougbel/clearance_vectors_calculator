
from viewer.point_score.ControlPointScore import ControlPointScore

if __name__ == '__main__':
    directory_of_trainings = "./output/descriptors_repository/IBSMesh_400_4_OnGivenPointCloudWeightedSampler_5_500_PropagateNormalObjectPoissonDiscSamplerClearance_256"
    # json_conf_execution_file = "./data/test_configs/single_testing_standing_up.json"
    json_conf_execution_file = "./data/test_configs/single_testing_sitting.json"
    # json_conf_execution_file = "./data/test_configs/single_testing_laying.json"
    # json_conf_execution_file = "./data/test_configs/single_testing_child_laying.json"
    # json_conf_execution_file = "./data/test_configs/single_testing_placing_small_box.json"
    # json_conf_execution_file = "./data/test_configs/single_testing_placing_large_box.json"
    # directory_of_trainings = "./output/descriptors_repository/IBSMesh_2000_2_OnGivenPointCloudWeightedSampler_5_500_PropagateNormalObjectPoissonDiscSamplerClearance_256"
    # json_conf_execution_file = "./data/test_configs/single_testing_reaching_out_low.json"
    # jsqon_conf_execution_file = "./data/test_configs/single_testing_reaching_out_mid_low.json"
    # json_conf_execution_file = "./data/test_configs/single_testing_reaching_out_mid_up.json"
    # directory_of_trainings = "./output/descriptors_repository/IBSMesh_2000_2_OnGivenPointCloudWeightedSampler_5_1500_PropagateNormalObjectPoissonDiscSamplerClearance_256"
    # json_conf_execution_file = "./data/test_configs/single_testing_reaching_out_up.json"
    # directory_of_trainings = "./output/descriptors_repository/IBSMesh_400_4_OnGivenPointCloudWeightedSampler_5_1500_PropagateNormalObjectPoissonDiscSamplerClearance_256"
    # json_conf_execution_file = "./data/test_configs/single_testing_hanging_umbrella.json"

    directory_env_test_results = "./output/testing_env_single/scene0000_00"
    directory_of_prop_configs = "./output/propagators_configs/scene0000_00"

    scores_ctrl = ControlPointScore(directory_of_trainings, json_conf_execution_file,
                                    directory_env_test_results, directory_of_prop_configs)

    scores_ctrl.start()
