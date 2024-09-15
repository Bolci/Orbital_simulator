import orekit_jpype
orekit_jpype.initVM()
from orekit_jpype.pyhelpers import setup_orekit_curdir
setup_orekit_curdir('resources')
import unittest
import sys
import java.io.File as File
from org.orekit.data import DataProvidersManager, DirectoryCrawler
from org.orekit.utils import IERSConventions
from org.orekit.data import DataProvidersManager, ZipJarCrawler


orekit_data_path = "/home/bolci/Documents/Projekty/Lidas in Space/Orbital_simulator/orekit-data-master.zip"
data_manager = DataProvidersManager()
zip_crawler = ZipJarCrawler(orekit_data_path)
data_manager.addProvider(zip_crawler)



from org.orekit.bodies import OneAxisEllipsoid
from org.orekit.data import DataProvidersManager, ZipJarCrawler
from org.orekit.frames import FramesFactory
from org.orekit.orbits import KeplerianOrbit, OrbitType
from org.orekit.propagation.analytical.tle import TLE, TLEPropagator
from org.orekit.propagation import SpacecraftState
from org.orekit.time import AbsoluteDate, TimeScalesFactory
from org.orekit.utils import Constants

# Load the TLE
tle_line1 = '1 25544U 98067A   21025.51136670  .00002182  00000-0  43544-4 0  9991'
tle_line2 = '2 25544  51.6455 148.3428 0002197  52.3363  60.0711 15.48815328266001'
tle = TLE(tle_line1, tle_line2)

# Set up the TLE propagator
tle_propagator = TLEPropagator.selectExtrapolator(tle)

# Define the time at which we want to extract the state
utc = TimeScalesFactory.getUTC()
target_date = AbsoluteDate(2021, 2, 10, 12, 0, 0.0, utc)

# Get the spacecraft state at the target date
initial_state = tle_propagator.propagate(target_date)

# Extract position and velocity in meters and meters per second
pv_coordinates = initial_state.getPVCoordinates(FramesFactory.getGCRF())
position = pv_coordinates.getPosition()  # In meters
velocity = pv_coordinates.getVelocity()  # In meters per second

print(f"Initial Position (m): {position}")
print(f"Initial Velocity (m/s): {velocity}")

