import numpy as np
import scipy.signal as signal


def create_land() -> np.ndarray:
    return np.random.random(size=(800, 800))


def add_smoothing_to_land(l: np.ndarray):
    sl = signal.savgol_filter(x=l, window_length=21, polyorder=4, axis=0)
    sl = signal.savgol_filter(x=sl, window_length=21, polyorder=4, axis=-1)
    return sl


def lower_all_land_below_threshold(l2: np.ndarray, t: float) -> np.ndarray:
    lowered_land = l2.copy()

    for item in np.nditer(lowered_land, op_flags=['readwrite']):
        if item < t:
            item[...] = 0

    return lowered_land
