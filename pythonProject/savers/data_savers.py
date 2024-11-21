import os
import matplotlib.pyplot as plt
import cv2
import numpy as np
import json


class DataSaver:
    def __init__(self, saving_folder_path: str) -> None:
        self.saving_folder = saving_folder_path
        self.folder_template = "Simulation_{}"
        self.full_path = ''
        self.create_path(saving_folder_path)
        self.current_it_path = ''

    @staticmethod
    def save_txt(path: str, data):
        """
        Saves data to a text file in JSON format.

        Args:
            path (str): The path to the text file.
            data (dict): The data to save.
        """
        with open(path, 'w') as fp:
            json.dump(data, fp)


    def create_path(self, path: str):
        if not os.path.exists(path) or os.listdir(path) == []:
            indexs = 0
        else:
            all_folders = os.listdir(path)
            sorted_f = sorted(all_folders, key=lambda x: int(x.split('_')[1]))[::-1]
            indexs = int(sorted_f[0].split('_')[1]) + 1
        folder_name = self.folder_template.format(indexs)
        path = os.path.join(path, folder_name)
        os.makedirs(path)
        self.full_path = path

    def create_iteration_folder(self, it_id):
        path = os.path.join(self.full_path, f'it_{it_id}')
        os.makedirs(path)
        self.current_it_path = path

    @staticmethod
    def extract_data_from_buffer_by_key(raw_data_buffer, key: str):
        data, time_stamps = raw_data_buffer.get_buffers()

        data_buffer = []
        time_stamp_buffer = []
        for data_sample, time_stamp in zip(data, time_stamps):
            single_data_sample_by_type = data_sample[key]

            data_buffer.append(single_data_sample_by_type)
            time_stamp_buffer.append(time_stamp)

        return data_buffer, time_stamp_buffer


    def save_laser_measurement(self, raw_data_buffer):
        extracted_images, time_stamps = self.extract_data_from_buffer_by_key(raw_data_buffer, 'Laser_altimeter')

        data_buffer = {}
        for id_laser, (laser_val, time_stamp) in enumerate(zip(extracted_images, time_stamps)):

            while isinstance(laser_val, list):
                laser_val = laser_val[0]

            data_buffer[id_laser] = {'Laser_distance': laser_val, 'TimeStamp': time_stamp.tt}

        saving_path = os.path.join(self.current_it_path, 'laser_measurement.txt')

        self.save_txt(saving_path, data_buffer)

    def save_images(self, raw_data_buffer):
        extracted_images, time_stamps = self.extract_data_from_buffer_by_key(raw_data_buffer, 'Camera')

        for id_photo, (img, time_stamp) in enumerate(zip(extracted_images, time_stamps)):

            file_name = f'photo_{id_photo}_timestamp={time_stamp}.png'
            file_path = os.path.join(self.current_it_path, file_name)
            cv2.imwrite(file_path, img)

    def save_raw_data(self, raw_data_buffer, id_it: int) -> None:
        self.create_iteration_folder(id_it)
        self.save_images(raw_data_buffer)
        self.save_laser_measurement(raw_data_buffer)

    def save_data(self, raw_data_buffer, processed_data_buffer, id_it):
        pass


