import numpy as np
import matplotlib.pyplot as plt
from numba.cuda.printimpl import print_item
from skyfield.api import load

from tle_worker import TLEWorker
from objects import Sphere, Sun
from sattelites.sattelite_active import SatteliteActive
from sattelites.sattelite_object import SatteliteObject
from instruments.camera import Camera
from instruments.laser_altimeter import LaserAltimeter


if __name__ == "__main__":

    # define constants
    mu = 398600.4418  # Gravitational parameter for Earth (km^3/s^2)
    earth_radius = 6378.1363  # Earth's radius in km

    # Artificial TLE of sattelite on Sun-sychnronus orbit
    altitude = 750  # Satellite altitude in km
    inclination = np.radians(98.39)  # Inclination in radians
    raan = np.radians(52)  # RAAN in radians

    # Artificial TLE of dummy sattelite on Sun-sychnronus orbit
    altitude2 = 850  # Satellite altitude in km
    inclination2 = np.radians(93.1)  # Inclination in radians
    raan2 = np.radians(52)  # RAAN in radians
    dimensions_of_satt_2 = 0.050 #in meters

    # Camera parameters
    sensor_resolution = (2176, 4112)
    fov_deg = (1.23,2.37)
    fps = 1
    conversion = 1

    #laser altimeter parameters
    laser_divergence = 2e-5 #rad
    laser_pulse_lenght = 0.001

    # get_sattelites_TLE

    tle_worker = TLEWorker()

    tle_measurement_sat = tle_worker.generate_tle(altitude=altitude,
                                                  inclination=inclination,
                                                  raan=raan)

    tle_measurement_sat_2 = tle_worker.generate_tle(altitude=altitude2,
                                                    inclination=inclination2,
                                                    raan=raan2)

    # Load timescale
    max_simulation_time = 10 #in minutes
    ts = load.timescale()
    t0 = ts.now()
    minutes = np.linspace(0, max_simulation_time, max_simulation_time*fps*conversion)
    times = t0 + minutes / (24 * 60)  # Convert minutes to fraction of a day

    # get objetcs
    earth = Sphere.get_planet(earth_radius)
    Sun = Sun()

    # get sattelites
    measured_sattelite = SatteliteObject('Dummy_sattelite', dimensions_of_satt_2)
    measured_sattelite.load_sattelite(tle_measurement_sat_2, ts)

    measurement_sattelite = SatteliteActive('Measurement_sattelite')
    measurement_sattelite.load_sattelite(tle_measurement_sat, ts)


    camera = Camera(sensor_resolution=sensor_resolution,
                    fov_deg=fov_deg)
    laser_altimeter = LaserAltimeter(beam_divergence = laser_divergence)
    laser_altimeter.pulse_length = laser_pulse_lenght

    camera.assign_sattelite(measurement_sattelite)
    laser_altimeter.assign_sattelite(measurement_sattelite)

    measurement_sattelite.add_intruments('Camera', camera)
    measurement_sattelite.add_intruments('Laser_atimeter', laser_altimeter)

    measurement_sattelite.set_intrument_orientation_relative_to_sattelite('Camera', np.array([0.,0.0, 1.0]))
    measurement_sattelite.set_intrument_orientation_relative_to_sattelite('Laser_atimeter', np.array([0.0, 0.0, 1.0]))


    counter = 0
    is_oriented_flag = 0

    image_all = np.zeros(sensor_resolution, dtype=np.uint8)



    for id_t, t in enumerate(times):
        sattelite_dummy_possition = measured_sattelite.at(t)
        sattelite_measurement_possition = measurement_sattelite.at(t)

        measured_objects = [measured_sattelite]

        if is_oriented_flag < 2:
            measurement_sattelite.orient_instrument_on_satellite('Camera', sattelite_dummy_possition)
        is_oriented_flag += 1

        measured_data = measurement_sattelite.perform_measurements(measured_objects)

        image_all += measured_data['Camera']


        if counter >= 200:
            break

        counter += 1

    plt.figure()
    plt.imshow(image_all)

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(*measured_sattelite.get_orbit(), label="Satellite with intruments")
    ax.plot(*measurement_sattelite.get_orbit(), 'magenta', label="Dummy sattelite")
    ax.plot_surface(*earth, color='b', alpha=0.1)
    ax.set_xlabel('X (km)')
    ax.set_ylabel('Y (km)')
    ax.set_zlabel('Z (km)')
    ax.set_title("3D Orbit of Satellite")

    '''
    for id_x in range(len(x_vals)):
        if id_x % 10 == 0:
            ax.plot([x_vals[id_x], x_vals2[id_x]], [y_vals[id_x], y_vals2[id_x]], [z_vals[id_x], z_vals2[id_x]])
    '''


    for id_x in range(len(times)):
        if id_x % 10 == 0:

            sattelite_possition = measurement_sattelite.sattelite_orbit.get_sample_by_id(id_x)
            sattelite_arientation_buffer = measurement_sattelite.orientation_buffer.get_sample_by_id(id_x)
            print(sattelite_arientation_buffer)

            ax.quiver(*sattelite_possition, *(sattelite_arientation_buffer[0]), length=1000,
                      color='r', normalize=True)

            ax.quiver(*sattelite_possition, *(sattelite_arientation_buffer[1]), length=1000,
                      color='b', normalize=True)

            ax.quiver(*sattelite_possition, *(sattelite_arientation_buffer[2]), length=1000,
                      color='g', normalize=True)


    plt.legend()
    plt.show()



