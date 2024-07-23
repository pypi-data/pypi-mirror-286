import traceback
import pomegranate as pg
import numpy as np
import hmmlearn.hmm as hmm
from TraceAnalyser.funcs.gui_worker import Worker
from functools import partial


class _HMM_methods:

    def get_combo_box_items(self, combo_box):
        items = []
        for index in range(combo_box.count()):
            items.append(combo_box.itemText(index))
        return items


    def update_hmm_fit_algo(self):

        try:

            hmm_package = self.fitting_window.hmm_package.currentText()

            if hmm_package == "Pomegranate":
                hmm_fit_algos = ["Baum-Welch", "Viterbi", "Auto"]
            elif hmm_package == "HMM Learn":
                hmm_fit_algos = ["Diag", "Spherical", "Full", "Tied", "Auto"]

            self.fitting_window.hmm_fit_algo.blockSignals(True)
            self.fitting_window.hmm_fit_algo.clear()
            self.fitting_window.hmm_fit_algo.addItems(hmm_fit_algos)
            self.fitting_window.hmm_fit_algo.blockSignals(False)

        except:
            print(traceback.format_exc())
            pass

    def format_hmm_fit_data(self, fit_data, hmm_package, crop_range=None):

        try:

            fit_data = np.array(fit_data)

            if hmm_package == "Pomegranate":

                if len(fit_data.shape) != 2:
                    fit_data = np.expand_dims(fit_data, axis=1)

            elif hmm_package == "HMM Learn":

                if len(fit_data.shape) != 2:
                    fit_data = np.expand_dims(fit_data, axis=1)

            if crop_range != None:
                if len(crop_range) == 2:
                    crop_range = sorted(crop_range)
                    if crop_range[0] < 0:
                        crop_range[0] = 0
                    if crop_range[1] > len(fit_data):
                        crop_range[1] = len(fit_data)

                    fit_data = fit_data[int(crop_range[0]):int(crop_range[1])]

        except:
            print(traceback.format_exc())
            pass

        return fit_data

    def get_hmm_fit_data(self, dataset_name=None, channel_name=None, hmm_package = None,
            crop=None, concat_traces = None):

        try:

            if dataset_name is None:
                dataset_name = self.fitting_window.hmm_fit_dataset.currentText()
            if channel_name is None:
                channel_name = self.fitting_window.hmm_fit_channel.currentText()
            if hmm_package is None:
                hmm_package = self.fitting_window.hmm_package.currentText()
            if crop is None:
                crop = self.fitting_window.hmm_crop_plots.isChecked()

            fit_dataset = {}
            fit_dataset_lengths = []

            if dataset_name in self.data_dict.keys():

                for localisation_index, localisation_data in enumerate(self.data_dict[dataset_name]):

                    trace_dict = localisation_data["trace_dict"]
                    channel_keys = list(trace_dict.keys())

                    user_label = localisation_data["user_label"]

                    if crop == True:
                        crop_range = localisation_data["crop_range"]
                    else:
                        crop_range = None

                    if self.get_filter_status("hmm", user_label) == False:

                        if channel_name != "FRET":

                            if channel_name in channel_keys:

                                if localisation_index not in fit_dataset.keys():
                                    fit_dataset[localisation_index] = {}

                                fit_data = trace_dict[channel_name]

                                # if "efficiency" in channel_name.lower():
                                #     fit_data = fit_data[fit_data > 0]

                                fit_data = self.format_hmm_fit_data(fit_data, hmm_package, crop_range)

                                fit_dataset[localisation_index] = fit_data
                                fit_dataset_lengths.append(fit_data.shape[0])

                        else:
                            if "Donor" in channel_keys and "Acceptor" in channel_keys:

                                if localisation_index not in fit_dataset.keys():
                                    fit_dataset[localisation_index] = {}

                                donor_trace = trace_dict["Donor"]
                                acceptor_trace = trace_dict["Acceptor"]

                                fit_data = np.stack((donor_trace, acceptor_trace), axis=1)

                                fit_data = self.format_hmm_fit_data(fit_data, hmm_package, crop_range)

                                fit_dataset[localisation_index] = fit_data
                                fit_dataset_lengths.append(fit_data.shape[0])

        except:
            print(traceback.format_exc())
            pass

        return fit_dataset

    def detect_hmm_states_finished(self):

        try:
            self.fitting_window.hmm_progressbar.setValue(0)
            self.fitting_window.hmm_detect_states.setEnabled(True)

            self.plot_traces(update_plot=True)

        except:
            print(traceback.format_exc())
            pass

    def count_transitions(self, data):

        # Count of transitions
        count = 0

        try:
            # Iterate through the list
            for i in range(1, len(data)):
                # Check if the current element is different from the previous one
                if data[i] != data[i - 1]:
                    count += 1

        except:
            print(traceback.format_exc())

        return count



    def detect_hmm_states(self):

        try:

            self.fitting_window.hmm_detect_states.setEnabled(False)

            worker = Worker(self._detect_hmm_states)
            worker.signals.progress.connect(partial(self.gui_progrssbar,name="hmm"))
            worker.signals.finished.connect(self.detect_hmm_states_finished)
            self.threadpool.start(worker)

        except:
            self.fitting_window.hmm_detect_states.setEnabled(True)
            self.fitting_window.hmm_progressbar.setValue(0)
            print(traceback.format_exc())
            pass

    def find_peaks_with_moving_average(self, data, window_size=5, threshold=0.2):
        """
        Find peaks in 1D data using a moving average filter.

        Parameters:
        data (numpy.array): 1D array of data points.
        window_size (int): Size of the moving average window.
        threshold (float): Threshold value to identify a peak.

        Returns:
        numpy.array: Indices of the peaks.
        """
        # Calculate the moving average using a convolution
        moving_avg = np.convolve(data, np.ones(window_size) / window_size, mode='valid')

        # Find where the data exceeds the moving average by the threshold
        peaks = np.where(data[window_size - 1:] > moving_avg + threshold)[0]
        # Adjust the indices because of the convolution 'valid' mode
        peaks += window_size - 1

        return peaks

    def _detect_hmm_states(self, progress_callback=None):

        try:

            dataset_name = self.fitting_window.hmm_fit_dataset.currentText()

            n_states = self.fitting_window.hmm_n_states.currentText()
            n_init = int(self.fitting_window.hmm_n_init.text())
            fit_algo = self.fitting_window.hmm_fit_algo.currentText()
            hmm_package = self.fitting_window.hmm_package.currentText()
            hmm_mode = self.fitting_window.hmm_mode.currentIndex()
            n_iter = int(self.fitting_window.hmm_n_iterations.text())
            min_length = self.fitting_window.hmm_min_length.text()
            max_transitions = self.fitting_window.hmm_max_transitions.text()

            if hmm_mode == 0:
                concat_traces = True
            else:
                concat_traces = False

            fit_dataset = self.get_hmm_fit_data()

            n_traces = len(fit_dataset.keys())

            hmm_models = {}

            self.print_notification("Fitting HMM Model(s)...")

            if concat_traces == False:

                for fit_index, (trace_index, fit_data) in enumerate(fit_dataset.items()):

                    if hmm_package == "Pomegranate":
                        model = pg_fit_hmm(fit_data, n_states, n_iter, n_init, fit_algo)
                    elif hmm_package == "HMM Learn":
                        model = hmmlearn_fit_hmm(fit_data, n_states, n_iter, n_init, fit_algo)

                    hmm_models[trace_index] = model

                    progress = int(100*(fit_index+1)/n_traces)

                    if progress_callback is not None:
                        progress_callback.emit(progress)

            else:

                if hmm_package == "Pomegranate":

                    fit_data = list(fit_dataset.values())
                    model = pg_fit_hmm(fit_data, n_states)

                elif hmm_package == "HMM Learn":

                    lengths = [len(trace) for trace in fit_dataset.values()]
                    fit_data = np.concatenate(list(fit_dataset.values()), axis=0)

                    model = hmmlearn_fit_hmm(fit_data, n_states, lengths=lengths)

                if model != None:
                    for trace_index in fit_dataset.keys():
                        hmm_models[trace_index] = model

                if progress_callback is not None:
                    progress_callback.emit(100)

            self.print_notification("Predicting HMM states...")

            combined_predictions = []

            for fit_index, (trace_index, fit_data) in enumerate(fit_dataset.items()):

                localisation_data = self.data_dict[dataset_name][trace_index]

                model = hmm_models[trace_index]

                predictions = np.zeros_like(fit_data.shape[0]).tolist()

                if model != None:

                    if hmm_package == "Pomegranate":
                        predictions = pg_predict_hmm(model, fit_data)
                    elif hmm_package == "HMM Learn":
                        predictions = hmmlearn_predict_hmm(model, fit_data)

                    if predictions is not None:
                        if len(predictions) == len(fit_data):

                            predictions = correct_hmm_predictions(predictions,
                                min_length, max_transitions)

                            predictions = reasign_hmm_states(fit_data, predictions)

                localisation_data["states"] = list(predictions)
                combined_predictions.append(predictions)

                if progress_callback is not None:
                    progress = int(100 * (fit_index + 1) / n_traces)
                    progress_callback.emit(progress)

            self.print_notification("Computing state means...")
            self.compute_state_means(dataset_name=dataset_name)

            self.print_notification("State detection complete.")

        except:
            self.fitting_window.hmm_detect_states.setEnabled(True)
            print(traceback.format_exc())
            pass

