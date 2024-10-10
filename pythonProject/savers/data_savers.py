import os
import matplotlib.pyplot as plt
import cv2
import numpy as np


class DataSaver:
    def __init__(self, saving_folder_path: str) -> None:
        self.saving_folder = saving_folder_path
        self.folder_template = "Simulation_{}"
        self.full_path = ''
        self.create_path(saving_folder_path)
        self.current_it_path = ''


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

    def save_images(self, raw_data_buffer):
        data, time_stamps = raw_data_buffer.get_buffers()
        for id_photo, (data_sample, time_stamp) in enumerate(zip(data, time_stamps)):
            img = data_sample['Camera']

            file_name = f'photo_{id_photo}_timestamp={time_stamp}.png'
            file_path = os.path.join(self.current_it_path, file_name)
            cv2.imwrite(file_path, img)


    def save_data(self, raw_data_buffer, processed_data_buffer, id_it):
        self.create_iteration_folder(id_it)
        self.save_images(raw_data_buffer)

