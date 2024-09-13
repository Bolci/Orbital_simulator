import numpy as np
import matplotlib.pyplot as plt
from skyfield.api import load

from tle_worker import TLEWorker
from objects import Sphere
from sattellites import SatteliteActive, SatteliteWithDimension
from instruments import Camera, LaserAltimeter
from utils import Utils


if __name__ == "__main__":

    # define constants
    mu = 398600.4418  # Gravitational parameter for Earth (km^3/s^2)
    earth_radius = 6378.1363  # Earth's radius in km

    # Artificial TLE of sattelite on Sun-sychnronus orbit
    altitude = 750  # Satellite altitude in km
    inclination = np.radians(98.39)  # Inclination in radians
    raan = np.radians(52)  # RAAN in radians

    # Artificial TLE of dummy sattelite on Sun-sychnronus orbit
    altitude2 = 750  # Satellite altitude in km
    inclination2 = np.radians(98.1)  # Inclination in radians
    raan2 = np.radians(52)  # RAAN in radians
    dimensions_of_satt_2 = 0.050

    # Camera parameters
    sensor_resolution = (4112, 2176)
    fov_deg = (2.37, 1.23)

    # get_sattelites_TLE

    tle_worker = TLEWorker()

    tle_measurement_sat = tle_worker.generate_tle(r_earth=earth_radius,
                                                  altitude=altitude,
                                                  inclination=inclination,
                                                  raan=raan)

    tle_measurement_sat_2 = tle_worker.generate_tle(r_earth=earth_radius,
                                                    altitude=altitude2,
                                                    inclination=inclination2,
                                                    raan=raan2)

    # Load timescale
    ts = load.timescale()
    t0 = ts.now()
    minutes = np.linspace(0, 90, 500)  # Simulate over 90 minutes (approx one orbit)
    times = t0 + minutes / (24 * 60)  # Convert minutes to fraction of a day

    # get planes
    earth = Sphere.get_planet(earth_radius)

    # get sattelites
    measured_sattelite = SatteliteWithDimension('Dummy_sattelite', dimensions_of_satt_2)
    measured_sattelite.load_sattelite(tle_measurement_sat_2, ts)

    measurement_sattelite = SatteliteActive('Measurement_sattelite')
    measurement_sattelite.load_sattelite(tle_measurement_sat, ts)

    # generate instruments
    camera_orientation = [-30.623567051375606, -17.353989865522664, 0]  # yaw, pitch, roll

    camera = Camera(sensor_resolution=sensor_resolution,
                    fov_deg=fov_deg)
    laser_altimeter = LaserAltimeter()

    camera.assign_sattelite(measurement_sattelite)
    laser_altimeter.assign_sattelite(measurement_sattelite)

    camera.set_rotation(np.array(camera_orientation))

    measurement_sattelite.add_intruments(camera)
    measurement_sattelite.add_intruments(laser_altimeter)

    x_vals = []
    y_vals = []
    z_vals = []

    x_vals2 = []
    y_vals2 = []
    z_vals2 = []

    counter = 0

    for id_t, t in enumerate(times):
        sattelite_measurement_possition = measurement_sattelite.at(t)
        sattelite_dummy_possition = measured_sattelite.at(t)

        # yaw, pitch, roll = compute_camera_angles_with_roll(sattelite_measurement_possition, sattelite_dummy_possition)

        measured_objects = [measured_sattelite]
        measured_data = measurement_sattelite.perform_measurements(measured_objects)

        x_vals.append(sattelite_measurement_possition[0])
        y_vals.append(sattelite_measurement_possition[1])
        z_vals.append(sattelite_measurement_possition[2])

        x_vals2.append(sattelite_dummy_possition[0])
        y_vals2.append(sattelite_dummy_possition[1])
        z_vals2.append(sattelite_dummy_possition[2])

        if counter >= 10:
            break

        counter += 1

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(x_vals, y_vals, z_vals, label="Satellite with intruments")
    ax.plot(x_vals2, y_vals2, z_vals2, '*', label="Dummy sattelite")
    # ax.plot_surface(*earth.get_planet(), color='b', alpha=0.5)
    ax.set_xlabel('X (km)')
    ax.set_ylabel('Y (km)')
    ax.set_zlabel('Z (km)')
    ax.set_title("3D Orbit of Satellite")

    for id_x in range(len(x_vals)):
        if id_x % 10 == 0:
            ax.plot([x_vals[id_x], x_vals2[id_x]], [y_vals[id_x], y_vals2[id_x]], [z_vals[id_x], z_vals2[id_x]])

    vec_len = 10

    for id_x in range(len(x_vals)):

        if id_x % 10 == 0:
            vec_end = Utils.yaw_pitch_roll_to_vector(*camera_orientation, vec_len)
            ax.quiver(x_vals[id_x], y_vals[id_x], z_vals[id_x], vec_end[0], vec_end[1], vec_end[2], length=vec_len,
                      color='r')

        if id_x % 10 == 0:
            translated_point = [x_vals2[id_x] - x_vals[id_x], y_vals2[id_x] - y_vals[id_x],
                                z_vals2[id_x] - z_vals[id_x]]
            rotated_point = Utils.compute_rotation_matrix_in_3D(*camera_orientation) @ translated_point

            ax.quiver(x_vals[id_x], y_vals[id_x], z_vals[id_x], *rotated_point, length=vec_len, color='b')

    plt.legend()
    plt.show()

