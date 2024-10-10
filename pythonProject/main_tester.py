from org.orekit.bodies import OneAxisEllipsoid
from org.orekit.forces.gravity.potential import GravityFieldFactory
from org.orekit.forces.gravity import HolmesFeatherstoneAttractionModel
from org.orekit.forces.drag import DragForce
from org.orekit.forces.radiation import SolarRadiationPressure
from org.orekit.propagation.numerical import NumericalPropagator
from org.orekit.frames import FramesFactory
from org.orekit.time import AbsoluteDate
from org.orekit.orbits import KeplerianOrbit, OrbitType, PositionAngleType
from org.orekit.propagation.analytical.tle import TLE
from org.orekit.utils import Constants

# Define the initial TLE orbit
tle = TLE("TLE_LINE1", "TLE_LINE2")
initialOrbit = tle.getOrbit()

# Set up the frame, gravitational model, and atmosphere
earth = OneAxisEllipsoid(Constants.WGS84_EARTH_EQUATORIAL_RADIUS,
                         Constants.WGS84_EARTH_FLATTENING,
                         FramesFactory.getITRF())
gravityField = GravityFieldFactory.getNormalizedProvider(10, 10)
gravityModel = HolmesFeatherstoneAttractionModel(earth.getBodyFrame(), gravityField)

# Initialize the propagator
propagator = NumericalPropagator(gravityModel)

# Define drag model (atmospheric drag example)
#dragForce = DragForce(HarrisPriester(earth), 2.2)  # 2.2 is the drag coefficient
#propagator.addForceModel(dragForce)

# Set the orbit type
propagator.setOrbitType(OrbitType.KEPLERIAN)

# Propagate the orbit for a given time
finalDate = AbsoluteDate.now().shiftedBy(86400.0)  # 1 day later
pvCoordinates = propagator.getPVCoordinates(finalDate, FramesFactory.getICRF())

# Print the propagated position and velocity
print("Propagated position:", pvCoordinates.getPosition())
print("Propagated velocity:", pvCoordinates.getVelocity())
