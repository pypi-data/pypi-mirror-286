"""
High-level interface for data access using Table Access Protocol (TAP)
"""


import os
import secrets
import shutil
import tempfile
import time
from io import BytesIO
from pathlib import Path
from typing import Callable, Dict, List, Literal, Sequence, Union
from urllib.parse import quote, urlencode

import numpy as np
import pandas as pd
import requests
# from astromodule.io import batch_download_file, download_file, write_table
# from astromodule.table import concat_tables
# from astromodule.table import guess_coords_columns
from astropy import units as u
from astropy.table import Table
from bs4 import BeautifulSoup

from pylegs.config import configs
from pylegs.io import (PathOrFile, TableLike, _create_parents, _prepare_path,
                       batch_download_file, concat_tables, download_file,
                       parallel_function_executor, read_table, write_table)
from pylegs.utils import guess_coords_columns

__all__ = [
  'ls_crossmatch', 'sync_query', 'async_query', 'batch_sync_query', 
  'batch_async_query'
]


def ls_crossmatch(
  table: TableLike | PathOrFile, 
  columns: Sequence[str], 
  radius: float | u.Quantity,
  save_path: str | Path,
  ra_col: str = None,
  dec_col: str = None,
  workers: int = 3,
):
  query_template = """
  SELECT TOP 1 {columns}, 
    POWER(ra - ({ra}), 2) * {cos_dec} + POWER(dec - ({dec}), 2) AS ls_separation
  FROM ls_dr10.tractor
  WHERE 
    ra BETWEEN {ra_min} AND {ra_max} 
    AND dec BETWEEN {dec_min} AND {dec_max}
  ORDER BY ls_separation ASC
  """.strip()
  df = read_table(table)
  ra_col, dec_col = guess_coords_columns(df, ra_col, dec_col)
  queries = []
  
  if isinstance(radius, u.Quantity):
    radius = radius.to(u.deg).value
  else:
    radius = (radius * u.arcsec).to(u.deg).value
    
  for i, row in df.iterrows():
    ra = row[ra_col]
    dec = row[dec_col]
    query = query_template.format(
      columns=','.join([str(c) for c in columns]), 
      ra_min=ra-radius,
      ra_max=ra+radius,
      dec_min=dec-radius,
      dec_max=dec+radius,
      ra=ra,
      dec=dec,
      cos_dec=np.cos(np.deg2rad(dec)),
    )
    queries.append(query)
  batch_sync_query(
    queries=queries, 
    save_paths=save_path, 
    concat=True, 
    workers=workers
  )


def sync_query(
  query: str, 
  save_path: PathOrFile = None,
  overwrite: bool = True,
  http_client: requests.Session = configs.HTTP_CLIENT,
  dtype: Literal['bytes', 'pandas', 'astropy'] = 'bytes'
) -> bytes | pd.DataFrame | Table:
  params = {
    'request': 'doQuery',
    'version': 1.0,
    'lang': 'ADQL',
    'phase': 'run',
    'format': 'csv',
    'query': query
  }
  save_path = _prepare_path(save_path)
  _create_parents(save_path)
  
  # req_url = configs.TAP_SYNC_BASE_URL + '?' + urlencode(params)
  
  table_bytes = download_file(
    url=configs.TAP_SYNC_BASE_URL,#req_url, 
    save_path=save_path, 
    overwrite=overwrite,
    query=params,
    replace=True, 
    http_client=http_client,
  )
  
  if dtype == 'bytes':
    return table_bytes
  if dtype in ('pandas', 'astropy'):
    return read_table(BytesIO(table_bytes), fmt='csv', dtype=dtype)


