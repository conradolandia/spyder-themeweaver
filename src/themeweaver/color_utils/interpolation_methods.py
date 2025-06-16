"""
Pure mathematical interpolation methods.

This module contains various interpolation algorithms that can be used
for any numerical interpolation, including colors, animations, and other
mathematical applications.
"""

import math


def linear_interpolate(start, end, factor):
    """
    Linear interpolation between two values.

    Args:
        start: Starting value
        end: Ending value
        factor: Interpolation factor (0-1)

    Returns:
        Interpolated value
    """
    return start + (end - start) * factor


def circular_interpolate(start_angle, end_angle, factor):
    """
    Interpolate between two angles (in degrees) taking the shortest circular path.

    Args:
        start_angle: Starting angle in degrees
        end_angle: Ending angle in degrees
        factor: Interpolation factor (0-1)

    Returns:
        Interpolated angle in degrees
    """
    # Normalize angles to 0-360
    start_angle = start_angle % 360
    end_angle = end_angle % 360

    # Calculate the difference
    diff = end_angle - start_angle

    # Take the shortest path around the circle
    if diff > 180:
        diff -= 360
    elif diff < -180:
        diff += 360

    # Interpolate and normalize result
    result = (start_angle + diff * factor) % 360
    return result


def cubic_interpolate(start, end, factor):
    """
    Cubic (smooth) interpolation between two values using smoothstep function.

    Args:
        start: Starting value
        end: Ending value
        factor: Interpolation factor (0-1)

    Returns:
        Interpolated value with smooth acceleration/deceleration
    """
    # Using smoothstep function: 3t² - 2t³
    smooth_factor = factor * factor * (3 - 2 * factor)
    return start + (end - start) * smooth_factor


def exponential_interpolate(start, end, factor, exponent=2):
    """
    Exponential interpolation between two values.

    Args:
        start: Starting value
        end: Ending value
        factor: Interpolation factor (0-1)
        exponent: Exponential power (default: 2)

    Returns:
        Interpolated value with exponential curve
    """
    exp_factor = factor**exponent
    return start + (end - start) * exp_factor


def sine_interpolate(start, end, factor):
    """
    Sine-based interpolation between two values for smooth easing.

    Args:
        start: Starting value
        end: Ending value
        factor: Interpolation factor (0-1)

    Returns:
        Interpolated value with sine curve easing
    """
    sine_factor = (1 - math.cos(factor * math.pi)) / 2
    return start + (end - start) * sine_factor


def cosine_interpolate(start, end, factor):
    """
    Cosine-based interpolation between two values.

    Args:
        start: Starting value
        end: Ending value
        factor: Interpolation factor (0-1)

    Returns:
        Interpolated value with cosine curve
    """
    cosine_factor = (1 - math.cos(factor * math.pi)) / 2
    return start + (end - start) * cosine_factor


def hermite_interpolate(start, end, factor):
    """
    Hermite interpolation for smooth curves.

    Args:
        start: Starting value
        end: Ending value
        factor: Interpolation factor (0-1)

    Returns:
        Interpolated value using Hermite polynomial
    """
    # Hermite basis functions
    h1 = 2 * factor**3 - 3 * factor**2 + 1
    h2 = -2 * factor**3 + 3 * factor**2

    return h1 * start + h2 * end


def quintic_interpolate(start, end, factor):
    """
    Quintic (5th degree polynomial) interpolation for very smooth curves.

    Args:
        start: Starting value
        end: Ending value
        factor: Interpolation factor (0-1)

    Returns:
        Interpolated value with quintic smoothing
    """
    # Quintic smoothstep: 6t⁵ - 15t⁴ + 10t³
    smooth_factor = factor**3 * (factor * (factor * 6 - 15) + 10)
    return start + (end - start) * smooth_factor
