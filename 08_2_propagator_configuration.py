import os

from viewer.ControlScores import ControlScores

if __name__ == '__main__':
    ######################################################
    #SCENE0000_00
    #######################
    # 8 orientetions
    dir_data = "./data/to_test"
    dir_output = "./output/to_test/"
    # affordance = "laying_human_laying"
    # affordance = "child_laying_child_laying"
    # max_limit_score = 12.4
    # max_limit_missing = 12
    affordance = "reaching_out_low_human_reaching_out_low"
    # affordance = "reaching_out_mid_low_human_reaching_out_mid_low"
    # affordance = "reaching_out_mid_up_human_reaching_out_mid_up"
    # affordance = "reaching_out_up_human_reaching_out_up"
    max_limit_score = 75.41
    max_limit_missing = 36
    # affordance = "placing_small_box_small_box"
    # affordance = "placing_large_box_large_box"
    # max_limit_score = 12.4
    # max_limit_missing = 12
    # affordance = "hanging_umbrella_umbrella"
    # max_limit_score = 12.4
    # max_limit_missing = 1

    # ######################
    # 16 orientations
    # dir_data = "./data/scene0000_00/16_orientations"
    # dir_output = "./output/scene0000_00/16_orientations"
    # affordance = "reaching_out_low_human_reaching_out_low"
    # max_limit_score = 75.41
    # max_limit_missing = 36

    # #####################################################
    # HANGING RACK
    # ######################
    # dir_data = "./data/hanging_rack"
    # dir_output = "./output/hanging_rack"
    # affordance = "hanging_umbrella_umbrella"
    # max_limit_score = 12.5
    # max_limit_missing = 1

    dir_data = os.path.join(dir_data, affordance)

    # sitting
    # dir_data = os.path.join(dir_data, "sitting_ottoman_human_sitting")
    # max_limit_score = 76.89
    # max_limit_missing = 115

    scores_ctrl = ControlScores(dir_data, max_limit_score, max_limit_missing)

    scores_ctrl.start()

    dir_output = os.path.join(dir_output, affordance)
    scores_ctrl.save_rbf(dir_output)
