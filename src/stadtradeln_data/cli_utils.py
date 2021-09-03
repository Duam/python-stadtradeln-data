import numpy as np
import pathlib
from stadtradeln_data.constants import default_cache_path
from stadtradeln_data.status import Status
from stadtradeln_data.dataset_downloader import DownloadResult, download_dataset
from stadtradeln_data.dataset_extractor import ExtractResult, extract_dataset
from stadtradeln_data.dataset_clipper import ClipResult, clip_dataset


def download(
        year: int,
        path: pathlib.Path = default_cache_path,
        overwrite: bool = False,
) -> DownloadResult:
    """
    :param year:
    :param path:
    :param overwrite:
    :returns:
    """
    print(f"Downloading {year} dataset to path \"{path}\"")
    retry = True
    verify_ca_certificate = True
    while retry:
        download_result = download_dataset(
            year,
            destination_path=path,
            verify_ca_certificate=verify_ca_certificate,
            overwrite=overwrite
        )
        if download_result.status == Status.UNKNOWN_DATASET:
            print("The dataset you requested does not exist, aborting.")
            return download_result
        elif download_result.status == Status.FILE_ALREADY_EXISTS:
            print(f"File already exists, continuing.")
            retry = False
        elif download_result.status == Status.FAILURE:
            print(f"Download failed, data in \"{download_result.filepath}\" seems corrupted.")
            return download_result
        elif download_result.status == Status.SSL_ERROR:
            print("WARNING: Your CA-certificates could not be verified by the downloader. "
                  "If you do not trust your network, it is advised that you download the "
                  "files from the original BmVI website: "
                  "https://www.mcloud.de/web/guest/suche/-/results/detail/ECF9DF02-37DC-4268-B017-A7C2CF302006 "
                  f"and manually move them to \"{path}\"")
            choice = input("Retry without certificate verification (Y/n)? ")
            verify_ca_certificate = False
            if choice != "Y" and choice != "y":
                print("Aborting.")
                return download_result
        elif download_result.status == Status.SUCCESS:
            retry = False
        else:
            print("Something unexpectedly went really wrong, sorry. "
                  "Pleas submit an issue with a short description of the steps "
                  "you made before encountering this error:")
            print("https://github.com/Duam/stadtradeln-data/issues/new")
            print("Aborting.")
            return download_result
    print(f"Dataset is located in \"{download_result.filepath}\".")
    return download_result


def extract(
        year: int,
        path: pathlib.Path = default_cache_path,
        overwrite: bool = False,
) -> ExtractResult:
    """
    :param year:
    :param path:
    :param overwrite:
    :returns:
    """
    print(f"Extracting {year} dataset in \"{path}\".")
    extract_result = extract_dataset(year, path, overwrite)
    if extract_result.status == Status.UNKNOWN_DATASET:
        print(f"The compressed dataset was not found in path \"{extract_result.filepath}\".")
        return extract_result
    elif extract_result.status == Status.FAILURE:
        print("Could not extract the dataset (unknown reason).")
        return extract_result
    elif extract_result.status == Status.FILE_ALREADY_EXISTS:
        print("Extracted file already exists, continuing.")
    print(f"Raw data is located in \"{extract_result.filepath}\".")
    return extract_result


def clip(
        year: int,
        path: pathlib.Path = default_cache_path,
        overwrite: bool = False,
        latitude_min: float = -np.inf,
        latitude_max: float = np.inf,
        longitude_min: float = -np.inf,
        longitude_max: float = np.inf,
) -> None:
    """
    :param year:
    :param path:
    :param overwrite:
    :param latitude_min:
    :param latitude_max:
    :param longitude_min:
    :param longitude_max:
    :returns:
    """
    raise NotImplementedError
