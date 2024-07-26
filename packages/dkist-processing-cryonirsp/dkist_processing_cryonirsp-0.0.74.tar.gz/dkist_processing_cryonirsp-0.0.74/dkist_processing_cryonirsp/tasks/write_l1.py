"""Cryonirsp write L1 task."""
from abc import ABC
from abc import abstractmethod
from typing import Callable
from typing import Literal

import astropy.units as u
import numpy as np
from astropy.io import fits
from dkist_processing_common.models.wavelength import WavelengthRange
from dkist_processing_common.tasks import WriteL1Frame
from dkist_service_configuration.logging import logger

from dkist_processing_cryonirsp.models.constants import CryonirspConstants

__all__ = ["CIWriteL1Frame", "SPWriteL1Frame"]


class CryonirspWriteL1Frame(WriteL1Frame, ABC):
    """
    Task class for writing out calibrated l1 CryoNIRSP frames.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs
    """

    @property
    def constants_model_class(self):
        """Get Cryonirsp pipeline constants."""
        return CryonirspConstants

    def add_dataset_headers(
        self, header: fits.Header, stokes: Literal["I", "Q", "U", "V"]
    ) -> fits.Header:
        """
        Add the Cryonirsp specific dataset headers to L1 FITS files.

        Parameters
        ----------
        header : fits.Header
            calibrated data header

        stokes :
            stokes parameter

        Returns
        -------
        fits.Header
            calibrated header with correctly written l1 headers
        """
        first_axis = 1
        next_axis = self._add_first_axis(header, axis_num=first_axis)
        next_axis = self._add_second_axis(header, axis_num=next_axis)
        multiple_measurements = self.constants.num_meas > 1
        if multiple_measurements:
            next_axis = self._add_measurement_axis(header, next_axis)
        next_axis = self._add_scan_step_axis(header, axis_num=next_axis)
        if self.constants.num_map_scans > 1:
            next_axis = self._add_map_scan_axis(header, axis_num=next_axis)
        if self.constants.correct_for_polarization:
            next_axis = self._add_stokes_axis(header, stokes=stokes, axis_num=next_axis)
        self._add_wavelength_headers(header)
        last_axis = next_axis - 1
        self._add_common_headers(header, num_axes=last_axis)
        self._flip_spectral_axis(header)

        return header

    @property
    @abstractmethod
    def _latitude_pixel_name(self) -> str:
        """Return the descriptive name for the longitudinal axis."""
        pass

    @property
    @abstractmethod
    def _add_first_axis(self) -> Callable:
        """Return the add method for the first axis."""
        pass

    @property
    @abstractmethod
    def _add_second_axis(self) -> Callable:
        """Return the add method for the second axis."""
        pass

    def _flip_spectral_axis(self, header: fits.Header):
        """Adjust header values corresponding to axis flip."""
        pass

    def _add_helioprojective_latitude_axis(self, header: fits.Header, axis_num: int) -> int:
        """Add header keys for the spatial helioprojective latitude axis."""
        header[f"DNAXIS{axis_num}"] = header[f"NAXIS{axis_num}"]
        header[f"DTYPE{axis_num}"] = "SPATIAL"
        header[f"DPNAME{axis_num}"] = self._latitude_pixel_name
        header[f"DWNAME{axis_num}"] = "helioprojective latitude"
        header[f"DUNIT{axis_num}"] = header[f"CUNIT{axis_num}"]
        next_axis = axis_num + 1
        return next_axis

    def _add_measurement_axis(self, header: fits.Header, axis_num: int) -> int:
        """Add header keys related to multiple measurements."""
        header[f"DNAXIS{axis_num}"] = self.constants.num_meas
        header[f"DTYPE{axis_num}"] = "TEMPORAL"
        header[f"DPNAME{axis_num}"] = "measurement number"
        header[f"DWNAME{axis_num}"] = "time"
        header[f"DUNIT{axis_num}"] = "s"
        # DINDEX and CNCMEAS are both one-based
        header[f"DINDEX{axis_num}"] = header["CNCMEAS"]
        next_axis = axis_num + 1
        return next_axis

    @abstractmethod
    def _add_scan_step_axis(self, header: fits.Header, axis_num: int) -> int:
        pass

    def _add_map_scan_axis(self, header: fits.Header, axis_num: int) -> int:
        """Add header keys for the temporal map scan axis."""
        header["CNNMAPS"] = self.constants.num_map_scans
        header[f"DNAXIS{axis_num}"] = self.constants.num_map_scans
        header[f"DTYPE{axis_num}"] = "TEMPORAL"
        header[f"DPNAME{axis_num}"] = "map scan number"
        header[f"DWNAME{axis_num}"] = "time"
        header[f"DUNIT{axis_num}"] = "s"
        # Temporal position in dataset
        # DINDEX and CNMAP are both one-based
        header[f"DINDEX{axis_num}"] = header["CNMAP"]
        next_axis = axis_num + 1
        return next_axis

    def _add_stokes_axis(
        self, header: fits.Header, stokes: Literal["I", "Q", "U", "V"], axis_num: int
    ) -> int:
        """Add header keys for the stokes polarization axis."""
        header[f"DNAXIS{axis_num}"] = 4  # I, Q, U, V
        header[f"DTYPE{axis_num}"] = "STOKES"
        header[f"DPNAME{axis_num}"] = "polarization state"
        header[f"DWNAME{axis_num}"] = "polarization state"
        header[f"DUNIT{axis_num}"] = ""
        # Stokes position in dataset - stokes axis goes from 1-4
        header[f"DINDEX{axis_num}"] = self.constants.stokes_params.index(stokes.upper()) + 1
        next_axis = axis_num + 1
        return next_axis

    def _add_wavelength_headers(self, header: fits.Header) -> None:
        """Add header keys related to the observing wavelength."""
        # The wavemin and wavemax assume that all frames in a dataset have identical wavelength axes
        header["WAVEUNIT"] = -9  # nanometers
        header["WAVEREF"] = "Air"
        wavelength_range = self.get_wavelength_range(header)
        header["WAVEMIN"] = wavelength_range.min.to(u.nm).value
        header["WAVEMAX"] = wavelength_range.max.to(u.nm).value

    @staticmethod
    def _add_common_headers(header: fits.Header, num_axes: int) -> None:
        """Add header keys that are common to both SP and CI."""
        header["DNAXIS"] = num_axes
        header["DAAXES"] = 2  # Spatial, spatial
        header["DEAXES"] = num_axes - 2  # Total - detector axes
        header["LEVEL"] = 1
        # Binning headers
        header["NBIN1"] = 1
        header["NBIN2"] = 1
        header["NBIN3"] = 1
        header["NBIN"] = header["NBIN1"] * header["NBIN2"] * header["NBIN3"]

    def calculate_date_end(self, header: fits.Header) -> str:
        """
        In CryoNIRSP, the instrument specific DATE-END keyword is calculated during science calibration.

        Check that it exists.

        Parameters
        ----------
        header
            The input fits header
        """
        try:
            return header["DATE-END"]
        except KeyError as e:
            raise KeyError(
                f"The 'DATE-END' keyword was not found. "
                f"Was supposed to be inserted during science calibration."
            ) from e

    def l1_filename(self, header: fits.Header, stokes: Literal["I", "Q", "U", "V"]):
        """
        Use a FITS header to derive its filename in the following format.

        instrument_arm_datetime_wavelength__stokes_datasetid_L1.fits.

        This is done by taking the base filename and changing the instrument name to include the arm.

        Example
        -------
        "CRYO-NIRSP_CI_2020_03_13T00_00_00_000_01080000_Q_DATID_L1.fits"

        Parameters
        ----------
        header
            The input fits header
        stokes
            The stokes parameter

        Returns
        -------
        The L1 filename including the arm ID
        """
        base_l1_filename = super().l1_filename(header, stokes)
        return base_l1_filename.replace(
            self.constants.instrument, f"{self.constants.instrument}_{self.constants.arm_id}"
        )