def async_query(
  query: str, 
  save_path: PathOrFile = None,
  overwrite: bool = True,
  http_client: requests.Session = configs.HTTP_CLIENT,
  delay: int = 5,
  dtype: Literal['bytes', 'pandas', 'astropy'] = 'bytes'
) -> bytes | pd.DataFrame | Table:
  params = {
    'request': 'doQuery',
    'version': 1.0,
    'lang': 'ADQL',
    'phase': 'run',
    'format': 'csv',
    'query': query
  }
  save_path = _prepare_path(save_path)
  _create_parents(save_path)
  
  resp = http_client.post(
    url=configs.TAP_ASYNC_BASE_URL,
    data=params,
  )
  soup = BeautifulSoup(resp.text, 'xml')
  
  job_id = soup.find('uws:jobId').text
  job_phase = soup.find('uws:phase').text
  table_bytes = None
  
  while job_phase == 'PENDING':
    time.sleep(delay)
    resp = http_client.get(configs.TAP_ASYNC_BASE_URL + f'/{job_id}')
    soup = BeautifulSoup(resp.text, 'xml')
    job_phase = soup.find('uws:phase').text
  
  if job_phase == 'COMPLETED':
    table_url = soup.find('#result').attrs['xlink:href']
    table_bytes = download_file(
      url=table_url, 
      save_path=save_path, 
      overwrite=overwrite, 
      http_client=http_client
    )
  
  if dtype == 'bytes':
    return table_bytes
  if dtype in ('pandas', 'astropy'):
    return read_table(BytesIO(table_bytes), fmt='csv', dtype=dtype)
  
  
def _batch_query(
  func: Callable,
  queries: Sequence[str],
  save_paths: Sequence[str | Path],
  func_args: Dict[str, None],
  workers: int = 3,
  concat: bool = False,
):
  save_paths_aux = save_paths
  if concat:
    tmp_folder = Path(tempfile.gettempdir()) / f'pylegs_tap_{secrets.token_hex(4)}'
    tmp_folder.mkdir(parents=True)
    save_paths_aux = [tmp_folder / f'{i}.csv' for i in range(len(queries))]
    
  params = [
    {
      'query': _query,
      'save_path': _save_path,
      **func_args,
    }
    for _query, _save_path in zip(queries, save_paths_aux)
  ]
  
  try:
    parallel_function_executor(
      func,
      params=params,
      workers=workers,
      unit='query',
    )

    if concat:
      combined_df = concat_tables(tmp_folder.glob('*.csv'), comment='#')
      write_table(combined_df, save_paths)
  except Exception as e:
    if concat:
      shutil.rmtree(tmp_folder)
    raise e


def batch_sync_query(
  queries: str, 
  save_paths: PathOrFile = None,
  overwrite: bool = True,
  concat: bool = False,
  workers: int = 3,
  http_client: requests.Session = configs.HTTP_CLIENT,
) -> bytes | pd.DataFrame | Table:
  args = {
    'overwrite': overwrite,
    'http_client': http_client,
  }
  _batch_query(
    func=sync_query, 
    queries=queries, 
    save_paths=save_paths, 
    func_args=args, 
    workers=workers, 
    concat=concat
  )
  
  
def batch_async_query(
  queries: str, 
  save_paths: PathOrFile = None,
  overwrite: bool = True,
  concat: bool = False,
  workers: int = 3,
  http_client: requests.Session = configs.HTTP_CLIENT,
  delay: int = 5,
) -> bytes | pd.DataFrame | Table:
  args = {
    'overwrite': overwrite,
    'http_client': http_client,
    'delay': delay,
  }
  _batch_query(
    func=async_query, 
    queries=queries, 
    save_paths=save_paths, 
    func_args=args, 
    workers=workers, 
    concat=concat
  )




if __name__ == '__main__':
  sync_query(
    'select top 10 psfdepth_g, psfdepth_r from ls_dr9.tractor where ra between 230.2939-0.0013 and 230.2939+0.0013 and dec between 29.7714-0.0013 and 29.7714+0.0013',
    url='https://datalab.noirlab.edu/tap/sync'
  )
  sync_query('select top 10 psfdepth_g, psfdepth_r from ls_dr9.tractor where ra between 230.2939-0.0013 and 230.2939+0.0013 and dec between 29.7714-0.0013 and 29.7714+0.0013')