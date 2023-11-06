import numpy as np


def zero_crossings(signal: list[int]):
    """
    Returns the number of zero crossings in a signal.

    A zero crossing is defined as a point where the sign of the signal changes.
    If a signal touches zero but doesn't change sign, it is not a zero crossing.

    Example:
        [2, 1, 0, -1] -> 1 zero crossing
        [2, 1, 0, 1] -> no zero crossings

    Args:
        signal: A list of integers representing the signal.

    Returns:
        The number of zero crossings in the signal.
    """
    # Remove zeros to avoid detecting them as zero crossings
    signal = np.array(signal)
    signal = signal[signal != 0]

    # Create an array where True indicates a positive number
    signs = np.signbit(signal)

    # Create an array where True indicates a sign difference
    #  and count the times it happens
    return np.diff(signs).nonzero()[0].size
