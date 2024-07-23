"""Two sample benchmarks to compute runtime and memory usage.

For more information on writing benchmarks:
https://asv.readthedocs.io/en/stable/writing_benchmarks.html."""

from lco_etc.etc import (
    exposure_time_calc,
    moon_phase_to_numeric,
    radial_integrate_gauss,
    telescope_to_index,
)


class TimeComputation:
    """
    Benchmarks to measure the runtime of functions in the etc module.
    """

    def time_moon_phase_to_numeric(self):
        """
        Benchmark the moon_phase_to_numeric function for different moon phases.

        This benchmark measures the time taken to convert various moon phases
        ('new', 'half', 'full') to their numeric representations.
        """
        for phase in ["new", "half", "full"]:
            moon_phase_to_numeric(phase)

    def time_radial_integrate_gauss(self):
        """
        Benchmark the radial_integrate_gauss function for different radii.

        This benchmark measures the time taken to calculate the radial integral
        of a Gaussian function for different radius values (1.0, 2.0, 0.0).
        """
        for R in [1.0, 2.0, 0.0]:
            radial_integrate_gauss(R, 1.0)

    def time_telescope_to_index(self):
        """
        Benchmark the telescope_to_index function for different telescope names.

        This benchmark measures the time taken to convert various telescope names
        ('sbig', 'sinistro', 'qhy', 'spectral', 'muscat3') to their corresponding indices.
        """
        for telescope in ["sbig", "sinistro", "qhy", "spectral", "muscat3"]:
            telescope_to_index(telescope)

    def time_exposure_time_calc(self):
        """
        Benchmark the exposure_time_calc function for different input scenarios.

        This benchmark measures the time taken to calculate the exposure time,
        signal-to-noise ratio, and magnitude for various sets of inputs.
        """
        exposure_time_calc(10.0, 20, None, "sinistro", "V", "new", 1.2)
        exposure_time_calc(None, 15.0, 1.0, "sinistro", "R", "half", 1.2)
        exposure_time_calc(15, None, 1.0, "sbig", "U", "full", 3)
        exposure_time_calc(20, 15.0, None, "spectral", "r", "new", 1.5)
        exposure_time_calc(None, 15.0, 1.0, "qhy", "i", "new", 2.7)
        exposure_time_calc(5, None, 1.0, "muscat3", "g", "new", 1.2)
        exposure_time_calc(None, 15.0, 1000, "sinistro", "R", "half", 1.2)


class MemComputation:
    """
    Benchmarks to measure the memory usage of functions in the etc module.
    """

    def mem_moon_phase_to_numeric(self):
        """
        Benchmark the memory usage of the moon_phase_to_numeric function.

        This benchmark measures the memory usage when converting various moon
        phases ('new', 'half', 'full') to their numeric representations.
        """
        return [moon_phase_to_numeric(phase) for phase in ["new", "half", "full"]]

    def mem_radial_integrate_gauss(self):
        """
        Benchmark the memory usage of the radial_integrate_gauss function.

        This benchmark measures the memory usage when calculating the radial
        integral of a Gaussian function for different radius values (1.0, 2.0, 0.0).
        """
        return [radial_integrate_gauss(R, 1.0) for R in [1.0, 2.0, 0.0]]

    def mem_telescope_to_index(self):
        """
        Benchmark the memory usage of the telescope_to_index function.

        This benchmark measures the memory usage when converting various
        telescope names ('sbig', 'sinistro', 'qhy', 'spectral', 'muscat3')
        to their corresponding indices.
        """
        return [
            telescope_to_index(telescope) for telescope in ["sbig", "sinistro", "qhy", "spectral", "muscat3"]
        ]

    def mem_exposure_time_calc(self):
        """
        Benchmark the memory usage of the exposure_time_calc function.

        This benchmark measures the memory usage when calculating the exposure
        time, signal-to-noise ratio, and magnitude for various sets of inputs.
        """
        return [
            exposure_time_calc(10.0, 20, None, "sinistro", "V", "new", 1.2),
            exposure_time_calc(None, 15.0, 1.0, "sinistro", "R", "half", 1.2),
            exposure_time_calc(15, None, 1.0, "sbig", "U", "full", 3),
            exposure_time_calc(20, 15.0, None, "spectral", "r", "new", 1.5),
            exposure_time_calc(None, 15.0, 1.0, "qhy", "i", "new", 2.7),
            exposure_time_calc(5, None, 1.0, "muscat3", "g", "new", 1.2),
            exposure_time_calc(None, 15.0, 1000, "sinistro", "R", "half", 1.2),
        ]
