import numpy as np

# Constants
speed_of_light = 3e8  # m/s


# Function to simulate laser altimeter with Gaussian beam profile and pulse effects
def laser_altimeter_gaussian(target_distance, target_radius, beam_diameter, pulse_length, object_size, noise_level):
    # Beam radius at target distance (half of the footprint diameter)
    beam_radius = beam_diameter / 2

    # Calculate distance resolution from pulse length
    distance_resolution = (speed_of_light * pulse_length) / 2

    # Simulate the object at various positions within the beam footprint
    object_positions = np.linspace(-beam_radius, beam_radius, 100)  # 100 positions across the footprint
    return_signals = []

    for position in object_positions:
        # Gaussian intensity based on object's position in the beam
        signal_strength = np.exp(-2 * (position ** 2) / (beam_radius ** 2))

        # If the object is within the beam radius, calculate the return signal
        if abs(position) <= beam_radius:
            # Simulate the effect of the target's size relative to the footprint
            object_coverage = object_size / (2 * beam_radius)  # Fraction of footprint covered by the object
            signal_strength *= object_coverage  # Adjust signal based on coverage

            time_of_flight = (2 * target_distance) / speed_of_light  # Time taken for laser to return
            noise = np.random.normal(0, noise_level)  # Add noise to simulate real-world conditions

            # Adjust time-of-flight based on pulse length and resolution
            if time_of_flight <= distance_resolution:
                return_signals.append((signal_strength + noise, time_of_flight))
            else:
                return_signals.append((0, None))  # No return if resolution limit exceeded
        else:
            # Missed target or weak scattered signal
            return_signals.append((0, None))  # No signal or weak signal

    return return_signals


# Parameters for the simulation
target_distance = 1000 * 1e3  # 1000 km in meters
beam_diameter = 30  # 30 meters footprint diameter
pulse_length = 10e-9  # 10 nanoseconds pulse length
object_size = 0.5  # 50 cm object
noise_level = 0.05  # simulate some noise

# Simulate and print results
signals = laser_altimeter_gaussian(target_distance, "",beam_diameter, pulse_length, object_size, noise_level)

# Analyze the results
for signal in signals:
    print(f"Signal strength: {signal[0]}, Time of flight: {signal[1]}")
