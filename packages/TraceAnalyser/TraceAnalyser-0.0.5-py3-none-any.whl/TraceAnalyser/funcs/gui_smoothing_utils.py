import traceback
from functools import partial
from TraceAnalyser.funcs.gui_worker import Worker
from scipy.ndimage import gaussian_filter1d
import numpy as np

class _smoothing_utils:

    def update_smooth_options(self):

        try:
            smooth_type = self.smoothing_window.smooth_type.currentText()

            if smooth_type == "Moving Average":

                self.smoothing_window.smooth_option1.show()
                self.smoothing_window.smooth_option1_label.show()

                self.smoothing_window.smooth_option2.hide()
                self.smoothing_window.smooth_option2_label.hide()

                window_size_list = [2,3,5,10,20,50,100]
                window_size_list = [str(i) for i in window_size_list]

                self.smoothing_window.smooth_option1.clear()

                self.smoothing_window.smooth_option1.addItems(window_size_list)
                self.smoothing_window.smooth_option1_label.setText("Window Size")

            if smooth_type == "Gaussian 1D":

                self.smoothing_window.smooth_option1.show()
                self.smoothing_window.smooth_option1_label.show()

                self.smoothing_window.smooth_option2.hide()
                self.smoothing_window.smooth_option2_label.hide()

                sigma_list = [0.5,1,2,3,4,5]
                sigma_list = [str(i) for i in sigma_list]

                self.smoothing_window.smooth_option1.clear()

                self.smoothing_window.smooth_option1.addItems(sigma_list)
                self.smoothing_window.smooth_option1_label.setText("Sigma")

        except:
            print(traceback.format_exc())
            pass


    def smooth_traces_finished(self):

        try:

            self.smoothing_window.smooth_progressbar.setValue(0)
            self.initialise_plot()

        except:
            print(traceback.format_exc())
            pass


    def apply_live_smooth(self, data):

        try:
            smooth_type = self.smoothing_window.smooth_type.currentText()
            smooth_option1 = self.smoothing_window.smooth_option1.currentText()
            smooth_option2 = self.smoothing_window.smooth_option2.currentText()

            if smooth_type == "Moving Average":
                data = self.moving_average(data, smooth_option1)

            if smooth_type == "Gaussian 1D":
                data = self.gaussian_filter(data, smooth_option1)

        except:
            print(traceback.format_exc())
            pass

        return data


    def smooth_traces(self, progress_callback=None,
            smooth_type="Moving Average", smooth_option1=1, smooth_option2=1):

        dataset_name = self.smoothing_window.smooth_dataset.currentText()
        channel_name = self.smoothing_window.smooth_channel.currentText()

        if dataset_name == "All Datasets":
            dataset_list = list(self.data_dict.keys())
        else:
            dataset_list = [dataset_name]

        total_traces = 0
        for dataset_name in dataset_list:
            total_traces += len(self.data_dict[dataset_name])

        n_traces = 0
        for dataset_name in dataset_list:

            dataset_data = self.data_dict[dataset_name]

            for localisation_number, localisation_data in enumerate(dataset_data):

                trace_dict = localisation_data["trace_dict"]
                user_label = localisation_data["user_label"]

                if self.get_filter_status("smooth", user_label) == False:

                    plot_channels = self.get_plot_channel_list(trace_dict, channel_name)

                    for channel in plot_channels:

                        if "efficiency" not in channel.lower():

                            trace_data = trace_dict[channel].copy()

                            if smooth_type == "Moving Average":

                                trace_data = self.moving_average(trace_data, smooth_option1)

                            if smooth_type == "Gaussian 1D":

                                trace_data = self.gaussian_filter(trace_data, smooth_option1)

                            trace_data = np.array(trace_data)

                            self.data_dict[dataset_name][localisation_number]["trace_dict"][channel] = trace_data

                n_traces += 1

                if progress_callback != None:
                    progress = int(((n_traces+1)/total_traces)*100)
                    progress_callback.emit(progress)

    def moving_average(self, data, window_size):

        try:

            if window_size != "":

                window_size = int(window_size)

                data = np.convolve(data, np.ones(window_size)/window_size, mode='same')

        except:
            pass

        return data

    def gaussian_filter(self, data, sigma):

        try:

            if sigma != "":

                sigma = float(sigma)

                data = gaussian_filter1d(data, sigma)

        except:
            pass

        return data


    def initialise_trace_smoothing(self):

        try:

            if self.data_dict != {}:

                smooth_type = self.smoothing_window.smooth_type.currentText()
                smooth_option1 = self.smoothing_window.smooth_option1.currentText()
                smooth_option2 = self.smoothing_window.smooth_option2.currentText()

                if smooth_option1 != "":
                    smooth_option1 = float(smooth_option1)
                else:
                    smooth_option1 = None

                if smooth_option2 != "":
                    smooth_option2 = float(smooth_option2)
                else:
                    smooth_option2 = None

                worker = Worker(self.smooth_traces, smooth_type=smooth_type,
                    smooth_option1=smooth_option1, smooth_option2=smooth_option2)
                worker.signals.progress.connect(partial(self.gui_progrssbar,name="smooth"))
                worker.signals.finished.connect(self.smooth_traces_finished)
                self.threadpool.start(worker)

        except:
            print(traceback.format_exc())
            pass