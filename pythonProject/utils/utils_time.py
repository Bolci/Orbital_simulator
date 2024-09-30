from astropy.time import Time
import numpy as np

class UtilsTime:

    @staticmethod
    def find_closest_time(buffer: list[Time], target_time: Time):
        # Convert target time and buffer times to Julian date (JD)
        target_jd = target_time.tt.jd
        buffer_jd = np.array([time.tt.jd for time in buffer])

        # Find the index of the closest time
        closest_idx = (np.abs(buffer_jd - target_jd)).argmin()

        return closest_idx