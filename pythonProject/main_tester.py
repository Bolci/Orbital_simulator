from astropy.time import Time
import numpy as np


def find_closest_time(buffer, target_time):
    print(target_time)
    """
    Find the index of the closest Time object in the buffer.

    Parameters:
    buffer (list): List of Time objects.
    target_time (Time): Target Time object.

    Returns:
    int: Index of the closest Time object in the buffer.
    """
    # Convert target time and buffer times to Julian date (JD)
    target_jd = target_time.tt.jd
    print(target_jd)
    buffer_jd = np.array([time.tt.jd for time in buffer])

    # Find the index of the closest time
    closest_idx = (np.abs(buffer_jd - target_jd)).argmin()

    return closest_idx


# Example usage
buffer = [
    Time(2460584.018346552, format='jd', scale='tt'),
    Time(2460584.019077546, format='jd', scale='tt'),
    Time(2460584.01980854, format='jd', scale='tt'),
    Time(2460584.0205395343, format='jd', scale='tt'),
    Time(2460584.0212705284, format='jd', scale='tt'),
    Time(2460584.0220015226, format='jd', scale='tt'),
    Time(2460584.0227325168, format='jd', scale='tt')
]

target_time = Time(2460584.0205395345, format='jd', scale='tt')
index = find_closest_time(buffer, target_time)
print(f"Index of closest time: {index}")
