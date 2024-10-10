import numpy as np
from typing import Optional, Any


class UtilsReport:

    @staticmethod
    def parse_active_sattelite_report(report: dict):
        position_in_global_cc = report['Sattelite_position']
        position_in_global_cc = np.asarray([position_in_global_cc['x_val'],
                                           position_in_global_cc['y_val'],
                                           position_in_global_cc['z_val']])

        rotation_matrix = report['Satellite_orientation']
        rotation_matrix = np.column_stack((rotation_matrix['x_val'],
                                          rotation_matrix['y_val'],
                                          rotation_matrix['z_val']))

        instrument_orientations = report['Instruments_orientation']

        return position_in_global_cc, rotation_matrix, instrument_orientations
