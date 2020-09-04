import json
import os
import pickle

import numpy as np
import pandas as pd
import trimesh
from scipy.interpolate import Rbf
from tqdm import trange

from si.fulldataclearancescores import FullDataClearanceScores
from viewer.ViewScores import ViewScores


class ControlScores:
    BATCH_PROPAGATION = 10000

    interpolator = None

    def __init__(self, path, limit_score, limit_missing, limit_cv_collided):
        self.working_directory = path
        self.scores_data, propagation_epsilon = self.__read_scores()

        self.view = ViewScores(self, self.scores_data.max_score, 512, 100, limit_score, limit_missing,
                               limit_cv_collided, propagation_epsilon)
        self.file_mesh_env = os.path.join(path, "test_environment.ply")  # "scene0000_00_vh_clean_2.ply")

    def __read_scores(self):
        scores_data_file = os.path.join(self.working_directory, "test_scores.csv")
        test_execution_data_file = os.path.join(self.working_directory, "test_data.json")
        df_scores_data = pd.read_csv(scores_data_file)
        propagation_epsilon = 0.1
        with open(test_execution_data_file) as jsonfile:
            test_json = json.load(jsonfile)
            propagation_epsilon = test_json['testing_radius'] * 2
            affordance_name = test_json['tester_info']['interactions'][0]['affordance_name']

        scores_data = FullDataClearanceScores(df_scores_data, affordance_name)
        return scores_data, propagation_epsilon

    def start(self):
        self.view.show(self.file_mesh_env)
        self.update_point_visualization()

    def update_point_visualization(self):
        self.view.clean_environment()
        # extract and draw information about filtered points
        np_filtered_points, np_filtered_scores, __, __ = self.scores_data.filter_data_scores(self.view.slide_score,
                                                                                         self.view.slide_missings,
                                                                                         self.view.slide_cv_collided)
        self.view.add_point_cloud(np_filtered_points, np_filtered_scores)

        # draw sampled points with environment BAD normal
        scores = np.zeros(self.scores_data.np_bad_normal_points.shape[0])
        scores.fill(self.view.slide_score)
        self.view.add_point_cloud(self.scores_data.np_bad_normal_points, scores, r=5)
        self.view.vp.show(interactive=1)

    def show_histograms(self):
        __, np_filtered_scores, np_filtered_missings, __ = self.scores_data.filter_data_scores(self.view.slide_score,
                                                                                           self.view.slide_missings,
                                                                                           self.view.slide_cv_collided)
        __, np_raw_points_scores, np_raw_points_missings, np_raw_cv_collided = self.scores_data.get_raw_data()
        self.view.show_histograms(np_raw_points_scores, np_filtered_scores, np_raw_points_missings,
                                  np_filtered_missings)

    def rbf_propagation(self):
        function = self.view.propagation_function
        epsilon = self.view.propagation_epsilon

        bad_normal_points = self.scores_data.np_bad_normal_points
        bad_normal_scores = np.zeros(self.scores_data.np_bad_normal_points.shape[0])

        np_filtered_points, np_filtered_scores, __, __ = self.scores_data.filter_data_scores(self.view.slide_score,
                                                                                         self.view.slide_missings,
                                                                                         self.view.slide_cv_collided)
        # MAPPING SCORES TO [0,1]
        np_filtered_scores_mapped = [-value_in / self.view.slide_score + 1 for value_in in np_filtered_scores]

        # num_filtered_points = np_filtered_points.shape[0]
        np_full_points = np.concatenate((np_filtered_points, bad_normal_points), axis=0)
        np_full_scores = np.concatenate((np_filtered_scores_mapped, bad_normal_scores), axis=0)

        np_new_points = np.asarray(trimesh.load_mesh(self.file_mesh_env).vertices)

        # Radial Basis Function interpolator
        self.interpolator = Rbf(np_full_points[:, 0], np_full_points[:, 1], np_full_points[:, 2],
                                np_full_scores, function=function, epsilon=epsilon)

        np_new_scores = np.array([])
        for i in trange(0, np_new_points.shape[0], self.BATCH_PROPAGATION, desc="Scores propagation"):
            batch = np_new_points[i:i + self.BATCH_PROPAGATION]
            temp = self.interpolator(batch[:, 0], batch[:, 1], batch[:, 2])
            np_new_scores = np.concatenate((np_new_scores, temp), axis=0)

        # self.view.clean_environment()
        self.view.show_propagate_scores(np_full_points, np_full_scores, np_new_points, np_new_scores, epsilon)

    def save_rbf(self, dir_output=None):

        if dir_output is None:
            dir_output = self.working_directory

        if not os.path.exists(dir_output):
            os.makedirs(dir_output)

        rbf_pickle = open(os.path.join(dir_output, "propagation_rbf.pkl"), 'wb')
        pickle.dump(self.interpolator, rbf_pickle)
        rbf_pickle.close()

        data = {'max_limit_score': self.view.slide_score,
                'max_limit_missing': self.view.slide_missings,
                'batch': self.BATCH_PROPAGATION,
                'epsilon': self.view.propagation_epsilon,
                'function': self.view.propagation_function}

        with open(os.path.join(dir_output, 'propagation_data.json'), 'w') as outfile:
            json.dump(data, outfile, indent=4)
