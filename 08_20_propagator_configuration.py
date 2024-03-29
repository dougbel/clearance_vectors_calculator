import os

from viewer.enviro_scores.ControlScores import ControlScores

if __name__ == '__main__':
    ######################################################
    #SCENE0000_00
    #######################
    # dir_data = "./output/testing_env_single/scene0000_00/filled"
    # dir_output = "./output/propagators_configs/scene0000_00/filled"
    # 8 orientations
    # affordance = "sitting_human_sitting"
    # max_limit_score = 30.36 #76.89
    # max_limit_missing = 23 #115
    # max_limit_cv_collided = 6
    # affordance = "standing_up_floor_human_standing_up"
    # max_limit_score = 19
    # max_limit_missing = 35
    # max_limit_cv_collided = 0
    # affordance = "laying_human_laying"
    # affordance = "child_laying_child_laying"
    # max_limit_score = 20
    # max_limit_missing = 12
    # max_limit_cv_collided = 0
    # affordance = "placing_small_box_small_box"
    # affordance = "placing_large_box_large_box"
    # max_limit_score = 14
    # max_limit_missing = 15
    # max_limit_cv_collided = 0
    affordance = "reaching_out_low_human_reaching_out_low"
    # affordance = "reaching_out_mid_low_human_reaching_out_mid_low"
    # affordance = "reaching_out_mid_up_human_reaching_out_mid_up"
    # affordance = "reaching_out_up_human_reaching_out_up"
    max_limit_score = 75.41
    max_limit_missing = 36
    max_limit_cv_collided = 0
    # affordance = "placing_small_box_small_box"
    # affordance = "placing_large_box_large_box"
    # max_limit_score = 12.4
    # max_limit_missing = 12
    # max_limit_cv_collided = 2
    # affordance = "hanging_umbrella_umbrella"
    # max_limit_score = 12.4
    # max_limit_missing = 1
    # max_limit_cv_collided = 2
    # affordance = "ride_motorbike_ride"
    # max_limit_score = 88.4
    # max_limit_missing = 300
    # max_limit_cv_collided = 2

    # #####################################################
    # HANGING RACK
    # ######################
    # dir_data = "./output/testing_env_single/hanging_rack"
    # dir_output = "./output/propagators_configs/hanging_rack"
    # affordance = "hanging_umbrella_umbrella"
    # max_limit_score = 12.5
    # max_limit_missing = 1
    # max_limit_cv_collided = 2
    # dir_data = "./output/testing_env_single/scene0000_00/filled"
    # dir_output = "./output/propagators_configs/scene0000_00/filled"
    # dir_data = "./output/testing_env_single/scene0000_00"
    # dir_output = "./output/propagators_configs/scene0000_00"
    # affordance = "hanging_umbrella_umbrella"
    # max_limit_score = 12.5
    # max_limit_cv_collided = 2
    # max_limit_missing = 2

    ######################################################
    # living room 1
    #######################
    # dir_data = "./output/testing_env_single/living-room1"
    # dir_output = "./output/propagators_configs/living-room1"
    # affordance = "ride_motorbike_rider"
    # max_limit_score = 102
    # max_limit_missing = 200
    # max_limit_cv_collided = 3


    dir_data = os.path.join(dir_data, affordance)



    scores_ctrl = ControlScores(dir_data, max_limit_score, max_limit_missing, max_limit_cv_collided)

    scores_ctrl.start()

    dir_output = os.path.join(dir_output, affordance)
    scores_ctrl.save_rbf(dir_output)
