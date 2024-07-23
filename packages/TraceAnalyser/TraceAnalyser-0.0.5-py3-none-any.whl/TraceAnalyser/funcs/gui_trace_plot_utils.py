from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QCheckBox, QScrollArea, QSizePolicy
import numpy as np
import pyqtgraph as pg
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import traceback
from functools import partial
import uuid
import copy
import re
from PyQt5.QtGui import QColor, QFont

class _trace_plotting_methods:


    def check_plot_item_exists(self, plot, item):

        for item in plot.items:
            if item is item:
                return True

        return False

    def get_plot_item_instance(self, plot, instance):

        for item in plot.items:
            if isinstance(item, instance):
                return item

        return None

    def remove_plot_instance(self, plot, instance):

        for item in plot.items:
            if isinstance(item, instance):
                plot.removeItem(item)

    def get_plot_item(self, plot, name):

        for index, item in enumerate(plot.items):
            if item.name() == name:
                return item

        return None

    def remove_plot_item(self, plot, item):

        try:

            if type(item) == str:
                for item in plot.items:
                    if item.name() == "hmm_mean":
                        plot.removeItem(item)
            else:
                for item in plot.items:
                    if isinstance(item, item):
                        plot.removeItem(item)
        except:
            pass

        return plot

    def filter_data_dict(self):

        user_filter = self.plot_settings.plot_user_group.currentText()

        if user_filter != "None":
            user_filter = int(user_filter)

        localisation_numbers = []

        if user_filter != "None":

            for dataset_name, dataset_data in self.data_dict.items():

                if dataset_name != "All Datasets":

                    for localisation_number in range(len(dataset_data)):
                        user_label = int(dataset_data[localisation_number]["user_label"])

                        filter = False

                        if user_filter != "None":
                            if user_label != user_filter:
                                filter = True

                        if filter == True:
                            dataset_data[localisation_number]["filter"] = True
                        else:
                            localisation_numbers.append(localisation_number)

            self.localisation_numbers = np.unique(localisation_numbers)
            self.n_traces = len(self.localisation_numbers)

        else:
            self.n_traces = np.max([len(self.data_dict[dataset]) for dataset in self.plot_datasets])
            self.localisation_numbers = list(range(self.n_traces))

        return self.localisation_numbers, self.n_traces

    def sort_plot_labels(self, plot_labels):
        try:
            reference_list = ["Data", "Trace",
                              "Donor", "Acceptor",
                              "FRET Efficiency",
                              "DD", "DA", "AD", "AA",
                              "ALEX Efficiency"]

            order = {key: i for i, key in enumerate(reference_list)}

            # Sort the list and place items not in reference_list at the end in original order
            sorted_list = sorted(plot_labels, key=lambda x: (order.get(x, float('inf')), plot_labels.index(x)))

        except Exception as e:
            print(f"An error occurred: {e}")
            return plot_labels

        return sorted_list

    def initialise_plot(self):

        try:

            if self.data_dict != {}:

                plot_data = self.plot_dataset.currentText()
                plot_mode = self.plot_channel.currentText()

                if plot_mode != "" and plot_data != "":

                    self.plot_show_dict = {}

                    if plot_data == "All Datasets":
                        self.plot_datasets = list(self.data_dict.keys())
                    elif plot_data != "":
                        self.plot_datasets = [plot_data]
                    else:
                        self.plot_datasets = []

                    plot_label_dict = {}

                    for dataset_name in self.plot_datasets:

                        plot_labels = list(self.data_dict[dataset_name][0]["trace_dict"].keys())

                        if dataset_name not in plot_label_dict.keys():
                            plot_label_dict[dataset_name] = []

                        if plot_mode in ["All Channels", "Select Channels"]:
                            plot_label_dict[dataset_name].extend(plot_labels)
                        elif plot_mode in plot_labels:
                            plot_label_dict[dataset_name].append(plot_mode)
                        elif plot_mode == "FRET Data" and set(["Donor", "Acceptor"]).issubset(plot_labels):
                            plot_label_dict[dataset_name].extend(["Donor", "Acceptor"])
                        elif plot_mode == "FRET Efficiency" and set(["FRET Efficiency"]).issubset(plot_labels):
                            plot_label_dict[dataset_name].append("FRET Efficiency")
                        elif plot_mode == "FRET Data + FRET Efficiency" and set(["Donor", "Acceptor", "FRET Efficiency"]).issubset(plot_labels):
                            plot_label_dict[dataset_name].extend(["Donor", "Acceptor", "FRET Efficiency"])
                        elif plot_mode == "FRET Correction Data" and set(["Donor", "Acceptor"]).issubset(plot_labels):
                            plot_label_dict[dataset_name].extend(["Donor", "Acceptor"])
                        elif plot_mode == "ALEX Data" and set(["DD", "AA", "DA", "AD"]).issubset(plot_labels):
                            plot_label_dict[dataset_name].extend(["DD", "AA", "DA", "AD"])
                        elif plot_mode == "ALEX Efficiency" and set(["ALEX Efficiency"]).issubset(plot_labels):
                            plot_label_dict[dataset_name].append("ALEX Efficiency")
                        elif plot_mode == "ALEX Data + ALEX Efficiency" and set(["DD", "AA", "DA", "AD", "ALEX Efficiency"]).issubset(plot_labels):
                            plot_label_dict[dataset_name].extend(["DD", "AA", "DA", "AD", "ALEX Efficiency"])
                        elif plot_mode == "ALEX Correction Data" and set(["DD","DA"]).issubset(plot_labels):
                            plot_label_dict[dataset_name].extend(["DD","DA"])

                    self.plot_info = {}

                    for dataset_name, plot_labels in plot_label_dict.items():

                        if dataset_name not in self.plot_info.keys():
                            self.plot_info[dataset_name] = []

                        plot_labels = [label for label in plot_labels if len(self.data_dict[dataset_name][0]["trace_dict"][label]) > 0]

                        plot_labels = self.sort_plot_labels(plot_labels)

                        if len(plot_labels) > 0:
                            self.plot_info[dataset_name].extend(plot_labels)
                        else:
                            if dataset_name in self.plot_datasets and self.plot_mode != "All Channels":
                                self.plot_datasets.remove(dataset_name)

                    if len(self.plot_info.keys()) > 0 and len(self.plot_datasets) > 0:

                        self.localisation_numbers, self.n_traces = self.filter_data_dict()

                        if self.n_traces > 0:
                            slider_value = self.plot_localisation_number.value()
                            if slider_value >= self.n_traces:
                                slider_value = self.n_traces - 1
                                self.plot_localisation_number.setValue(slider_value)

                            self.plot_localisation_number.setMinimum(0)
                            self.plot_localisation_number.setMaximum(self.n_traces - 1)

                            for plot_labels in self.plot_info.values():
                                for label in plot_labels:
                                    self.plot_show_dict[label] = True

                            self.populate_plot_selector()
                            self.plot_traces(update_plot=True)

                        else:
                            self.print_notification("No traces to plot")

        except:
            print(traceback.format_exc())
            pass

    def check_efficiency_graph(self, input_string):
        pattern = r"FRET Data \+ FRET Efficiency|ALEX Data \+ ALEX Efficiency"
        return re.search(pattern, input_string) is not None


    def assign_plot_list(self, plot_line_labels):

        try:

            split = self.plot_settings.plot_split_lines.isChecked()
            combine_fret = self.plot_settings.plot_combine_fret.isChecked()
            separate_efficiency = self.plot_settings.plot_separate_efficiency.isChecked()

            plot_list = []
            plot_line_labels = list(set(plot_line_labels))
            plot_line_labels = self.sort_plot_labels(plot_line_labels)

            if separate_efficiency:
                efficiency_labels = [label for label in plot_line_labels if "Efficiency" in label]
            else:
                efficiency_labels = []

            if efficiency_labels != []:
                plot_line_labels = [label for label in plot_line_labels if label not in efficiency_labels]

            if combine_fret == True:

                fret_labels = ["Donor", "Acceptor", "DD", "DA", "AD", "AA"]
                fret_labels = [label for label in plot_line_labels if label in fret_labels]
                non_fret_labels = [label for label in plot_line_labels if label not in fret_labels]

                if len(fret_labels) > 0:
                    plot_list.append(fret_labels)
                if len(non_fret_labels) > 0:
                    if split:
                        non_fret_labels = [[line] for line in non_fret_labels]
                    else:
                        non_fret_labels = [non_fret_labels]
                    plot_list.extend(non_fret_labels)
            else:
                if split:
                    plot_list = [[line] for line in plot_line_labels]
                else:
                    plot_list = [plot_line_labels]

            if len(efficiency_labels) > 0:
                plot_list.append(efficiency_labels)

        except:
            print(traceback.format_exc())
            pass

        return plot_list


    def update_plot_layout(self):

        try:

            self.plot_grid = {}
            self.unique_crop_regions = []
            self.measure_refs = {}
            self.unique_gamma1_refs = []
            self.unique_gamma2_refs = []

            self.donor_bleach_refs = {}
            self.acceptor_bleach_refs = {}

            self.graph_canvas.clear()

            for plot_index, plot_dataset in enumerate(self.plot_datasets):

                sub_plots = []
                sub_axes = []
                sub_plot_gamma_refs = []
                donor_bleach_refs = []
                acceptor_bleach_refs = []
                sub_plot_crop_regions = []

                plot_line_labels = self.plot_info[plot_dataset]
                plot_line_labels = [label for label in plot_line_labels if self.plot_show_dict[label] == True]

                self.donor_bleach_refs[plot_dataset] = []
                self.acceptor_bleach_refs[plot_dataset] = []

                for plot_label in plot_line_labels:

                    if plot_label in ["Donor", "DD"]:
                        donor_bleach_ref = self.initialise_bleach_ref(dataset=plot_dataset,
                            plot_labels=[plot_label])
                        self.donor_bleach_refs[plot_dataset].append(donor_bleach_ref)
                    else:
                        donor_bleach_ref = None

                    if plot_label in ["Acceptor", "DA"]:
                        acceptor_bleach_ref = self.initialise_bleach_ref(dataset=plot_dataset,
                            plot_labels=[plot_label])
                        self.acceptor_bleach_refs[plot_dataset].append(acceptor_bleach_ref)
                    else:
                        acceptor_bleach_ref = None

                    if plot_label in ["Donor", "Acceptor", "DD", "DA"]:
                        gamma_refs = self.initialise_gamma_refs(dataset=plot_dataset, plot_labels=[plot_label])
                    else:
                        gamma_refs = [None, None]

                    sub_plot_gamma_refs.append(gamma_refs)

                    donor_bleach_refs.append(donor_bleach_ref)
                    acceptor_bleach_refs.append(acceptor_bleach_ref)

                n_plot_lines = len(plot_line_labels)

                sub_plot_list = self.assign_plot_list(plot_line_labels)

                if len(sub_plot_list) > 0:

                    plot_line_list = []
                    plot_line_label_list = []

                    layout = pg.GraphicsLayout()
                    self.graph_canvas.addItem(layout, row=plot_index, col=0)

                    for sub_plot_index, plot_lines in enumerate(sub_plot_list):

                        plot = CustomPlot()
                        plot.enableAutoRange()
                        plot.autoRange()
                        legend = plot.legend
                        legend.anchor(itemPos=(1, 0), parentPos=(1, 0), offset=(-10, 10))

                        layout.addItem(plot, row=sub_plot_index, col=0)
                        sub_axes.append(plot)

                        for line_index, line_label in enumerate(plot_lines):

                            pen = self.get_line_format(line_label, width=2)
                            plot_line = plot.plot(np.zeros(10), pen=pen, name=line_label)

                            plot_line_list.append(plot_line)
                            plot_line_label_list.append(line_label)

                            if self.plot_settings.plot_showy.isChecked() == False:
                                plot.hideAxis('left')

                            if self.plot_settings.plot_showx.isChecked() == False:
                                plot.hideAxis('bottom')

                            if sub_plot_index != len(sub_plot_list) - 1:
                                plot.hideAxis('bottom')

                            if sub_plot_index == 0:
                                self.initialise_text_overlay(plot, dataset=plot_dataset)

                            sub_plots.append(plot)

                            crop_region = self.initialise_crop_region()
                            sub_plot_crop_regions.append(crop_region)

                            plotmeta = plot.metadata
                            plotmeta[line_index] = {"plot_dataset": plot_dataset, "line_label": line_label}

                    localisation_number = self.plot_localisation_number.value()
                    user_label = self.data_dict[plot_dataset][localisation_number]["user_label"]
                    plot_details = f"{plot_dataset}   #:{localisation_number} G:{user_label}"

                    self.plot_grid[plot_index] = {
                        "plot_dataset": plot_dataset,
                        "sub_axes": sub_plots,
                        "unique_sub_axes": sub_axes,
                        "sub_plot_crop_regions": sub_plot_crop_regions,
                        "sub_plot_gamma_refs": sub_plot_gamma_refs,
                        "donor_bleach_refs": donor_bleach_refs,
                        "acceptor_bleach_refs": acceptor_bleach_refs,
                        "plot_lines": plot_line_list,
                        "plot_lines_labels": plot_line_label_list,
                    }

            plot_list = []
            for plot_index, grid in enumerate(self.plot_grid.values()):
                sub_axes = grid["sub_axes"]
                sub_plots = []
                for plot in sub_axes:
                    sub_plots.append(plot)
                    plot_list.append(plot)
            for i in range(1, len(plot_list)):
                plot_list[i].setXLink(plot_list[0])
            if len(plot_list) > 0:
                plot.getViewBox().sigXRangeChanged.connect(lambda: auto_scale_y(plot_list))

        except:
            print(traceback.format_exc())
            pass

        return self.plot_grid


    def get_line_format(self, label, width = 2):

        try:

            if label in ["Donor", "DD"]:
                pen = pg.mkPen(pg.mkPen(color=(0, 255, 0), width=width))

            elif label == "AD":
                pen = pg.mkPen(pg.mkPen(color=(0, 128, 0), width=width+0.5))

            elif label in ["Acceptor", "AA", "DA"]:
                pen = pg.mkPen(pg.mkPen(color=(255, 0, 0), width=width))

            elif label == "DA":
                pen = pg.mkPen(pg.mkPen(color=(128, 0, 0), width=width+0.5))

            elif "Efficiency" in label:
                pen = pg.mkPen(pg.mkPen('b', width=width))

            elif label in ["Data", "Trace"]:
                pen = pg.mkPen(pg.mkPen('r', width=width))

            else:
                pen = pg.mkPen(pg.mkPen('w', width=width+1))

        except:
            print(traceback.format_exc())
            pass

        return pen



    def populate_plot_selector(self):

        try:

            layout = self.plot_settings.selector_layout
            plot_channels = self.plot_channel.currentText()

            for i in range(layout.count()):
                item = layout.itemAt(i)
                widget = item.widget()
                if isinstance(widget, QCheckBox):
                    widget.deleteLater()
                    widget.hide()

            checkboxes = []

            line_list = []
            for plot_labels in self.plot_info.values():
                for label in plot_labels:
                    if label not in line_list:
                        line_list.append(label)

            line_list = set(line_list)
            line_list = self.sort_plot_labels(list(line_list))

            if len(line_list) > 1:
                for col_index, line_label in enumerate(line_list):

                    check_box_name = f"plot_show_{line_label}"
                    check_box_label = f"Show: {line_label}"

                    setattr(self, check_box_name, QCheckBox(check_box_label))
                    check_box = getattr(self, check_box_name)

                    checkboxes.append(check_box)

                    check_box.blockSignals(True)
                    if plot_channels == "Select Channels":
                        if col_index == 0:
                            check_box.setChecked(True)
                        else:
                            check_box.setChecked(False)
                    else:
                        check_box.setChecked(True)

                    check_box.blockSignals(False)
                    check_box.stateChanged.connect(self.plot_checkbox_event)
                    layout.addWidget(check_box)

                    self.plot_show_dict[line_label] = check_box.isChecked()

        except Exception as e:
            print(traceback.format_exc())

    def plot_checkbox_event(self, state):

        try:

            layout = self.plot_settings.selector_layout

            for i in range(layout.count()):
                item = layout.itemAt(i)
                widget = item.widget()
                if isinstance(widget, QCheckBox):
                    label = widget.text()
                    state = widget.isChecked()

                    self.plot_show_dict[label.replace("Show: ","")] = state

            self.plot_traces(update_plot=True)

        except:
            print(traceback.format_exc())
            pass

    def plot_traces(self, update_plot = False, update_checkboxes = False):

        try:

            if self.data_dict != {}:

                if hasattr(self, "plot_grid") == False or update_plot == True:
                    self.plot_grid = self.update_plot_layout()

                if self.plot_grid != {}:

                    slider_value = self.plot_localisation_number.value()
                    crop_plots = self.plot_settings.crop_plots.isChecked()
                    localisation_number = self.localisation_numbers[slider_value]
                    downsample = int(self.plot_settings.plot_downsample.currentText())
                    live_smooth = self.smoothing_window.live_smooth.isChecked()

                    self.plot_measure_ranges(self.plot_grid)

                    for plot_index, grid in enumerate(self.plot_grid.values()):

                        plot_dataset = grid["plot_dataset"]
                        sub_axes = grid["sub_axes"]
                        crop_regions = grid["sub_plot_crop_regions"]
                        gamma_refs = grid["sub_plot_gamma_refs"]
                        donor_bleach_refs = grid["donor_bleach_refs"]
                        acceptor_bleach_refs = grid["acceptor_bleach_refs"]
                        plot_lines = grid["plot_lines"]
                        plot_lines_labels = grid["plot_lines_labels"]

                        localisation_dict = self.data_dict[plot_dataset][localisation_number]
                        trace_dict = localisation_dict["trace_dict"]
                        user_label = localisation_dict["user_label"]
                        crop_range = copy.deepcopy(localisation_dict["crop_range"])
                        gamma_ranges = localisation_dict["gamma_ranges"]

                        plot_details = f"{plot_dataset} [#:{localisation_number} G:{user_label}]"

                        plot_ranges = {"xRange": [0, 100], "yRange": [0, 100]}

                        self.plot_bleach_correction_ranges(localisation_dict, sub_axes, plot_lines_labels,
                            donor_bleach_refs, acceptor_bleach_refs)
                        self.plot_gamma_correction_ranges(localisation_dict, sub_axes,
                            plot_lines_labels, gamma_refs, gamma_ranges)

                        for line_index, (plot, crop_region, line,  plot_label) in enumerate(zip(sub_axes,crop_regions,
                                plot_lines, plot_lines_labels)):

                            if line_index == 0:
                                plot.setTitle(plot_details)

                            legend = plot.legend

                            data = trace_dict[plot_label]
                            data_x = np.arange(len(data))

                            break_points = localisation_dict["break_points"]
                            state_means_x, state_means_y = localisation_dict["state_means"][plot_label]

                            if live_smooth == True:
                                data = self.apply_live_smooth(data)

                            # if "Efficiency" in plot_label:
                            #     data = np.clip(data, 0, 1)

                            if crop_plots == True and len(crop_range) == 2:
                                crop_range = sorted(crop_range)
                                crop_range = [int(crop_range[0]), int(crop_range[1])]
                                data = data[crop_range[0]:crop_range[1]]
                                data_x = data_x[crop_range[0]:crop_range[1]]

                            if self.plot_settings.plot_normalise.isChecked() and "efficiency" not in plot_label.lower():
                                data = (data - np.min(data)) / (np.max(data) - np.min(data))

                            self.plot_detected_states(state_means_x, state_means_y, plot, legend, plot_label, line_index, sub_axes, downsample=1)
                            self.plot_crop_ranges(crop_plots, crop_range, crop_region, crop_regions, plot)
                            self.plot_break_points(break_points, plot)

                            plot_line = plot_lines[line_index]
                            plot_line.setData(data_x, data)
                            plot_line.setDownsampling(ds=downsample)

                            try:
                                if plot_ranges["xRange"][1] < np.max(data_x):
                                    plot_ranges["xRange"][1] = np.max(data_x)
                                if plot_ranges["yRange"][1] < np.max(data):
                                    plot_ranges["yRange"][1] = np.max(data)
                                if plot_ranges["yRange"][0] > np.min(data):
                                    plot_ranges["yRange"][0] = np.min(data)
                                if plot_ranges["xRange"][0] < np.min(data_x):
                                    plot_ranges["xRange"][0] = np.min(data_x)
                            except:
                                pass

                        for line_index, (plot, line, plot_label) in enumerate(zip(sub_axes, plot_lines, plot_lines_labels)):
                            plot.setXRange(min=plot_ranges["xRange"][0], max=plot_ranges["xRange"][1])
                            # plot.enableAutoRange(axis="y")

        except:
            print(traceback.format_exc())
            pass



    def plot_break_points(self, break_points, plot):

        if len(break_points) > 2 and self.show_cpd_breakpoints.isChecked():
            break_points = np.unique(break_points).tolist()

            for break_point in break_points[1:-1]:
                bp = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('g', width=3))
                plot.addItem(bp)
                bp.setPos(break_point)


    def plot_detected_states(self,state_means_x, state_means_y, plot, legend, plot_label, line_index, sub_axes, downsample = 1):

        if self.plot_settings.show_detected_states.isChecked() and len(state_means_x) > 0:
            if self.plot_settings.plot_normalise.isChecked():
                state_means_y = (state_means_y - np.min(state_means_y)) / (np.max(state_means_y) - np.min(state_means_y))

            show_state_means = False

            if "Efficiency" in plot_label:
                show_state_means = True
            if "Efficiency" not in plot_label and line_index == len(sub_axes) - 1:
                show_state_means = True

            if show_state_means == True:
                if hasattr(self, "hmm_mean"):
                    if self.hmm_mean in plot.items:
                        self.hmm_mean.setData(state_means_x, state_means_y)
                    else:
                        self.hmm_mean = plot.plot(state_means_x, state_means_y, pen=pg.mkPen('w', width=3), name="hmm_mean", downsample=downsample)
                        legend.removeItem("hmm_mean")
                else:
                    self.hmm_mean = plot.plot(state_means_x, state_means_y, pen=pg.mkPen('w', width=3), name="hmm_mean", downsample=downsample)
                    legend.removeItem("hmm_mean")

            else:
                if hasattr(self, "hmm_mean"):
                    if self.hmm_mean in plot.items:
                        plot.removeItem(self.hmm_mean)
        else:
            if hasattr(self, "hmm_mean"):
                if self.hmm_mean in plot.items:
                    plot.removeItem(self.hmm_mean)






