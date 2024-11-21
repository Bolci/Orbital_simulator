from skyfield.timelib import Time
import numpy as np
from datetime import datetime, timedelta

class UtilsTime:

    @staticmethod
    def find_id_of_closest_time(buffer: list[Time], target_time:Time) -> int:
        target_jd = target_time.tt
        buffer_jd = np.array([time.tt for time in buffer])
        closest_idx = (np.abs(buffer_jd - target_jd)).argmin()
        return closest_idx

    @staticmethod
    def julian_date_to_iso8601(julian_date):
        return julian_date.utc_iso()
