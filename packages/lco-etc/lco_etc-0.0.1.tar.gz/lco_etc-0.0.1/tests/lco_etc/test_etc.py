import math

import pytest
from lco_etc.etc import (
    exposure_time_calc,
    moon_phase_to_numeric,
    radial_integrate_gauss,
    telescope_to_index,
)


def test_moon_phase_to_numeric():
    """
    Test the moon_phase_to_numeric function.

    This test verifies that the moon_phase_to_numeric function returns the correct
    numeric values for valid moon phases ('new', 'half', 'full') and raises a KeyError
    for an invalid moon phase.
    """
    assert moon_phase_to_numeric("new") == 0
    assert moon_phase_to_numeric("half") == 1
    assert moon_phase_to_numeric("full") == 2
    with pytest.raises(KeyError):
        moon_phase_to_numeric("unknown")


def test_radial_integrate_gauss():
    """
    Test the radial_integrate_gauss function.

    This test verifies that the radial_integrate_gauss function returns the correct
    values for given inputs of radius (R) and standard deviation (sigma).
    """
    assert math.isclose(radial_integrate_gauss(1.0, 1.0), 0.3934693402873666)
    assert math.isclose(radial_integrate_gauss(2.0, 1.0), 0.8646647167633873)
    assert math.isclose(radial_integrate_gauss(0.0, 1.0), 0.0)


def test_telescope_to_index():
    """
    Test the telescope_to_index function.

    This test verifies that the telescope_to_index function returns the correct
    index for valid telescope names and raises a KeyError for an invalid telescope name.
    """
    assert telescope_to_index("sbig") == 0
    assert telescope_to_index("sinistro") == 1
    assert telescope_to_index("qhy") == 2
    assert telescope_to_index("spectral") == 3
    assert telescope_to_index("muscat3") == 4
    with pytest.raises(KeyError):
        telescope_to_index("unknown")


def test_exposure_time_calc():
    """
    Test the exposure_time_calc function.

    This test verifies that the exposure_time_calc function correctly calculates
    the signal-to-noise ratio (snr), magnitude (magnitude), exposure time (exposure_time), saturation status,
    and magnitude system for given inputs. It also checks that the function raises
    a ValueError for invalid input combinations and invalid filters.
    """
    # Provided test cases with expected outputs
    result = exposure_time_calc(10.0, 20, None, "sinistro", "V", "new", 1.2)
    assert result == {
        "snr": 10.2,
        "magnitude": 20.0,
        "exposure_time": 29.0,
        "saturated": False,
        "mag_system": "Vega",
    }

    result = exposure_time_calc(None, 15.0, 1.0, "sinistro", "R", "half", 1.2)
    assert result == {
        "snr": 40.5,
        "magnitude": 15.0,
        "exposure_time": 1.0,
        "saturated": False,
        "mag_system": "Vega",
    }

    result = exposure_time_calc(15, None, 1.0, "sbig", "U", "full", 3)
    assert result == {
        "snr": 15.2,
        "magnitude": 9.3,
        "exposure_time": 1.0,
        "saturated": False,
        "mag_system": "Vega",
    }

    result = exposure_time_calc(20, 15.0, None, "spectral", "r", "new", 1.5)
    assert result == {
        "snr": 82.3,
        "magnitude": 15.0,
        "exposure_time": 1.0,
        "saturated": False,
        "mag_system": "AB",
    }

    result = exposure_time_calc(None, 15.0, 1.0, "qhy", "i", "new", 2.7)
    assert result == {
        "snr": 6.7,
        "magnitude": 15.0,
        "exposure_time": 1.0,
        "saturated": False,
        "mag_system": "AB",
    }

    result = exposure_time_calc(5, None, 1.0, "muscat3", "g", "new", 1.2)
    assert result == {
        "snr": 5.1,
        "magnitude": 18.2,
        "exposure_time": 1.0,
        "saturated": False,
        "mag_system": "AB",
    }

    result = exposure_time_calc(None, 15.0, 1000, "sinistro", "R", "half", 1.2)
    assert result == {
        "snr": 1742.4,
        "magnitude": 15.0,
        "exposure_time": 1000,
        "saturated": True,
        "mag_system": "Vega",
    }

    # Additional checks for invalid inputs
    with pytest.raises(ValueError):
        exposure_time_calc(None, None, None, "sinistro", "V", "new", 1.2)

    with pytest.raises(ValueError):
        exposure_time_calc(10.0, 15.0, None, "sinistro", "invalid_filter", "new", 1.2)

    with pytest.raises(ValueError):
        exposure_time_calc(10.0, 15.0, 5.0, "sinistro", "V", "new", 1.2)


if __name__ == "__main__":
    pytest.main()
