import logging
from pathlib import Path, PosixPath
from typing import Union, List

import pandas as pd
# TODO Multithread processing with Dask #15
# import dask.dataframe as dd
# from dask.dataframe import DataFrame
# from dask.distributed import Client, LocalCluster
from pandas import DataFrame

from istatcelldata.config import logger, console_handler, SHARED_DATA
from istatcelldata.generic import check_encoding

logger.addHandler(console_handler)
# TODO Multithread processing with Dask #15
# cluster = LocalCluster(n_workers=8, threads_per_worker=N_CORES, processes=True)
# client = Client(cluster)


def read_csv(
        csv_path: Union[Path, PosixPath],
        separator: str = ';'
) -> DataFrame:
    """Lettura di un csv e conversione in DataFrame.

    Args:
        csv_path: Union[Path, PosixPath]
        separator: str

    Returns:
        DataFrame
    """
    # Get encoding
    logging.info('Get encoding')
    data_encoding = check_encoding(data=csv_path)

    # Read data
    logging.info('Read data')
    # TODO Multithread processing with Dask #15
    # ddf = dd.read_csv(csv_path, encoding=data_encoding, sep=separator, sample=100000, assume_missing=True)
    ddf = pd.read_csv(csv_path, encoding=data_encoding, sep=separator)
    ddf.columns = ddf.columns.str.lower()
    ddf = ddf.replace(['nan', 'NaN'], 0)

    return ddf


def merge_data(
        csv_path: Union[Path, PosixPath],
        year: int,
        separator: str = ';',
        output_path: Union[Path, PosixPath] = None,
        region_list: List = []
) -> Union[Path, PosixPath, DataFrame]:
    """Unione di tutti i dati censuari per l'anno selezionato
    in un unico DataFrame.

    Args:
        csv_path: Union[Path, PosixPath]
        year: int
        separator: str
        output_path: Union[Path, PosixPath]
        region_list: List

    Returns:
        Union[Path, PosixPath, DataFrame]
    """
    # List all csv paths
    files_path = list(csv_path.rglob("*.csv"))

    data_list = []
    for file in files_path:
        if not file.stem == f'tracciato_{year}_sezioni':
            data = read_csv(csv_path=file, separator=separator)
            data_list.append(data)

    # Make Dask DataFrame
    logging.info('Make DataFrame')
    # TODO Multithread processing with Dask #15
    # logging.info('Make Dask DataFrame')
    # ddf = dd.concat(data_list)
    ddf = pd.concat(data_list)
    ddf = ddf.sort_values(f'sez{year}')

    if len(region_list) > 0:
        ddf = ddf[ddf["codreg"].isin(region_list)]

    if output_path is None:
        return ddf

    else:
        output_data = output_path.joinpath(f'data{year}.csv')
        logging.info(f'Save data to {output_data}')
        # TODO Multithread processing with Dask #15
        # df = ddf.compute()
        df = ddf
        df.to_csv(output_data, sep=separator, index=False)


def list_shared_columns() -> list:
    """Generazione della lista di tutti i dati condivisi.

    Returns:
        list
    """
    column_list = []
    for key, value in SHARED_DATA.items():
        column_code = value['codice'].lower()
        column_list.append(column_code)

    return column_list
