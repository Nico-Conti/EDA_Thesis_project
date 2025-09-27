import numpy as np
import matplotlib.pyplot as plt
import neurokit2 as nk
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.model_selection import train_test_split, LeaveOneGroupOut
from sklearn.metrics import accuracy_score, precision_score, f1_score, confusion_matrix
from skimage.util.shape import view_as_windows
import seaborn as sns


# Initialize lists to store extracted features and corresponding labels
extracted_features = []
label = []
label.extend([0] * (32 * 60 * 3))
label.extend([1] * (32 * 60 * 4))
label = np.array(label)
label_windows = view_as_windows(label, 32*60, int(32*0.25))

groups = []
person = 1

# Define a list of filenames
file_names = ['finger_person_1.txt', 'finger_person_2_L.txt', 'finger_person_3_P.txt', 'finger_person_4_E.txt', 'finger_person_5_T.txt']

for file_name in file_names:
    data = np.fromfile(file_name, dtype="int32").reshape(-1, 2)
    column1 = data[:,0]
    column1 = column1[:7*32*60]

    sampling_rate = 32  # Samples per second

    bioz_conductance_signal = np.array([(1 / ((sample * 1) / ((2 ** 19) * 10 * (110 * (10**-9))))) for sample in column1])
    bioz_conductance_signal= (bioz_conductance_signal- np.mean(bioz_conductance_signal)) / np.std(bioz_conductance_signal)

    bsignals, binfo = nk.eda_process(bioz_conductance_signal, sampling_rate, method="neurokit", method_phasic="highpass", amplitude_min=0.2)

    eda_phasic_array = np.array(bsignals.EDA_Phasic).reshape(-1, 1)
    eda_tonic_array = np.array(bsignals.EDA_Tonic).reshape(-1, 1)
    eda_peak_array = np.array(bsignals.SCR_Peaks).reshape(-1, 1)
    eda_rise_array = np.array(bsignals.SCR_RiseTime).reshape(-1, 1)
    phasic_windows = view_as_windows(eda_phasic_array, (60*32,1), int(0.25*32))[:,0,:,:]
    tonic_windows = view_as_windows(eda_tonic_array, (60*32,1), int(0.25*32))[:,0,:,:]
    peak_windows = view_as_windows(eda_peak_array, (60*32,1), int(0.25*32))[:,0,:,:]
    rise_windows = view_as_windows(eda_rise_array, (60*32,1), int(0.25*32))[:,0,:,:]

    # # print(phasic_windows.shape)

    mean_tonic_per_window = np.mean(tonic_windows, axis=(1))
    mean_phasic_per_window = np.mean(phasic_windows, axis=(1))
    max_tonic_per_window = np.max(tonic_windows, axis=(1))
    number_peak_per_window = np.sum(peak_windows, axis=(1))
    std_rise_per_window = np.array([np.std(window[window != 0]) if np.any(window != 0) else 0 for window in rise_windows])
    std_rise_per_window = std_rise_per_window.reshape(-1, 1)
    print(mean_phasic_per_window.shape)
    # print(mean_phasic_per_window)
    # # print(std_rise_per_window.shape)
    # # print(std_rise_per_window)


    window_labels_not_all_zero = np.all(label_windows != 0, axis=1)
    # # print(window_labels_not_all_zero.shape)

    window_labels_assigned = np.where(window_labels_not_all_zero, 1, 0)

    window_features = np.column_stack((mean_tonic_per_window, mean_phasic_per_window, max_tonic_per_window, number_peak_per_window, std_rise_per_window))
    window_labels_assigned = window_labels_assigned.flatten()

    # Append features and labels to the list
    extracted_features.append((window_features, window_labels_assigned))

    groups.append(np.full(mean_tonic_per_window.shape[0], person))
    print(len(groups[0]))
    print(groups)
    person += 1
    
# print(extracted_features)

# Combine features and labels for all files
all_features = np.vstack([features for features, labels in extracted_features])
all_labels = np.concatenate([labels for features, labels in extracted_features])
all_groups = np.hstack(groups)
# print(all_features.shape)
# print(all_labels.shape)

logo = LeaveOneGroupOut()

# Initialize lists to store evaluation metrics
accuracy_scores = []
precision_scores = []
f1_scores = []

for train_indices, test_indices in logo.split(all_features, all_labels, groups=all_groups):
    # Split the data into training and testing sets
    X_train, X_test = all_features[train_indices], all_features[test_indices]
    y_train, y_test = all_labels[train_indices], all_labels[test_indices]

    # Train the classifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
    clf.fit(X_train, y_train)

    # Predict on the test set
    y_pred = clf.predict(X_test)

    # Calculate and store evaluation metrics
    accuracy_scores.append(accuracy_score(y_test, y_pred))
    precision_scores.append(precision_score(y_test, y_pred))
    f1_scores.append(f1_score(y_test, y_pred))

print("Accuracy:", accuracy_scores)
print("Precision:", precision_scores)
print("F1 Score:", f1_scores)

cm = confusion_matrix(y_test, y_pred)

sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.show()