import math
import warnings

# Define constants and data tables
Filt = ["U", "B", "V", "R", "I", "u", "g", "r", "i", "Z", "Y"]
Ext = [0.54, 0.23, 0.12, 0.09, 0.04, 0.59, 0.14, 0.08, 0.06, 0.04, 0.03]
ApixelTable = [0.57, 0.389, 0.73, 0.304, 0.27]
gain_table = [1.6, 2.3, 0.7, 7.7, 1.9]
read_noise_table = [14, 8, 3, 11, 14.5]
dark_current_table = [0.02, 0.002, 0.04, 0.002, 0.005]
saturation_limit_table = [65000 * 1.6, 10000, 47000, 71000, 462000]
phot_zeropoint_table = [
    [18.0, 20.3, 20.7, 21.2, 20.3, 16.11, 21.4, 21.5, 20.75, 19.4, 17.8],
    [21.4, 23.5, 23.5, 23.8, 23.2, 22.45, 24.3, 23.8, 23.5, 22.2, 20.3],
    [0.0, 21.4, 21.4, 21.2, 20.3, 17.5, 21.8, 21.2, 20.1, 18.4, 0.0],
    [21.3, 24.4, 24.6, 24.9, 24.1, 21.4, 25.4, 25.25, 24.75, 23.75, 21.6],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 25.4, 25.2, 24.5, 24.3, 0.0],
]
Msky = [
    [23.0, 22.5, 21.6, 20.6, 19.8, 23.5, 22.0, 21.1, 20.6, 20.2, 19.4],
    [20.0, 20.5, 20.3, 20.0, 18.8, 21.0, 20.3, 20.2, 19.7, 19.2, 18.0],
    [17.0, 17.8, 17.5, 17.4, 17.0, 18.0, 17.6, 17.5, 17.5, 16.8, 16.5],
]
Carea = [1200.0, 6260.0, 660, 27000.0, 27000.0]
Fcent = [0.350, 0.437, 0.549, 0.653, 0.789, 0.354, 0.476, 0.623, 0.760, 0.853, 0.975]
Fband = [0.050, 0.107, 0.083, 0.137, 0.128, 0.057, 0.140, 0.135, 0.148, 0.113, 0.118]


def moon_phase_to_numeric(moon_phase: str) -> int:
    """
    Convert moon phase from string to numeric value.

    Parameters
    ----------
    moon_phase : str
        Phase of the moon (new, half, full)

    Returns
    -------
    int
        Numeric value of the moon phase
    """

    moon_phase_dict = {"new": 0, "half": 1, "full": 2}

    return moon_phase_dict[moon_phase]


def radial_integrate_gauss(R: float, sigma: float) -> float:
    """
    Calculates the radial integral of a Gaussian function.

    Parameters
    ----------
    R : float
        Radius
    sigma : float
        Standard deviation of the Gaussian
        that is based on the seeing

    Returns
    -------
    float
        Radial integral of the Gaussian function
    """

    return 1 - math.exp(-1.0 * (R * R) / (2 * sigma * sigma))


def telescope_to_index(telescope: str) -> int:
    """
    Convert telescope name to index.

    Parameters
    ----------
    telescope : str
        Name of the telescope

    Returns
    -------
    int
        Index of the telescope
    """

    telescope_dict = {"sbig": 0, "sinistro": 1, "qhy": 2, "spectral": 3, "muscat3": 4}

    return telescope_dict[telescope]


