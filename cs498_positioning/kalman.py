from pykalman import KalmanFilter
import numpy as np

kf = KalmanFilter(transition_matrices=np.array([[1.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                                                [0.0, 1.0, 0.0, 0.0, 1.0, 0.0],
                                                [0.0, 0.0, 1.0, 0.0, 0.0, 1.0],
                                                [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                                                [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                                                [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]),
                  observation_matrices=np.array([[1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                                 [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                                                 [0.0, 0.0, 1.0, 0.0, 0.0, 0.0]]),
                  transition_covariance=0.003 * np.eye(6, dtype=float))  # TODO: change this constant

t = 0

means = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
covariances = np.eye(6, dtype=float)


def kalman_filter(measurement):
    global t, means, covariances

    new_filtered_means, new_filtered_covariances = (kf.filter_update(means, covariances, measurement))
    means, covariances = new_filtered_means, new_filtered_covariances
    t = t + 1.0
    # print(means[:3]);
    return means[:3]
