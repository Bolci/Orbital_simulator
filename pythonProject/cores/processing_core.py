import sys

import matplotlib.pyplot as plt
import numpy as np

from utils.utils_vector import Utils

sys.path.append('../')

from buffers.measurement_buffer import MeasurementBuffer
from numpy.typing import NDArray
from utils.utils_image import ImageUtils
from utils.utils_camera import UtilsCamera
from utils.utils_report import UtilsReport
from .core_abstract import CoreAbstract
#from data_processors.lamber_solver import LambertSolver
from poliastro.iod import izzo
from skyfield.timelib import Time
from exceptions.exceptions import SamplingException
from poliastro.bodies import Earth
from astropy import units as u

class ProcessingCore(CoreAbstract):
    def __init__(self, mu):
        super().__init__()
        self.mu = mu
        #self.lambert = LambertSolver(mu)

    @staticmethod
    def get_overlapped_image(image_data: list[NDArray]):
        overlapped_image = np.sum(image_data, axis=0)
        overlapped_image = np.clip(overlapped_image,0,255)
        return overlapped_image

    def image_all_times(self, image):
        pass

    @staticmethod
    def get_image_center_point(image) -> tuple[int, int]:
        return ImageUtils.get_center_of_image(image)

    def get_los_from_image(self, single_image_data, measurement_setup_report):
        x_center, y_center = self.get_image_center_point(single_image_data)

        camera_report = self.sattelite_active.sattelite_intruments['Camera'].get_camera_report()
        camera_intrinsics = [camera_report['camera_intrinsics']['fx'],
                             camera_report['camera_intrinsics']['fy'],
                             camera_report['camera_intrinsics']['cx'],
                             camera_report['camera_intrinsics']['cy']]


        los = UtilsCamera.pixel_to_los(pixel_coords=(x_center, y_center),
                                       camera_intrinsics=camera_intrinsics)

        return los


    @staticmethod
    def predict_position(los, distance, measurement_setup_report):
        position_in_global_cc, rotation_matrix, instrument_orientations = UtilsReport.parse_active_sattelite_report(measurement_setup_report)
        relative_position_to_sattelite = los*distance
        position_global = Utils.local_to_global_vector(relative_position_to_sattelite, rotation_matrix, position_in_global_cc)

        return position_global

    def process_position_by_lamber(self, positions, dts):

        v_s = []
        v_s2 = []

        for id_t in range(len(dts)):
            ps1 = positions[id_t] * u.km
            ps2 =  positions[id_t+1] * u.km
            dt = dts[id_t] * u.s
            v1, v2 = izzo.lambert(Earth.k, ps1, ps2, dt)
            v_s.append(v1)
            v_s2.append(v2)


    def process_data(self,
                     measurement_buffer: MeasurementBuffer):

        time_buf = 0
        predicted_positions_from_laser = []
        dts = []
        for id_t, time_sample in enumerate(measurement_buffer._time_buffer):
            utc_ts = int(time_sample.tt)
            seconds = (time_sample.tt - utc_ts) * 86400

            if not time_buf == 0:
                dts.append(seconds - time_buf)

            time_buf  = seconds
            measurement_setup_report = self.sattelite_active.get_report_by_time(time_sample)
            data_in_time = measurement_buffer.get_sample_by_time(time_sample)

            if not (measurement_setup_report['Timestamp'] == data_in_time['Timestamp']):
                raise SamplingException('Timestamp for report and data are not the same')

            los = self.get_los_from_image(data_in_time['Data']['Camera'], measurement_setup_report)
            distance = data_in_time['Data']['Laser_altimeter'][0][0]

            position_from_laser = self.predict_position(los, distance, measurement_setup_report)
            predicted_positions_from_laser.append(position_from_laser)

        self.process_position_by_lamber(predicted_positions_from_laser, dts)

        measured_data_all = measurement_buffer.get_reorganized_buffer()
        overlapped_image = self.get_overlapped_image(measured_data_all['Camera'])
        return {"Overlapped_image": overlapped_image}
