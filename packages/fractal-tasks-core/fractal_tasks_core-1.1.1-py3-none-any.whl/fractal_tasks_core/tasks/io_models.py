from typing import Literal
from typing import Optional

from pydantic.v1 import BaseModel
from pydantic.v1 import Field
from pydantic.v1 import validator

from fractal_tasks_core.channels import ChannelInputModel
from fractal_tasks_core.channels import OmeroChannel


class InitArgsRegistration(BaseModel):
    """
    Registration init args.

    Passed from `image_based_registration_hcs_init` to
    `calculate_registration_image_based`.

    Attributes:
        reference_zarr_url: zarr_url for the reference image
    """

    reference_zarr_url: str


class InitArgsRegistrationConsensus(BaseModel):
    """
    Registration consensus init args.

    Provides the list of zarr_urls for all acquisitions for a given well

    Attributes:
        zarr_url_list: List of zarr_urls for all the OME-Zarr images in the
            well.
    """

    zarr_url_list: list[str]


class InitArgsCellVoyager(BaseModel):
    """
    Arguments to be passed from cellvoyager converter init to compute

    Attributes:
        image_dir: Directory where the raw images are found
        plate_prefix: part of the image filename needed for finding the
            right subset of image files
        well_ID: part of the image filename needed for finding the
            right subset of image files
        image_extension: part of the image filename needed for finding the
            right subset of image files
        image_glob_patterns: Additional glob patterns to filter the available
            images with
        acquisition: Acquisition metadata needed for multiplexing
    """

    image_dir: str
    plate_prefix: str
    well_ID: str
    image_extension: str
    image_glob_patterns: Optional[list[str]]
    acquisition: Optional[int]


class InitArgsIllumination(BaseModel):
    """
    Dummy model description.

    Attributes:
        raw_path: dummy attribute description.
        subsets: dummy attribute description.
    """

    raw_path: str
    subsets: dict[Literal["C_index"], int] = Field(default_factory=dict)


class InitArgsMIP(BaseModel):
    """
    Init Args for MIP task.

    Attributes:
        origin_url: Path to the zarr_url with the 3D data
    """

    origin_url: str


class MultiplexingAcquisition(BaseModel):
    """
    Input class for Multiplexing Cellvoyager converter

    Attributes:
        image_dir: Path to the folder that contains the Cellvoyager image
            files for that acquisition and the MeasurementData &
            MeasurementDetail metadata files.
        allowed_channels: A list of `OmeroChannel` objects, where each channel
            must include the `wavelength_id` attribute and where the
            `wavelength_id` values must be unique across the list.
    """

    image_dir: str
    allowed_channels: list[OmeroChannel]


class NapariWorkflowsOutput(BaseModel):
    """
    A value of the `output_specs` argument in `napari_workflows_wrapper`.

    Attributes:
        type: Output type (either `label` or `dataframe`).
        label_name: Label name (for label outputs, it is used as the name of
            the label; for dataframe outputs, it is used to fill the
            `region["path"]` field).
        table_name: Table name (for dataframe outputs only).
    """

    type: Literal["label", "dataframe"]
    label_name: str
    table_name: Optional[str] = None

    @validator("table_name", always=True)
    def table_name_only_for_dataframe_type(cls, v, values):
        """
        Check that table_name is set only for dataframe outputs.
        """
        _type = values.get("type")
        if (_type == "dataframe" and (not v)) or (_type != "dataframe" and v):
            raise ValueError(
                f"Output item has type={_type} but table_name={v}."
            )
        return v


class NapariWorkflowsInput(BaseModel):
    """
    A value of the `input_specs` argument in `napari_workflows_wrapper`.

    Attributes:
        type: Input type (either `image` or `label`).
        label_name: Label name (for label inputs only).
        channel: `ChannelInputModel` object (for image inputs only).
    """

    type: Literal["image", "label"]
    label_name: Optional[str]
    channel: Optional[ChannelInputModel]

    @validator("label_name", always=True)
    def label_name_is_present(cls, v, values):
        """
        Check that label inputs have `label_name` set.
        """
        _type = values.get("type")
        if _type == "label" and not v:
            raise ValueError(
                f"Input item has type={_type} but label_name={v}."
            )
        return v

    @validator("channel", always=True)
    def channel_is_present(cls, v, values):
        """
        Check that image inputs have `channel` set.
        """
        _type = values.get("type")
        if _type == "image" and not v:
            raise ValueError(f"Input item has type={_type} but channel={v}.")
        return v