def reasign_hmm_states(fit_data, predictions):

    try:

        unique_states = np.unique(predictions)
        state_mapping = {}

        # Sort unique states based on their mean data values
        sorted_states = sorted(unique_states, key=lambda state: np.mean(fit_data[predictions == state]))

        # Create a new array to store the re-assigned states
        updated_states = np.zeros_like(predictions)

        # Assign new states based on the sorted order
        for i, old_state in enumerate(sorted_states):
            state_mapping[old_state] = i
            updated_states[predictions == old_state] = i

    except:
        print(traceback.format_exc())
        pass

    return updated_states


def pg_fit_hmm(data, n_states, n_iter=1000, n_init=1,
        fit_algo="baum-welch"):

    try:
        # note that the data should be in the shape (trace,n_frames,features)

        best_score = float("-inf")
        best_model = None
        best_model_type = None
        best_n_states = None

        fit_algo = fit_algo.lower()

        if fit_algo == "auto":
            fit_algo_list = ["baum-welch", "viterbi"]
        else:
            fit_algo_list = [fit_algo]

        if type(n_states) == str:
            if n_states.lower() == "auto":
                n_states = range(2, 5)
            else:
                n_states = [int(n_states)]
        else:
            n_states = [int(n_states)]

        for mode in fit_algo_list:
            for state in n_states:

                model = pg.HiddenMarkovModel.from_samples(pg.NormalDistribution,
                    n_components=state,
                    max_iterations=n_iter,
                    X=data,
                    n_jobs=1,
                    algorithm=mode,
                    n_init=n_init,
                )

                score = model.log_probability(data)

                if score > best_score:
                    best_score = score
                    best_model = model
                    best_model_type = mode
                    best_n_states = state

    except:
        print(traceback.format_exc())
        model = None
        pass

    return best_model

