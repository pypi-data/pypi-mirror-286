from __future__ import annotations

import logging
from typing import Iterator

import geopandas as gpd
import pandas as pd
import xarray as xr
from datatree import DataTree
from spatialdata import SpatialData
from spatialdata.models import SpatialElement
from spatialdata.transformations import Identity, get_transformation, set_transformation
from xarray import DataArray

from ._constants import SopaKeys

log = logging.getLogger(__name__)


def get_boundaries(
    sdata: SpatialData, return_key: bool = False, warn: bool = False
) -> gpd.GeoDataFrame | tuple[str, gpd.GeoDataFrame] | None:
    """Gets the baysor boundaries or cellpose boundaries of a SpatialData object after running Sopa

    Args:
        sdata: A SpatialData object
        return_key: Whether to return the key of the shapes or not.
        warn: If `True`, prints a warning if no boundary is found. Else, raises an error.

    Returns:
        A `GeoDataFrame` containing the boundaries, or a tuple `(shapes_key, geo_df)`
    """
    VALID_BOUNDARIES = [
        SopaKeys.BAYSOR_BOUNDARIES,
        SopaKeys.COMSEG_BOUNDARIES,
        SopaKeys.CELLPOSE_BOUNDARIES,
    ]
    for shapes_key in VALID_BOUNDARIES:
        res = _try_get_boundaries(sdata, shapes_key, return_key)
        if res is not None:
            return res

    error_message = (
        "sdata object has no valid segmentation boundary. Consider running Sopa segmentation first."
    )

    if not warn:
        raise ValueError(error_message)

    log.warn(error_message)
    return (None, None) if return_key else None


def _try_get_boundaries(
    sdata: SpatialData, shapes_key: str, return_key: bool
) -> gpd.GeoDataFrame | None:
    """Try to get a cell boundaries for a given `shapes_key`"""
    if shapes_key in sdata.shapes:
        return (shapes_key, sdata[shapes_key]) if return_key else sdata[shapes_key]


def get_intrinsic_cs(
    sdata: SpatialData, element: SpatialElement | str, name: str | None = None
) -> str:
    """Gets the name of the intrinsic coordinate system of an element

    Args:
        sdata: A SpatialData object
        element: `SpatialElement`, or its key
        name: Name to provide to the intrinsic coordinate system if not existing. By default, uses the element id.

    Returns:
        Name of the intrinsic coordinate system
    """
    if name is None:
        name = f"_{element if isinstance(element, str) else id(element)}_intrinsic"

    if isinstance(element, str):
        element = sdata[element]

    for cs, transform in get_transformation(element, get_all=True).items():
        if isinstance(transform, Identity):
            return cs

    set_transformation(element, Identity(), name)
    return name


def to_intrinsic(
    sdata: SpatialData, element: SpatialElement | str, element_cs: SpatialElement | str
) -> SpatialElement:
    """Transforms a `SpatialElement` into the intrinsic coordinate system of another `SpatialElement`

    Args:
        sdata: A SpatialData object
        element: `SpatialElement` to transform, or its key
        element_cs: `SpatialElement` of the target coordinate system, or its key

    Returns:
        The `SpatialElement` after transformation in the target coordinate system
    """
    if isinstance(element, str):
        element = sdata[element]
    cs = get_intrinsic_cs(sdata, element_cs)
    return sdata.transform_element_to_coordinate_system(element, cs)


def get_key(sdata: SpatialData, attr: str, key: str | None = None):
    if key is not None:
        return key

    elements = getattr(sdata, attr)

    if not len(elements):
        return None

    assert (
        len(elements) == 1
    ), f"Trying to get an element key of `sdata.{attr}`, but it contains multiple values and no dict key was provided"

    return next(iter(elements.keys()))


def get_element(sdata: SpatialData, attr: str, key: str | None = None):
    key = get_key(sdata, attr, key)
    return sdata[key] if key is not None else None


def get_item(sdata: SpatialData, attr: str, key: str | None = None):
    key = get_key(sdata, attr, key)
    return key, sdata[key] if key is not None else None


def get_intensities(sdata: SpatialData) -> pd.DataFrame | None:
    """Gets the intensity dataframe of shape `n_obs x n_channels`"""
    assert SopaKeys.TABLE in sdata.tables, f"No '{SopaKeys.TABLE}' found in sdata.tables"

    adata = sdata.tables[SopaKeys.TABLE]

    if not adata.uns[SopaKeys.UNS_KEY][SopaKeys.UNS_HAS_INTENSITIES]:
        return None

    if adata.uns[SopaKeys.UNS_KEY][SopaKeys.UNS_HAS_TRANSCRIPTS]:
        return adata.obsm[SopaKeys.INTENSITIES_OBSM]

    return adata.to_df()


def iter_scales(image: DataTree) -> Iterator[xr.DataArray]:
    """Iterates through all the scales of a `DataTree`

    Args:
        image: a `DataTree`

    Yields:
        Each scale (as a `xr.DataArray`)
    """
    assert isinstance(
        image, DataTree
    ), f"Multiscale iteration is reserved for type DataTree. Found {type(image)}"

    for scale in image:
        yield next(iter(image[scale].values()))


def get_spatial_image(
    sdata: SpatialData, key: str | None = None, return_key: bool = False
) -> DataArray | tuple[str, DataArray]:
    """Gets a DataArray from a SpatialData object (if the image has multiple scale, the `scale0` is returned)

    Args:
        sdata: SpatialData object.
        key: Optional image key. If `None`, returns the only image (if only one), or raises an error.
        return_key: Whether to also return the key of the image.

    Returns:
        If `return_key` is False, only the image is returned, else a tuple `(image_key, image)`
    """
    key = get_key(sdata, "images", key)

    assert key is not None, "One image in `sdata.images` is required"

    image = sdata.images[key]
    if isinstance(image, DataTree):
        image = next(iter(image["scale0"].values()))

    if return_key:
        return key, image
    return image