class CIWriteL1Frame(CryonirspWriteL1Frame):
    """
    Task class for writing out calibrated l1 CryoNIRSP frames.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs
    """

    @property
    def _latitude_pixel_name(self) -> str:
        """Return the descriptive name for the latitude axis."""
        return "detector x axis"

    @property
    def _add_first_axis(self) -> Callable:
        """Return the add method for the first axis."""
        return self._add_helioprojective_longitude_axis

    @property
    def _add_second_axis(self) -> Callable:
        """Return the add method for the second axis."""
        return self._add_helioprojective_latitude_axis

    @staticmethod
    def _add_helioprojective_longitude_axis(header: fits.Header, axis_num: int) -> int:
        """Add header keys for the spatial helioprojective longitude axis."""
        header[f"DNAXIS{axis_num}"] = header[f"NAXIS{axis_num}"]
        header[f"DTYPE{axis_num}"] = "SPATIAL"
        header[f"DWNAME{axis_num}"] = "helioprojective longitude"
        header[f"DUNIT{axis_num}"] = header[f"CUNIT{axis_num}"]
        header[f"DPNAME{axis_num}"] = "detector y axis"
        next_axis = axis_num + 1
        return next_axis

    def _add_scan_step_axis(self, header: fits.Header, axis_num: int) -> int:
        """Add header keys for the scan step axis."""
        header[f"DNAXIS{axis_num}"] = self.constants.num_scan_steps
        header[f"DTYPE{axis_num}"] = "TEMPORAL"
        header[f"DPNAME{axis_num}"] = "scan step number"
        header[f"DWNAME{axis_num}"] = "time"
        header[f"DUNIT{axis_num}"] = "s"
        # DINDEX and CNCURSCN are both one-based
        header[f"DINDEX{axis_num}"] = header["CNCURSCN"]
        next_axis = axis_num + 1
        return next_axis

    def _flip_spectral_axis(self, header: fits.Header):
        """Adjust header values corresponding to axis flip."""
        pass

    def get_wavelength_range(self, header: fits.Header) -> WavelengthRange:
        """
        Return the wavelength range of this frame.

        Range is the wavelengths at the edges of the filter full width half maximum.
        """
        filter_central_wavelength = header["CNCENWAV"] * u.nm
        filter_fwhm = header["CNFWHM"] * u.nm
        return WavelengthRange(
            min=filter_central_wavelength - (filter_fwhm / 2),
            max=filter_central_wavelength + (filter_fwhm / 2),
        )


