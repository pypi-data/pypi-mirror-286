#!/usr/bin/env python
u"""
test_coordinates.py (07/2024)
Verify forward and backwards coordinate conversions

UPDATE HISTORY:
    Updated 07/2024: add check for if projections are geographic
    Updated 12/2023: use new crs class for coordinate reprojection
    Written 08/2020
"""
import pytest
import numpy as np
import pyTMD.crs

# parameterize projections
@pytest.mark.parametrize("PROJ", ['3031','CATS2008','3976','PSNorth','4326'])
# PURPOSE: verify forward and backwards coordinate conversions
def test_coordinates(PROJ):
    startlat = {'3031':-60,'CATS2008':-60,'3976':-60,'PSNorth':60,'4326':90}
    endlat = {'3031':-70,'CATS2008':-70,'3976':-70,'PSNorth':70,'4326':-90}
    is_geographic = {'3031':False,'CATS2008':False,'3976':False,
        'PSNorth':False,'4326':True}
    i1 = np.arange(-180,180+1,1)
    i2 = np.linspace(startlat[PROJ],endlat[PROJ],len(i1))
    # convert latitude and longitude to and from projection
    transform = pyTMD.crs().get(PROJ)
    o1, o2 = pyTMD.crs().convert(i1,i2,PROJ,'F')
    lon, lat = pyTMD.crs().convert(o1,o2,PROJ,'B')
    # calculate great circle distance between inputs and outputs
    cdist = np.arccos(np.sin(i2*np.pi/180.0)*np.sin(lat*np.pi/180.0) +
        np.cos(i2*np.pi/180.0)*np.cos(lat*np.pi/180.0)*
        np.cos((lon-i1)*np.pi/180.0),dtype=np.float32)
    # test that forward and backwards conversions are within tolerance
    eps = np.finfo(np.float32).eps
    assert np.all(cdist < eps)
    assert transform.is_geographic == is_geographic[PROJ]