def pg_predict_hmm(model, data):

    try:

        if model is not None:

            predictions = model.predict(data)

        else:
            predictions = None

    except:
        print(traceback.format_exc())
        predictions = None
        pass

    return predictions

def hmmlearn_fit_hmm(data, n_states, n_iter=1000, n_init=1,
fit_algo="diag", lengths=None):

    try:

        best_score = float("-inf")
        best_model = None
        best_model_type = None
        best_n_states = None

        fit_algo = fit_algo.lower()

        if fit_algo == "auto":
            fit_algo_list = ["spherical", "diag", "full", "tied"]
        else:
            fit_algo_list = [fit_algo]

        if type(n_states) == str:
            if n_states.lower() == "auto":
                n_states = range(2, 5)
            else:
                n_states = [int(n_states)]
        else:
            n_states = [int(n_states)]

        if lengths is None:
            lengths = [len(data)]

        for mode in fit_algo_list:
            for state in n_states:
                for i in range(n_init):

                    try:
                        model = hmm.GaussianHMM(
                            n_components=state,
                            n_iter=n_iter,
                            covariance_type=mode,
                            random_state=np.random.randint(0, 1000),
                            verbose=False,
                        ).fit(data, lengths)

                        score = model.score(data)

                        if score > best_score:
                            best_score = score
                            best_model = model
                            best_model_type = mode
                            best_n_states = state

                    except:
                        print(traceback.format_exc())
                        pass

    except:
        print(traceback.format_exc())
        model = None
        pass

    return best_model

def hmmlearn_predict_hmm(model, data):

        try:

            if model is not None:

                predictions = model.predict(data)
                transmat = model.transmat_

            else:
                predictions = None

        except:
            print(traceback.format_exc())
            predictions = None
            pass

        return predictions

def correct_hmm_predictions(predictions, min_length=2, max_transitions=100):

    try:

        array = np.array(predictions)

        # Find the indices where adjacent elements differ
        change_points = np.where(array[:-1] != array[1:])[0] + 1
        change_points = np.insert(change_points, 0, 0)

        if type(min_length) == str:
            if min_length.isdigit():
                min_length = int(min_length)
            else:
                min_length = 0
        else:
            min_length = int(min_length)

        new_predictions = predictions.copy()

        for index in range(len(change_points)-1):

            start_index = change_points[index]
            end_index = change_points[index+1]

            state_length = end_index - start_index

            if state_length <= min_length:

                try:

                    previous_state = new_predictions[start_index-1]
                    next_state = new_predictions[end_index]

                    if previous_state == next_state:
                        new_predictions[int(start_index):int(end_index)] = int(previous_state)

                except:
                    pass

        array = np.array(new_predictions)

        # Find the indices where adjacent elements differ
        change_points = np.where(array[:-1] != array[1:])[0] + 1
        change_points = np.insert(change_points, 0, 0)

        n_transitions = len(change_points)-1

        if type(max_transitions) == str:
            if max_transitions.isdigit():
                max_transitions = int(max_transitions)
            else:
                max_transitions = n_transitions
        else:
            max_transitions = int(max_transitions)

        if n_transitions > max_transitions:
            new_predictions = np.zeros_like(predictions).tolist()

    except:
        print(traceback.format_exc())
        new_predictions = predictions
        pass

    return new_predictions