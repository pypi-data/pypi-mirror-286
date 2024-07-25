from pathlib import Path
import shutil
from copy import copy, deepcopy
import pydicom.dataset
import pydicom.datadict
from ... import base_cache_dir

cache_dir = base_cache_dir / "dummy" / "dicom"
dicom_pkg_dir = Path(__file__).parent


def default_dicom_dir(file_loc: str):
    """Gets relative path location of module from base DICOM directory

    Parameters
    ----------
    file_loc : str
        File path to module were the

    Returns
    -------
    Path
        Relative path to module
    """
    return (
        cache_dir
        / Path(file_loc).relative_to(dicom_pkg_dir)
    ).with_suffix("")


def generate_dicom(
    cache_path: Path,
    num_vols: int,
    constant_hdr: dict,
    collated_data: dict,
    varying_hdr: dict,
):
    """Generates a dummy DICOM dataset for a test fixture

    Parameters
    ----------
    cache_path : Path
        Path to directory to save the DICOM files relative to the base cache dir
    num_vols : int
        Number of volumes in the set
    constant_hdr : dict[str, Any]
        constant header values
    collated_data : dict[str, int]
        data array lengths
    varying_hdr : dict[str, list], optional
        varying header values across a multi-volume set

    Returns
    -------
    Dicom
        Dicom dataset
    """

    cache_path = Path(cache_path)
    # Check for non-empty cache directory, and return it if present
    if cache_path.exists() and len(
        [p for p in cache_path.iterdir() if not p.name.startswith(".")]
    ):
        return cache_path

    cache_path.mkdir(parents=True, exist_ok=True)

    try:
        for i in range(num_vols):
            i = str(i)
            vol_json = copy(constant_hdr)
            if varying_hdr is not None:
                vol_json.update({k: v[i] for k, v in varying_hdr.items() if i in v})
            # Reconstitute large binary fields with dummy data filled with
            # \3 bytes
            for key, val in collated_data.items():
                if i in val:
                    vol_json[key] = {
                        "vr": val[i]["vr"],
                        "InlineBinary": "X" * val[i]["BinaryLength"],
                    }
            ds = pydicom.dataset.Dataset.from_json(vol_json)
            ds.is_implicit_VR = True
            ds.is_little_endian = True

            ds.save_as(cache_path / f"{i}.dcm", write_like_original=False)
    except Exception:
        shutil.rmtree(cache_path)  # Remove directory from cache on error
        raise
    else:
        return cache_path


def evolve_header(dicom_header, **kwargs):
    """Evolves a DICOM header with newly update values

    Parameters
    ----------
    dicom_header : dict[str, any]
        DICOM header extracted from a dataset
    **kwargs
        keyword arguments containing values to update in the header
    """
    hdr = deepcopy(dicom_header)
    for key, val in kwargs.items():
        tag_decimal = pydicom.datadict.tag_for_keyword(key)
        hex_tag = format(tag_decimal, '08x').upper()
        elem = hdr[hex_tag]["Value"]
        assert isinstance(elem, list) and len(elem) == 1
        nested_elem = elem[0]
        if isinstance(nested_elem, dict) and list(nested_elem.keys()) == ["Alphabetic"]:
            nested_elem["Alphabetic"] = val
        else:
            elem[0] = val
    return hdr