def exposure_time_calc(
    snr: float,
    magnitude: float,
    etime: float,
    telescope: str,
    filter: str,
    moon_phase: str,
    airmass: float,
    seeing: float = 2,
) -> dict:
    """
    Exposure Time calculator for the Las Cumbres Observatory (LCO) network.

    Given two of the three values (S/N, magnitude, and exposure time), this
    function calculates the third value.

    This function is based on the LCO exposure time calculator available at https://exposure-time-calculator.lco.global/

    The javascript code for the original calculator was extracted from the webpage and translated to Python.

    Make sure that the filter is available on the selected instrument!

    Information about each telescope can be found at https://lco.global/observatory/instruments/

    UBVRI in Vega magnitudes; ugriz in AB magnitudes

    Parameters
    ----------
    snr : float
        Signal-to-noise ratio
    magnitude : float
        Magnitude
    etime : float
        Exposure time
    telescope : str
        Telescope name (sbig, sinistro, qhy, spectral, muscat3)
    filter : str
        Filter (U, B, V, R, I, u, g, r, i, Z, Y)
    moon_phase : int
        Moon phase
    airmass : float
        Airmass
    seeing : float, optional
        Seeing in arcseconds (default is 2)

    Returns
    -------
    dict
        A dictionary containing the calculated values:
        - snr : float
            Signal-to-noise ratio
        - magnitude : float
            Magnitude
        - exposure_time : float
            Exposure time
        - saturated : bool
            True if the source is saturated
        - mag_system : str
            Magnitude system (Vega or AB)
    """

    # Check to see that telescope name is available
    if telescope not in ["sbig", "sinistro", "qhy", "spectral", "muscat3"]:
        raise ValueError(
            f"{telescope} is not a valid telescope. Please select one of the following telescopes: \
              sbig, sinistro, qhy, spectral, muscat3"
        )

    # Check to see that at least two out [snr, magnitude, etime] are provided
    if sum([snr is not None, magnitude is not None, etime is not None]) < 2:
        raise ValueError("At least two of the following values must be provided: snr, magnitude, etime")

    # If all three values are provided, raise an error
    if sum([snr is not None, magnitude is not None, etime is not None]) == 3:
        raise ValueError("Only two of the following values should be provided: snr, magnitude, etime")

    if filter not in Filt:
        raise ValueError(
            f"{filter} is not a valid filter. Please select one of the following filters: {Filt}"
        )

    # Convert telescope name to index
    telescope = telescope_to_index(telescope)

    # Convert moon phase to numeric value
    moon_phase = moon_phase_to_numeric(moon_phase)

    # Various initializations and parameter setups
    airmass_correction = (airmass - 1.0) * Ext[Filt.index(filter)]
    zeropoint = phot_zeropoint_table[telescope][Filt.index(filter)]
    adiam = 3.0
    Nas = math.pi / 4 * adiam * adiam
    apixel = ApixelTable[telescope]
    Npix = Nas / (apixel * apixel)
    skymag = Msky[moon_phase][Filt.index(filter)]
    # gain = gain_table[telescope]
    ron = read_noise_table[telescope]
    dark = dark_current_table[telescope]
    saturationLimit = saturation_limit_table[telescope]

    # Determine which value to calculate (e, m, or S/N)
    result = None
    if snr is not None and magnitude is not None and etime is None:
        exposure_time = 1.0
        result = "e"
    elif snr is not None and magnitude is None and etime is not None:
        magt = 30.0
        result = "m"
    elif snr is None and magnitude is not None and etime is not None:
        s_nt = 1.0
        result = "s"

    endloop = 0

    while endloop < 1:
        mag_at_airmass = (
            magnitude + airmass_correction if magnitude is not None else magt + airmass_correction
        )
        Nobj = math.pow(10.0, -0.4 * (mag_at_airmass - zeropoint))
        Nbkgd = math.pow(10.0, -0.4 * (skymag - zeropoint))
        # NbDN = Nbkgd * apixel * apixel
        NeObj = Nobj * (etime if etime is not None else exposure_time)
        NeBkgd = Nbkgd * Nas * (etime if etime is not None else exposure_time)
        NeDark = Npix * dark * (etime if etime is not None else exposure_time)
        NeRon = Npix * ron * ron
        s_nt = NeObj / math.sqrt(NeObj + NeBkgd + NeDark + NeRon)

        gauss_sigma = seeing / 2.354

        PkDN = NeObj * radial_integrate_gauss(apixel, gauss_sigma)

        # Check to see if source is saturated
        if PkDN > saturationLimit:
            warnings.warn("Saturation may occur. Consider reducing the exposure or defocusing the telescope.")

            saturated = True

        else:
            saturated = False

        if result == "e":
            if s_nt < snr:
                exposure_time += 1
            else:
                endloop = 1
        elif result == "m":
            if s_nt < snr:
                magt -= 0.1
            else:
                endloop = 1
        elif result == "s":
            snr = s_nt
            endloop = 1

    # Rounding and returning results
    output = {
        "snr": round(10.0 * s_nt) / 10.0,
        "magnitude": round(10.0 * magnitude) / 10.0 if magnitude is not None else round(10.0 * magt) / 10.0,
        "exposure_time": exposure_time if result == "e" else etime,
        "saturated": saturated,
        "mag_system": "Vega" if Filt.index(filter) < 5 else "AB",
    }
    return output
