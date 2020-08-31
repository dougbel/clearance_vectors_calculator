import numpy as np
import math

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from vtkplotter import Plotter, Points


class ViewScores:

    def __init__(self, controler, max_slide_score, max_slide_missings, slide_score, slide_missings, propagation_epsilon):
        self.controler = controler
        self.max_slide_score = max_slide_score
        self.max_slide_missings = max_slide_missings
        self.min_slide_score = 0
        self.min_slide_missings = 0
        self.slide_score = slide_score
        self.slide_missings = slide_missings
        self.propagation_function = ""
        self.propagation_epsilon = propagation_epsilon

    def show(self, file_env):
        self.vp = Plotter(verbose=0, title="Heat map scores", bg="white", size=(1200, 800))
        self.vp.load(file_env, alpha=0.75)
        self.vp.show(interactive=0)

        slider = self.vp.addSlider2D(self.change_slider_max_score,
                            self.min_slide_score,
                            self.max_slide_score,
                            value=self.slide_score,
                            pos=[(.60, .11), (1, .11)], title="Max score")
        slider.GetRepresentation().SetLabelFormat("%0.2f")

        self.vp.addSlider2D(self.change_slider_max_missing,
                            self.min_slide_missings,
                            self.max_slide_missings,
                            value=self.slide_missings,
                            pos=[(.60, .04), (1, .04)], title="Max missing")

        self.vp.addButton(self.click_show_histograms,
                          pos=(.9, .15), states=["Show histograms"],
                          c=["w"], bc=["firebrick"], font="courier", size=13, bold=True, italic=False)


        slider = self.vp.addSlider2D(self.change_slider_propagation_epsilon, 0, 2,
                            value=self.propagation_epsilon,
                            pos=[(0, .95), (.3, .95)], title="epsilon")
        slider.GetRepresentation().SetLabelFormat("%0.3f")
        self.btns_propagation=[]
        b = self.vp.addButton(self.click_gaussian,
                          pos=(.03, .89), states=["gaussian", "gaussian"],
                          c=["w","w"], bc=["black", 'forestgreen'], font="courier", size=10, bold=True, italic=False)
        self.btns_propagation.append(b)
        b = self.vp.addButton(self.click_multicuadratic,
                          pos=(.1, .89), states=["multiquadric","multiquadric"],
                          c=["w","w"], bc=["black", 'forestgreen'], font="courier", size=10, bold=True, italic=False)
        self.btns_propagation.append(b)
        b = self.vp.addButton(self.click_inverse,
                          pos=(.17, .89), states=["inverse", "inverse"],
                          c=["w","w"], bc=["black", 'forestgreen'], font="courier", size=10, bold=True, italic=False)
        self.btns_propagation.append(b)
        self.click_gaussian()

        self.vp.addButton(self.click_propagate_scores,
                          pos=(.25, .89), states=["Propagate Scores"],
                          c=["w"], bc=["firebrick"], font="courier", size=10, bold=True, italic=False)


    def change_slider_max_score(self, widget, event):
        self.slide_score = widget.GetRepresentation().GetValue()
        self.controler.update_point_visualization()

    def change_slider_max_missing(self, widget, event):
        self.slide_missings = round(widget.GetRepresentation().GetValue())
        self.controler.update_point_visualization()

    def click_show_histograms(self):
        self.controler.show_histograms()

    def click_gaussian(self):
        self.update_status_btns_propagation(0)

    def click_multicuadratic(self):
        self.update_status_btns_propagation(1)

    def click_inverse(self):
        self.update_status_btns_propagation(2)

    def update_status_btns_propagation(self, pos_enable):
        for pos in range(len(self.btns_propagation)):
            if pos_enable == pos:
                self.btns_propagation[pos].status(1)
                self.propagation_function = self.btns_propagation[pos].status()
            else:
                self.btns_propagation[pos].status(0)

    def change_slider_propagation_epsilon(self,  widget, event):
        self. propagation_epsilon = round(widget.GetRepresentation().GetValue(),3)
        print(round(self. propagation_epsilon,3))



    def show_histograms(self, np_score, np_filter_score, np_missings, np_filter_missings):

        mpl.rc('xtick', labelsize=6)
        mpl.rc('ytick', labelsize=6)
        fig, axs = plt.subplots(2, 2)
        fig.canvas.set_window_title(
            "Max score: " + str(round(self.max_slide_score, 2)) + ", Max missings: " + str(self.max_slide_missings))
        mpl.pyplot.subplots_adjust(
            top=0.935, bottom=0.07, left=0.08, right=0.977, hspace=0.324, wspace=0.195)
        plt.ion()
        plt.show()

        bins = math.ceil(self.max_slide_score)
        axs[0, 0].hist(np_score, facecolor='green', alpha=0.5, edgecolor='black')
        axs[0, 0].set_title("Scores histogram [0," + str(bins) + "]", size=8)
        plt.pause(0.02)

        axs[0, 1].hist(np_filter_score, facecolor='green', edgecolor='black')
        axs[0, 1].set_title(
            "Scores histogram [0," + str(round(self.slide_score, 2)) + "]", size=8)
        plt.pause(0.02)

        num_bins = int(np.max(np_missings) / 20)
        axs[1, 0].hist(np_missings, num_bins, facecolor='blue',
                       alpha=0.5, edgecolor='black')
        axs[1, 0].set_title("Missing points histogram [0,512]", size=8)
        plt.pause(0.02)

        num_bins = self.slide_missings
        axs[1, 1].hist(np_filter_missings, bins=[*range(num_bins + 2)],
                       align='left', facecolor='blue', edgecolor='black')
        axs[1, 1].set_title("Missing points histogram [0," +
                            str(self.slide_missings) + "]", size=8)
        plt.pause(0.02)

        plt.draw_all()

        plt.ioff()

    def clean_environment(self):
        while len(self.vp.actors) > 1:
            self.vp.remove(self.vp.actors[1])

    def add_point_cloud(self, np_points, np_scores, r = 5):
        pts = Points(np_points, r=r)
        pts.cellColors(np_scores, cmap='jet',  vmin=self.min_slide_score, vmax=self.slide_score)
        pts.addScalarBar(vmin=self.min_slide_score,
                         vmax=self.slide_score,
                         nlabels=5,
                         title="PV alignment distance",
                         pos=(0.8, 0.25))
        self.vp += pts
        self.vp.show(bg="white", interactive=0)


    def click_propagate_scores(self):
        self.controler.rbf_propagation()


    def show_propagate_scores(self, np_src_points, np_src_scores, np_points, np_scores, epsilon):
        vp2 = Plotter(pos=(500, 250),verbose=0, title="Propagation "+self.propagation_function+", e:"+str(epsilon), bg="white",  size=(800, 800))
        vp2.show(bg="white", interactive=0)

        pts_measure = Points(np_src_points, r=5,  alpha=0.5)
        pts_measure.cellColors(np_src_scores, cmap='jet_r', vmin=0, vmax=1)
        vp2 += pts_measure
        pts_measure = Points(np_points, r=5, )
        pts_measure.cellColors(np_scores, cmap='jet_r' ,vmin=0, vmax=1)
        vp2 += pts_measure

        pts_measure.addScalarBar(vmin=0, vmax=1, nlabels=5, title="Support score", pos=(0.8, 0.25))

        vp2.show(interactive=1)

# def show_mapped_scores(np_points, np_scores):
#     vp2 = Plotter(pos=(500, 250),verbose=0, title="Mapped scores ",bg="black",  size=(800, 800))
#     vp2.show( interactive=0)
#     pts_measure = Points(np_points, r=5,  alpha=0.5)
#     pts_measure.cellColors(np_scores, vmin=0, vmax=1)
#     pts_measure.addScalarBar(vmin=0, vmax=1, nlabels=5, pos=(0.8, 0.25))
#     vp2 += pts_measure
#     vp2.show(interactive=1)