def auto_scale_y(sub_plots):

    try:

        for p in sub_plots:
            data_items = p.listDataItems()

            if not data_items:
                return

            y_min = np.inf
            y_max = -np.inf

            # Get the current x-range of the plot
            plot_x_min, plot_x_max = p.getViewBox().viewRange()[0]

            for index, item in enumerate(data_items):
                if item.name() != "hmm_mean":

                    y_data = item.yData
                    x_data = item.xData

                    # Get the indices of y_data that lies within the current x-range and y data is finite
                    idx = np.where((x_data >= plot_x_min) &
                                   (x_data <= plot_x_max) &
                                   (np.isfinite(y_data)))

                    if len(idx[0]) > 0:  # If there's any data within the x-range
                        y_min = min(y_min, y_data[idx].min())
                        y_max = max(y_max, y_data[idx].max())

                    if plot_x_min < 0:
                        x_min = 0
                    else:
                        x_min = plot_x_min

                    if plot_x_max > x_data.max():
                        x_max = x_data.max()
                    else:
                        x_max = plot_x_max

            p.getViewBox().setYRange(y_min, y_max, padding=0)
            p.getViewBox().setXRange(x_min, x_max, padding=0)

    except:
        pass


class CustomPlot(pg.PlotItem):

    def __init__(self, title="", colour="", label="", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.metadata = {}

        self.setMenuEnabled(False)
        self.symbolSize = 100

        legend = self.addLegend(offset=(10, 10))
        legend.setLabelTextSize("8pt")
        self.hideAxis('top')
        self.hideAxis('right')
        self.getAxis('left').setWidth(30)

        self.title = title
        self.colour = colour

        if self.title != "":
            self.setLabel('top', text=title, size="3pt", color=colour)


    def setMetadata(self, metadata_dict):
        self.metadata = metadata_dict

    def getMetadata(self):
        return self.metadata


class CustomPyQTGraphWidget(pg.GraphicsLayoutWidget):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.frame_position_memory = {}
        self.frame_position = None

        # Set the focus policy to accept focus
        self.setFocusPolicy(Qt.StrongFocus)
        # Enable mouse tracking if you want to focus the widget when the mouse hovers over it
        self.setMouseTracking(True)

    def enterEvent(self, event):
        self.setFocus()

    def mousePressEvent(self, event):

        if hasattr(self.parent, "plot_grid"):

            if event.modifiers() in [Qt.ControlModifier, Qt.AltModifier, Qt.ShiftModifier]:

                dataset, plot_labels, xpos = self.get_mouse_press_postion(event, mode="click")

            if event.modifiers() & Qt.ControlModifier:
                self.parent.update_crop_range(xpos,plot_labels=plot_labels, dataset=dataset)

            elif event.modifiers() & Qt.AltModifier:
                self.parent.update_gamma_ranges(xpos,plot_labels=plot_labels, dataset=dataset)

            elif event.modifiers() & Qt.ShiftModifier:
                self.parent.update_bleach_range(xpos,plot_labels=plot_labels, dataset=dataset)

            super().mousePressEvent(event)  # Process the event further

    def keyPressEvent(self, event):

        if event.key() in [Qt.Key_C, Qt.Key_B, Qt.Key_G, Qt.Key_M]:

            if hasattr(self.parent, "plot_grid"):

                dataset, labels, xpos, plot = self.get_key_press_position(event)

                if event.key() == Qt.Key_C:
                    self.parent.update_crop_range(xpos, plot_labels=labels, dataset=dataset)

                elif event.key() == Qt.Key_B:
                    self.parent.update_bleach_range(xpos, plot_labels=labels, dataset=dataset)

                elif event.key() == Qt.Key_G:
                    self.parent.update_gamma_ranges(xpos, plot_labels=labels, dataset=dataset)

                elif event.key() == Qt.Key_M:
                    self.parent.update_measure_range(event, xpos, plot=plot, plot_labels=labels, dataset=dataset)

        else:

            if event.key() == Qt.Key_Escape:
                self.close()
            else:
                self.parent.keyPressEvent(event)

    def get_key_press_position(self, event):

        try:

            xpos = None
            plot_labels = []
            plot_dataset = ""
            active_plot = None

            if hasattr(self.parent, "plot_grid"):

                # Fetch global cursor position
                globalPos = QCursor.pos()
                localPos = self.mapFromGlobal(globalPos)

                # Iterate over all plots
                plot_grid = self.parent.plot_grid

                for plot_index, grid in enumerate(plot_grid.values()):
                    sub_axes = grid["sub_axes"]
                    plot_lines_labels = grid["plot_lines_labels"]
                    dataset = grid["plot_dataset"]

                    for axes_index, (plot, labels) in enumerate(zip(sub_axes, plot_lines_labels)):
                        viewbox = plot.vb

                        if viewbox.sceneBoundingRect().contains(localPos):
                            plot_coords = viewbox.mapSceneToView(localPos)
                            xpos = plot_coords.x()
                            plot_labels.append(labels)
                            plot_dataset = dataset
                            active_plot = plot
                            break

            if type(plot_labels) == str:
                plot_labels = [plot_labels]

        except:
            xpos = None
            plot_labels = []
            plot_dataset = ""

        return plot_dataset, plot_labels, xpos, plot


    def get_mouse_press_postion(self, event,  mode="click"):

        self.xpos = None
        plot_labels = []
        plot_dataset = ""

        if hasattr(self.parent, "plot_grid"):

            if mode == "click":
                pos = event.pos()
                self.scene_pos = self.mapToScene(pos)
            else:
                pos = QCursor.pos()
                self.scene_pos = self.mapFromGlobal(pos)

            # Iterate over all plots
            plot_grid = self.parent.plot_grid

            for plot_index, grid in enumerate(plot_grid.values()):
                sub_axes = grid["sub_axes"]
                plot_lines_labels = grid["plot_lines_labels"]
                dataset = grid["plot_dataset"]

                for axes_index, (plot, labels) in enumerate(zip(sub_axes,plot_lines_labels)):
                    viewbox = plot.vb

                    if viewbox.sceneBoundingRect().contains(self.scene_pos):
                        plot_coords = viewbox.mapSceneToView(self.scene_pos)
                        plot_labels.append(labels)
                        plot_dataset = dataset

            self.xpos = plot_coords.x()

        if type(plot_labels) == str:
            plot_labels = [plot_labels]

        return dataset, plot_labels, self.xpos










