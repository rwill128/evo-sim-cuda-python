import numpy as np
import scipy.signal as signal


def create_template(x=800, y=800) -> np.ndarray:
    return np.random.random(size=(x, y))


def add_smoothing_to_template(l: np.ndarray):
    sl = signal.savgol_filter(x=l, window_length=21, polyorder=4, axis=0)
    sl = signal.savgol_filter(x=sl, window_length=21, polyorder=4, axis=-1)
    return sl


def generate_land_and_water_from_template(l2: np.ndarray, t: float) -> (np.ndarray, np.ndarray):
    lowered_template = l2.copy()
    threshold_array = np.full(np.shape(lowered_template), t)

    lowered_template = np.subtract(lowered_template, threshold_array)
    land = np.clip(lowered_template, 0.0, 1.0)
    water = np.clip(lowered_template, -1.0, 0.0)
    return land, water


def entire_surface(l: np.ndarray, w: np.ndarray) -> np.ndarray:
    zeros = np.zeros(w.shape)
    non_zero_locations_in_land = np.not_equal(l, zeros)
    non_zero_locations_in_water = np.not_equal(w, zeros)
    ef = np.empty(l.shape)
    np.copyto(ef, l, where=non_zero_locations_in_land)
    np.copyto(ef, w, where=non_zero_locations_in_water)
    return ef
