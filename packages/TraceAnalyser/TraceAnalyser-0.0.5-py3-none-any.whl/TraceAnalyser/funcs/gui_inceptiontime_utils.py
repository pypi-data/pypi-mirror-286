import importlib
import os.path
from importlib import resources
import traceback
import glob
import torch
from functools import partial
from TraceAnalyser.funcs.gui_worker import Worker
import numpy as np
import sklearn


class _inceptiontime_methods:

    def load_inceptiontime_model(self, model_path=""):

        try:

            if os.path.exists(model_path) == False:
                model_directory = resources.files(importlib.import_module(f'TraceAnalyser.InceptionTime'))
                model_directory = os.path.normpath(model_directory)
                model_directory = os.path.join(model_directory, "models")

                model_paths = glob.glob(f'{model_directory}/*.h5')
                model_paths = [path for path in model_paths if ".py" not in path]
                model_path = model_paths[0]

            if os.path.isfile(model_path):
                model_path = os.path.normpath(model_path)

                from tsai.all import InceptionTime

                model = InceptionTime(1,2)

                if torch.cuda.is_available():
                    device = torch.device("cuda")
                    model_weights = torch.load(model_path)['model_state_dict']
                else:
                    device = torch.device("cpu")
                    model_weights = torch.load(model_path, map_location=torch.device('cpu'))['model_state_dict']

                model.load_state_dict(state_dict=model_weights)

                model.to(device)

        except:
            print(traceback.format_exc())
            inceptionTime = None
            pass

        return model, device

    def get_prediction_data(self):
        def rescale01(X):
            X = (X - np.min(X)) / (np.max(X) - np.min(X))
            return X
        def normalize99(X):
            sklearn.preprocessing.minmax_scale(X, feature_range=(0, 1), axis=0, copy=True)
            return X

        predict_data = {}
        n_traces = 0

        try:

            dataset_name = self.detect_window.detect_dataset.currentText()
            channel_name = self.detect_window.detect_channel.currentText()
            detect_mode_index = self.detect_window.detect_mode.currentIndex()
            crop_data = True

            if dataset_name == "All Datasets":
                dataset_list = list(self.data_dict.keys())
            else:
                dataset_list = [dataset_name]

            for dataset_name in dataset_list:

                if detect_mode_index == 0:
                    if dataset_name not in predict_data.keys():
                        predict_data[dataset_name] = {}
                else:
                    if "All Datasets" not in predict_data.keys():
                        predict_data["All Datasets"] = {}

                for localisation_index, localisation_data in enumerate(self.data_dict[dataset_name]):

                    trace_dict = localisation_data["trace_dict"]
                    user_label = localisation_data["user_label"]
                    crop_range = localisation_data["crop_range"]

                    if self.get_filter_status("inceptiontime", user_label) == False:

                        if detect_mode_index == 0:
                            if localisation_index not in predict_data[dataset_name].keys():
                                predict_data[dataset_name][localisation_index] = []
                        else:
                            if localisation_index not in predict_data["All Datasets"].keys():
                                predict_data["All Datasets"][localisation_index] = []

                        data = trace_dict[channel_name].copy()

                        if crop_data == True and len(crop_range) == 2:
                            crop_range = sorted(crop_range)
                            if crop_range[0] < 0:
                                crop_range[0] = 0
                            if crop_range[1] > len(data):
                                crop_range[1] = len(data)

                            data = data[int(crop_range[0]):int(crop_range[1])]

                        data = np.array(data)
                        data = normalize99(data)
                        data = rescale01(data)

                        if detect_mode_index == 0:
                            predict_data[dataset_name][localisation_index].append(data)
                        else:
                            predict_data["All Datasets"][localisation_index].append(data)

            for dataset in predict_data.keys():
                for localisation_index in predict_data[dataset].keys():

                    data = predict_data[dataset][localisation_index]
                    data = np.array(data)

                    if detect_mode_index == 0:
                        data = np.expand_dims(data, axis=0)
                    else:
                        data = np.expand_dims(data, axis=1)

                    data = torch.from_numpy(data).float()

                    predict_data[dataset][localisation_index] = data
                    n_traces += 1

        except:
            print(traceback.format_exc())
            predict_data = {}
            n_traces = 0
            pass

        return predict_data, n_traces

    def _detect_inceptiontime_states(self, progress_callback):

        try:

            label_dict = {0: "Dynamic", 1: "Static"}

            model, device = self.load_inceptiontime_model()

            if model is not None:

                predict_data, n_traces = self.get_prediction_data()

                if n_traces > 0:

                    iter = 0
                    model.eval()

                    for dataset, dataset_data in predict_data.items():
                        for localisation_index, localisation_data in dataset_data.items():

                            data = localisation_data.to(device)

                            with torch.no_grad():
                                prediction = model(data)

                            pred = prediction.cpu().numpy()
                            pred = np.squeeze(pred)

                            pred_class = np.argmax(pred)
                            pred_confidence = torch.nn.functional.softmax(prediction, dim=1).cpu().numpy()[0][pred_class]

                            pred_label = label_dict[pred_class]
                            pred_plot_label = f"{pred_label} [{pred_confidence:.4f}]"

                            if dataset == "All Datasets":
                                dataset_list = list(self.data_dict.keys())
                            else:
                                dataset_list = [dataset]

                            for dataset_name in dataset_list:
                                self.data_dict[dataset_name][localisation_index]["pred_class"] = pred_class
                                self.data_dict[dataset_name][localisation_index]["pred_label"] = label_dict[pred_class]
                                self.data_dict[dataset_name][localisation_index]["pred_conf"] = pred_confidence
                                self.data_dict[dataset_name][localisation_index]["pred_plot_label"] = pred_plot_label

                            iter += 1
                            progress = int(iter/n_traces*100)
                            progress_callback.emit(progress)

        except:
            print(traceback.format_exc())
            self.detect_window.detect_inceptiontime.setEnabled(True)
            self.detect_window.inceptiontime_progressbar.setValue(0)
            pass

    def _detect_inceptiontime_states_cleanup(self):

        try:

            self.print_notification("InceptionTime states detected")

            self.detect_window.detect_inceptiontime.setEnabled(True)
            self.detect_window.inceptiontime_progressbar.setValue(0)

            self.plot_traces(update_plot=True)

        except:
            print(traceback.format_exc())
            pass

    def detect_inceptiontime_states(self):

        try:
            if self.data_dict != {}:

                self.detect_window.detect_inceptiontime.setEnabled(False)

                worker = Worker(self._detect_inceptiontime_states)
                worker.signals.progress.connect(partial(self.gui_progrssbar,name="inceptiontime"))
                worker.signals.finished.connect(self._detect_inceptiontime_states_cleanup)
                self.threadpool.start(worker)

        except:
            print(traceback.format_exc())
            self.detect_window.detect_inceptiontime.setEnabled(True)
            self.detect_window.inceptiontime_progressbar.setValue(0)
            pass



    def update_singletrace_labels(self):

        try:

            if self.data_dict != {}:

                target_label = self.detect_window.singletrace_label.currentText()
                target_user_label = self.detect_window.singletrace_user_label.currentText()

                for dataset_name, dataset_data in self.data_dict.items():
                    for localisation_index, localisation_data in enumerate(dataset_data):

                        pred_label = localisation_data["pred_label"]

                        if pred_label == target_label:
                            self.data_dict[dataset_name][localisation_index]["user_label"] = int(target_user_label)

                self.plot_traces(update_plot=True)
                self.print_notification("Labels updated")

        except:
            print(traceback.format_exc())
            pass

    def update_multitrace_labels(self):

        try:

            if self.data_dict != {}:

                target_label = self.detect_window.multitrace_label.currentText()
                min_number = self.detect_window.multitrace_min_traces.currentText()
                target_user_label = self.detect_window.multitrace_user_label.currentText()

                prediction_memory = {}

                for dataset_name, dataset_data in self.data_dict.items():
                    for localisation_index, localisation_data in enumerate(dataset_data):

                        if "pred_label" in localisation_data.keys():

                            if localisation_index not in prediction_memory.keys():
                                prediction_memory[localisation_index] = []

                            pred_label = localisation_data["pred_label"]

                            if pred_label == target_label:
                                prediction_memory[localisation_index].append(dataset_name)

                for localisation_index, dataset_list in prediction_memory.items():
                    if len(dataset_list) >= int(min_number):
                        for dataset_name, dataset_data in self.data_dict.items():
                            self.data_dict[dataset_name][localisation_index]["user_label"] = int(target_user_label)

                self.plot_traces(update_plot=True)
                self.print_notification("Labels updated")

        except:
            print(traceback.format_exc())