"""
High-level interface to Legacy Survey data
"""


from io import BytesIO
from pathlib import Path
from typing import List, Literal, Sequence, Tuple, Union

import numpy as np
import pandas as pd
import requests
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.units import Quantity
from PIL import Image

from pylegs.config import configs
from pylegs.io import (PathLike, PathOrFile, _is_folder, _prepare_path,
                       compress_fits_image, download_file,
                       parallel_function_executor)
from pylegs.utils import iauname, iauname_path


def _coord_to_deg(
  coord: int | float | Quantity | SkyCoord = None,
  ra: int | float | Quantity = None,
  dec: int | float | Quantity = None,
) -> Tuple[float, float]:
  if coord and isinstance(coord, SkyCoord):
    return coord.ra.to(u.deg).value, coord.dec.to(u.deg).value
  
  if isinstance(ra, (float, int)):
    new_ra = ra
  if isinstance(ra, Quantity):
    new_dec = ra.to(u.deg).value
  
  if isinstance(dec, (float, int)):
    new_dec = dec
  if isinstance(dec, Quantity):
    new_dec = dec.to(u.deg).value
  
  return new_ra, new_dec


def cutout(
  coord: SkyCoord = None,
  ra: int | float | Quantity = None,
  dec: int | float | Quantity = None,
  save_path: PathOrFile = None,
  overwrite: bool = False,
  pixscale: float = 0.3,
  width: int = None,
  height: int = None,
  size: int = None,
  fmt: Literal['jpg', 'fits'] = 'jpg',
  bands: str = None,
  layer: str = None,
  compress_fits: bool = False,
  compress_type: str = 'HCOMPRESS_1',
  hcomp_scale: int = 3,
  quantize_level: int = 10,
  quantize_method: int = -1,
  http_client: requests.Session = None,
  dtype: Literal['bytes', 'numpy', 'pil', 'astropy'] = 'bytes'
) -> bytes | np.ndarray | Image.Image:
  """
  Downloads a single Legacy Survey object RGB stamp defined by RA and DEC.

  Parameters
  ----------
  ra: float
    Right ascension of the object.
  dec: float
    Declination of the object.
  save_path: pathlib.Path, optional
    Path where downloaded file will be stored.
  base_path: str, pathlib.Path, optional
    The path that will be appended at beggining of every paths if ``save_path``
    is ``None``.
  """
  ra, dec = _coord_to_deg(coord=coord, ra=ra, dec=dec)
  
  if fmt[0] == '.': fmt = fmt[1:]
    
  if fmt == 'jpg':
    url = configs.CUTOUT_RGB_BASE_URL
  else:
    url = configs.CUTOUT_FITS_BASE_URL
    
  if size is not None:
    width, height = size, size
  else:
    if width is None or height is None:
      width, height = 300, 300
      
  _prepare_path(save_path)

  if _is_folder(save_path):
    save_path = iauname_path(
      iaunames=iauname(ra=ra, dec=dec),
      prefix=save_path,
      suffix=f'.{fmt}'
    )

  query_params = {
    'ra': ra,
    'dec': dec,
    'width': width,
    'height': height,
    'pixscale': pixscale,
    'bands': bands,
    'layer': layer
  }

  image_bytes = download_file(
    url=url,
    query=query_params,
    save_path=save_path,
    http_client=http_client or configs.HTTP_CLIENT,
    replace=overwrite,
  )

  if compress_fits:
    compress_fits_image(
      file=BytesIO(image_bytes),
      compress_type=compress_type,
      hcomp_scale=hcomp_scale,
      quantize_level=quantize_level,
      quantize_method=quantize_method,
      ext=0,
      save_path=save_path,
      replace=overwrite,
    )
    
  if dtype == 'bytes':
    return image_bytes
  if dtype == 'pil':
    return Image.open(BytesIO(image_bytes))
  if dtype == 'numpy':
    return np.asarray(Image.open(BytesIO(image_bytes)))
  if dtype == 'astropy':
    return fits.open(BytesIO(image_bytes))



  
def batch_cutout(
  coords: SkyCoord = None,
  ra: Sequence[int | float | Quantity | SkyCoord] | SkyCoord = None,
  dec: Sequence[int | float | Quantity | SkyCoord] | SkyCoord = None,
  save_path: Sequence[PathLike] | PathLike = None,
  workers: int = 1,
  overwrite: bool = False,
  pixscale: Sequence[float | int] | float = 0.3,
  width: int = None,
  height: int = None,
  size: int = None,
  fmt: Literal['jpg', 'fits'] = 'jpg',
  bands: str = None,
  layer: str = None,
  compress_fits: bool = False,
  compress_type: str = 'HCOMPRESS_1',
  hcomp_scale: int = 3,
  quantize_level: int = 10,
  quantize_method: int = -1,
  http_client: requests.Session = None,
) -> Tuple[List[Path], List[Path]]:
  """
  Downloads a list of objects defined by RA and DEC coordinates.

  The ``ra``, ``dec`` and ``save_path`` lists are mandatory and
  must have same length.

  Parameters
  ----------
  ra: List[float]
    The list of RA coordinates of the desired objects.
  dec: List[float]
    The list of DEC coordinates of the desired objects.
  save_path: List[Path], optional
    The list of path where files should be saved.
  base_path: str, Path, optional
    The path that will be appended at beggining of every paths if ``save_path``
    is ``None``.
  """
  ra, dec = _coord_to_deg(coord=coords, ra=ra, dec=dec)
  
  if _is_folder(save_path):
    save_path = iauname_path(
      iaunames=iauname(ra=ra, dec=dec),
      prefix=Path(save_path),
      suffix=f'.{fmt}'
    )

  params = [
    {
      'ra': _ra,
      'dec': _dec,
      'save_path': _save_path,
      'overwrite': overwrite,
      'width': width,
      'height': height,
      'size': size,
      'bands': bands,
      'layer': layer,
      'compress_fits': compress_fits,
      'compress_type': compress_type,
      'hcomp_scale': hcomp_scale,
      'quantize_level': quantize_level,
      'quantize_method': quantize_method,
      'http_client': http_client,
    }
    for _ra, _dec, _save_path in zip(ra, dec, save_path)
  ]
  
  if np.isscalar(pixscale):
    params = [{**_param, 'pixelscale': pixscale} for _param in params]
  else:
    params = [{**_param, 'pixscale': _pixscale} for _param, _pixscale in zip(params, pixscale)]

  parallel_function_executor(
    cutout,
    params=params,
    workers=workers,
    unit='file'
  )

  success = [p for p in save_path if p.exists()]
  error = [p for p in save_path if not p.exists()]
  return success, error
    


if __name__ == '__main__':
  # ls = LegacyService(workers=6)
  # ls.batch_download_legacy_rgb(
  #   ra=[185.1458 + dx/2 for dx in range(20)],
  #   dec=[12.8624 + dy/2 for dy in range(20)],
  #   save_path=[Path(f'test/{i}.jpg') for i in range(20)]
  # )
  df = pd.DataFrame(({'ra':[184.4924, 184.4922], 'dec': [7.2737, 7.1862]}))
  # ls_crossmatch(df, ['mag_r', 'mag_g', 'mag_i', 'mag_z'], 3, 'test.csv')