class SPWriteL1Frame(CryonirspWriteL1Frame):
    """
    Task class for writing out calibrated l1 CryoNIRSP frames.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs
    """

    @property
    def _latitude_pixel_name(self) -> str:
        """Return the descriptive name for the latitudinal axis."""
        return "spatial along slit"

    @property
    def _add_first_axis(self) -> Callable:
        """Return the add method for the first axis."""
        return self._add_spectral_axis

    @property
    def _add_second_axis(self) -> Callable:
        """Return the add method for the first axis."""
        return self._add_helioprojective_latitude_axis

    @staticmethod
    def _add_spectral_axis(header: fits.Header, axis_num: int) -> int:
        """Add header keys for the spectral dispersion axis."""
        header[f"DNAXIS{axis_num}"] = header[f"NAXIS{axis_num}"]
        header[f"DTYPE{axis_num}"] = "SPECTRAL"
        header[f"DPNAME{axis_num}"] = "dispersion axis"
        header[f"DWNAME{axis_num}"] = "wavelength"
        header[f"DUNIT{axis_num}"] = header[f"CUNIT{axis_num}"]
        next_axis = axis_num + 1
        return next_axis

    def _flip_spectral_axis(self, header: fits.Header):
        """Adjust header values corresponding to axis flip."""
        # Fix the dispersion value to always be positive (Cryo gives it to us negative, which is wrong)
        header["CDELT1"] = np.abs(header["CDELT1"])
        # re-set the value of the reference pixel after the axis flip
        header["CRPIX1"] = header["NAXIS1"] - header["CRPIX1"]

    def _add_scan_step_axis(self, header: fits.Header, axis_num: int) -> int:
        """Add header keys for the spatial scan step axis."""
        header[f"DNAXIS{axis_num}"] = self.constants.num_scan_steps
        header[f"DTYPE{axis_num}"] = "SPATIAL"
        header[f"DPNAME{axis_num}"] = "scan step number"
        header[f"DWNAME{axis_num}"] = "helioprojective longitude"
        # NB: CUNIT axis number is hard coded here
        header[f"DUNIT{axis_num}"] = header[f"CUNIT3"]
        # DINDEX and CNCURSCN are both one-based
        header[f"DINDEX{axis_num}"] = header["CNCURSCN"]
        next_axis = axis_num + 1
        return next_axis

    def get_wavelength_range(self, header: fits.Header) -> WavelengthRange:
        """
        Return the wavelength range of this frame.

        Range is the wavelength values of the pixels at the ends of the wavelength axis.
        """
        axis_types = [
            self.constants.axis_1_type,
            self.constants.axis_2_type,
            self.constants.axis_3_type,
        ]
        wavelength_axis = axis_types.index("AWAV") + 1  # FITS axis numbering is 1-based, not 0
        wavelength_unit = header[f"CUNIT{wavelength_axis}"]

        minimum = header[f"CRVAL{wavelength_axis}"] - (
            header[f"CRPIX{wavelength_axis}"] * header[f"CDELT{wavelength_axis}"]
        )
        maximum = header[f"CRVAL{wavelength_axis}"] + (
            (header[f"NAXIS{wavelength_axis}"] - header[f"CRPIX{wavelength_axis}"])
            * header[f"CDELT{wavelength_axis}"]
        )
        return WavelengthRange(
            min=u.Quantity(minimum, unit=wavelength_unit),
            max=u.Quantity(maximum, unit=wavelength_unit),
        )
