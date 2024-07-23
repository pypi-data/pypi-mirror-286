#!/usr/bin/env python
u"""
test_download_and_read.py (07/2024)
Tests that CATS2008 data can be downloaded from the US Antarctic Program (USAP)
Tests that AOTIM-5-2018 data can be downloaded from the NSF ArcticData server
Tests the read program to verify that constituents are being extracted
Tests that interpolated results are comparable to Matlab TMD program
    https://github.com/EarthAndSpaceResearch/TMD_Matlab_Toolbox_v2.5

PYTHON DEPENDENCIES:
    numpy: Scientific Computing Tools For Python
        https://numpy.org
        https://numpy.org/doc/stable/user/numpy-for-matlab-users.html
    scipy: Scientific Tools for Python
        https://docs.scipy.org/doc/
    Oct2Py: Python to GNU Octave Bridge
        https://oct2py.readthedocs.io/en/latest/
    boto3: Amazon Web Services (AWS) SDK for Python
        https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

UPDATE HISTORY:
    Updated 07/2024: add parametrize over cropping the model fields
    Updated 04/2024: use timescale for temporal operations
    Updated 01/2024: refactored compute functions into compute.py
    Updated 04/2023: using pathlib to define and expand paths
    Updated 12/2022: add check for read and interpolate constants
    Updated 11/2022: added encoding for writing ascii files
        use f-strings for formatting verbose or ascii output
    Updated 10/2022: added encoding for reading ascii files
    Updated 09/2021: added test for model definition files
    Updated 07/2021: download CATS2008 and AntTG from S3 to bypass USAP captcha
    Updated 05/2021: added test for check point program
    Updated 03/2021: use pytest fixture to setup and teardown model data
        use TMD tmd_tide_pred_plus to calculate OB time series
        refactor program into two classes for CATS2008 and AOTIM-5-2018
        replaced numpy bool/int to prevent deprecation warnings
    Updated 01/2021: download CATS2008 and AOTIM-5-2018 to subdirectories
    Updated 08/2020: Download Antarctic tide gauge database and compare with RMS
        directly call Matlab program (octave+oct2py) and compare outputs
        compare outputs for both Antarctic (CATS2008) and Arctic (AOTIM-5-2018)
        will install octave and oct2py in development requirements
    Written 08/2020
"""
import re
import io
import boto3
import shutil
import pytest
import inspect
import pathlib
import zipfile
import warnings
import posixpath
import numpy as np
import pyTMD.io
import pyTMD.io.model
import pyTMD.compute
import pyTMD.predict
import pyTMD.utilities
import pyTMD.check_points
import pyTMD.ellipse
import pyTMD.solve
import timescale.time
from oct2py import octave

# current file path
filename = inspect.getframeinfo(inspect.currentframe()).filename
filepath = pathlib.Path(filename).absolute().parent

# PURPOSE: calculate the matlab serial date from calendar date
# http://scienceworld.wolfram.com/astronomy/JulianDate.html
def convert_calendar_serial(year, month, day, hour=0.0, minute=0.0, second=0.0):
    # return the date in days since serial epoch 0000-01-01T00:00:00
    sd = 367.0*year - np.floor(7.0*(year + np.floor((month+9.0)/12.0))/4.0) - \
        np.floor(3.0*(np.floor((year + (month - 9.0)/7.0)/100.0) + 1.0)/4.0) + \
        np.floor(275.0*month/9.0) + day + hour/24.0 + minute/1440.0 + \
        second/86400.0 - 30.0
    return sd

# PURPOSE: Test and Verify CATS2008 model read and prediction programs
class Test_CATS2008:
    # PURPOSE: Download CATS2008 from US Antarctic Program
    @pytest.fixture(scope="class", autouse=False)
    def download_CATS2008(self):
        # download CATS2008 zip file and read as virtual file object
        HOST = ['https://www.usap-dc.org','dataset','usap-dc','601235',
            '2019-12-19T23:26:43.6Z','CATS2008.zip?dataset_id=601235']
        FILE = pyTMD.utilities.from_http(HOST)
        zfile = zipfile.ZipFile(FILE)
        print(f'{posixpath.join(*HOST)} -->\n')
        # find model files within zip file
        rx = re.compile(r'(grid|h[0f]?|UV[0]?|Model|xy)[_\.](.*?)',re.IGNORECASE)
        m = [m for m in zfile.filelist if rx.match(posixpath.basename(m.filename))]
        # verify that model files are within downloaded zip file
        assert all(m)
        # output tide directory for model
        modelpath = filepath.joinpath('CATS2008')
        # extract each member (model and configuration files)
        for member in m:
            # strip directories from member filename
            member.filename = posixpath.basename(member.filename)
            print(f'\t{modelpath.joinpath(member.filename)}\n')
            zfile.extract(member, path=modelpath)
        # close the zipfile object
        zfile.close()
        # output control file for tide model
        CFname = filepath.joinpath('Model_CATS2008')
        fid = CFname.open(mode='w', encoding='utf8')
        for model_file in ['hf.CATS2008.out','uv.CATS2008.out','grid_CATS2008']:
            print(modelpath.joinpath(model_file), file=fid)
        print('xy_ll_CATS2008', file=fid)
        fid.close()
        # verify control file
        assert CFname.exists()
        # run tests
        yield
        # clean up model
        shutil.rmtree(modelpath)
        # clean up
        CFname.unlink()

    # PURPOSE: Download CATS2008 from AWS S3 bucket
    @pytest.fixture(scope="class", autouse=True)
    def AWS_CATS2008(self, aws_access_key_id, aws_secret_access_key, aws_region_name):
        # get aws session object
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region_name)
        # get s3 object and bucket object for pytmd data
        s3 = session.resource('s3')
        bucket = s3.Bucket('pytmd')
        # model parameters for CATS2008
        modelpath = filepath.joinpath('CATS2008')
        # recursively create model directory
        modelpath.mkdir(parents=True, exist_ok=True)
        # output control file for tide model
        CFname = filepath.joinpath('Model_CATS2008')
        fid = CFname.open(mode='w', encoding='utf8')
        # retrieve each model file from s3
        for model_file in ['hf.CATS2008.out','uv.CATS2008.out','grid_CATS2008']:
            # retrieve CATS2008 model files
            obj = bucket.Object(key=posixpath.join('CATS2008',model_file))
            response = obj.get()
            local = modelpath.joinpath(model_file)
            with local.open(mode='wb') as destination:
                shutil.copyfileobj(response['Body'], destination)
            assert local.exists()
            # print to model control file
            print(local, file=fid)
        # retrieve CATS2008 coordinate file
        model_file = 'xy_ll_CATS2008.m'
        obj = bucket.Object(key=posixpath.join('CATS2008',model_file))
        response = obj.get()
        local = modelpath.joinpath(model_file)
        with local.open(mode='wb') as destination:
            shutil.copyfileobj(response['Body'], destination)
        # print coordinate conversion function to model control file
        print('xy_ll_CATS2008', file=fid)
        fid.close()
        # verify control file
        assert CFname.exists()
        # run tests
        yield
        # clean up model
        shutil.rmtree(modelpath)
        # clean up
        CFname.unlink()

    # PURPOSE: Download Antarctic Tide Gauge Database from US Antarctic Program
    @pytest.fixture(scope="class", autouse=False)
    def download_AntTG(self):
        # download Tide Gauge Database text file
        HOST = ['https://www.usap-dc.org','dataset','usap-dc','601358',
            '2020-07-10T19:50:08.8Z','AntTG_ocean_height_v1.txt?dataset_id=601358']
        local = filepath.joinpath('AntTG_ocean_height_v1.txt')
        pyTMD.utilities.from_http(HOST, local=local)
        assert local.exists()
        # run tests
        yield
        # clean up
        local.unlink()

    # PURPOSE: Download Antarctic Tide Gauge Database from AWS
    @pytest.fixture(scope="class", autouse=True)
    def AWS_AntTG(self, aws_access_key_id, aws_secret_access_key, aws_region_name):
        # get aws session object
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region_name)
        # get s3 object and bucket object for pytmd data
        s3 = session.resource('s3')
        bucket = s3.Bucket('pytmd')
        # retrieve Tide Gauge Database text file
        obj = bucket.Object(key='AntTG_ocean_height_v1.txt')
        response = obj.get()
        local = filepath.joinpath('AntTG_ocean_height_v1.txt')
        with local.open(mode='wb') as destination:
            shutil.copyfileobj(response['Body'], destination)
        assert local.exists()
        # run tests
        yield
        # clean up
        local.unlink()

    # PURPOSE: Test read program that grids and constituents are as expected
    def test_read_CATS2008(self, ny=2026, nx=1663):
        # model parameters for CATS2008
        modelpath = filepath.joinpath('CATS2008')
        grid_file = modelpath.joinpath('grid_CATS2008')
        elevation_file = modelpath.joinpath('hf.CATS2008.out')
        transport_file = modelpath.joinpath('uv.CATS2008.out')
        # read CATS2008 grid file
        xi,yi,hz,mz,iob,dt = pyTMD.io.OTIS.read_otis_grid(grid_file)
        # check dimensions of input grids
        assert (hz.shape == (ny,nx))
        assert (mz.shape == (ny,nx))
        # check constituent list
        constituents,nc = pyTMD.io.OTIS.read_constituents(elevation_file)
        cons = ['m2','s2','n2','k2','k1','o1','p1','q1','mf','mm']
        assert all(c in constituents for c in cons)
        # check dimensions of input grids from elevation and transport files
        for i,c in enumerate(constituents):
            z = pyTMD.io.OTIS.read_otis_elevation(elevation_file,i)
            u,v = pyTMD.io.OTIS.read_otis_transport(transport_file,i)
            assert (z.shape == (ny,nx))
            assert (u.shape == (ny,nx))
            assert (v.shape == (ny,nx))

    # PURPOSE: Tests check point program
    def test_check_CATS2008(self):
        lons = np.zeros((10)) + 178.0
        lats = -45.0 - np.arange(10)*5.0
        obs = pyTMD.check_points(lons, lats, DIRECTORY=filepath,
            MODEL='CATS2008', EPSG=4326)
        exp = np.array([False, False, False, False, True,
            True, True, True, False, False])
        assert np.all(obs == exp)

    # PURPOSE: Tests that interpolated results are comparable to AntTG database
    def test_compare_CATS2008(self):
        # model parameters for CATS2008
        modelpath = filepath.joinpath('CATS2008')
        grid_file = modelpath.joinpath('grid_CATS2008')
        model_file = modelpath.joinpath('hf.CATS2008.out')
        GRID = 'OTIS'
        EPSG = 'CATS2008'
        TYPE = 'z'

        # open Antarctic Tide Gauge (AntTG) database
        AntTG = filepath.joinpath('AntTG_ocean_height_v1.txt')
        with AntTG.open(mode='r', encoding='utf8') as f:
            file_contents = f.read().splitlines()
        # counts the number of lines in the header
        count = 0
        HEADER = True
        # Reading over header text
        while HEADER:
            # check if file line at count starts with matlab comment string
            HEADER = file_contents[count].startswith('%')
            # add 1 to counter
            count += 1
        # rewind 1 line
        count -= 1
        # iterate over number of stations
        constituents = ['q1','o1','p1','k1','n2','m2','s2','k2']
        antarctic_stations = (len(file_contents) - count)//10
        stations = [None]*antarctic_stations
        shortname = [None]*antarctic_stations
        station_lon = np.zeros((antarctic_stations))
        station_lat = np.zeros((antarctic_stations))
        station_amp = np.ma.zeros((antarctic_stations,len(constituents)))
        station_ph = np.ma.zeros((antarctic_stations,len(constituents)))
        for s in range(antarctic_stations):
            i = count + s*10
            stations[s] = file_contents[i + 1].strip()
            shortname[s] = file_contents[i + 3].strip()
            lat,lon,_,_ = file_contents[i + 4].split()
            station_lon[s] = np.float64(lon)
            station_lat[s] = np.float64(lat)
            amp = file_contents[i + 7].split()
            ph = file_contents[i + 8].split()
            station_amp.data[s,:] = np.array(amp,dtype=np.float64)
            station_ph.data[s,:] = np.array(ph,dtype=np.float64)
        # update masks where NaN
        station_amp.mask = np.isnan(station_amp.data) | (station_amp.data == 0.0)
        station_ph.mask = np.isnan(station_ph.data)
        # replace nans with fill values
        station_amp.data[station_amp.mask] = station_amp.fill_value
        station_ph.data[station_ph.mask] = station_ph.fill_value

        # extract amplitude and phase from tide model
        amp,ph,D,cons = pyTMD.io.OTIS.extract_constants(station_lon,
            station_lat, grid_file, model_file, EPSG, type=TYPE,
            method='spline', grid=GRID)
        # reorder constituents of model and convert amplitudes to cm
        model_amp = np.ma.zeros((antarctic_stations,len(constituents)))
        model_ph = np.ma.zeros((antarctic_stations,len(constituents)))
        for i,c in enumerate(constituents):
            j, = [j for j,val in enumerate(cons) if (val == c)]
            model_amp[:,i] = 100.0*amp[:,j]
            model_ph[:,i] = ph[:,j]
        # calculate complex constituent oscillations
        station_z = station_amp*np.exp(-1j*station_ph*np.pi/180.0)
        model_z = model_amp*np.exp(-1j*model_ph*np.pi/180.0)
        # valid stations for all constituents
        valid = np.all((~station_z.mask) & (~model_z.mask), axis=1)
        invalid_list = ['Ablation Lake','Amery','Bahia Esperanza','Beaver Lake',
            'Cape Roberts','Casey','Doake Ice Rumples','EE4A','EE4B',
            'Eklund Islands','Gerlache C','Groussac','Gurrachaga','Half Moon Is.',
            'Heard Island','Hobbs Pool','Mawson','McMurdo','Mikkelsen','Palmer',
            'Primavera','Rutford GL','Rutford GPS','Rothera','Scott Base',
            'Seymour Is','Terra Nova Bay']
        # remove coastal stations from the list
        invalid_stations = [i for i,s in enumerate(shortname) if s in invalid_list]
        valid[invalid_stations] = False
        nv = np.count_nonzero(valid)
        # compare with RMS values from King et al. (2011)
        # https://doi.org/10.1029/2011JC006949
        RMS = np.array([1.4,2.7,1.7,3.5,2.9,7.3,5.0,1.7])
        rms = np.zeros((len(constituents)))
        for i,c in enumerate(constituents):
            # calculate difference and rms
            difference = np.abs(station_z[valid,i] - model_z[valid,i])
            # round to precision of King et al. (2011)
            rms[i] = np.round(np.sqrt(np.sum(difference**2)/(2.0*nv)),decimals=1)
        # test RMS differences
        assert np.all(rms <= RMS)

    # parameterize type: heights versus currents
    parameters = []
    parameters.append(dict(type='z',model='hf.CATS2008.out',grid='grid_CATS2008'))
    parameters.append(dict(type='U',model='uv.CATS2008.out',grid='grid_CATS2008'))
    parameters.append(dict(type='V',model='uv.CATS2008.out',grid='grid_CATS2008'))
    @pytest.mark.parametrize("parameters", parameters)
    # PURPOSE: Tests that interpolated results are comparable to Matlab program
    def test_verify_CATS2008(self, parameters):
        # model parameters for CATS2008
        modelpath = filepath.joinpath('CATS2008')
        grid_file = modelpath.joinpath(parameters['grid'])
        model_file = modelpath.joinpath(parameters['model'])
        TYPE = parameters['type']
        GRID = 'OTIS'
        EPSG = 'CATS2008'

        # open Antarctic Tide Gauge (AntTG) database
        AntTG = filepath.joinpath('AntTG_ocean_height_v1.txt')
        with AntTG.open(mode='r', encoding='utf8') as f:
            file_contents = f.read().splitlines()
        # counts the number of lines in the header
        count = 0
        HEADER = True
        # Reading over header text
        while HEADER:
            # check if file line at count starts with matlab comment string
            HEADER = file_contents[count].startswith('%')
            # add 1 to counter
            count += 1
        # rewind 1 line
        count -= 1
        # iterate over number of stations
        antarctic_stations = (len(file_contents) - count)//10
        stations = [None]*antarctic_stations
        shortname = [None]*antarctic_stations
        station_type = [None]*antarctic_stations
        station_lon = np.zeros((antarctic_stations))
        station_lat = np.zeros((antarctic_stations))
        for s in range(antarctic_stations):
            i = count + s*10
            stations[s] = file_contents[i + 1].strip()
            shortname[s] = file_contents[i + 3].strip()
            lat,lon,_,_ = file_contents[i + 4].split()
            station_type[s] = file_contents[i + 6].strip()
            station_lon[s] = np.float64(lon)
            station_lat[s] = np.float64(lat)

        # calculate daily results for a time period
        # convert time to days since 1992-01-01T00:00:00
        tide_time = np.arange(timescale.time.convert_calendar_dates(2000,1,1),
            timescale.time.convert_calendar_dates(2000,12,31)+1)
        # serial dates for matlab program (days since 0000-01-01T00:00:00)
        SDtime = np.arange(convert_calendar_serial(2000,1,1),
            convert_calendar_serial(2000,12,31)+1)
        # presently not converting times to dynamic times for model comparisons
        deltat = np.zeros_like(tide_time)
        # number of days
        ndays = len(tide_time)

        # extract amplitude and phase from tide model
        amp,ph,D,c = pyTMD.io.OTIS.extract_constants(station_lon,
            station_lat, grid_file, model_file, EPSG, type=TYPE,
            method='spline', grid=GRID)
        # calculate complex phase in radians for Euler's
        cph = -1j*ph*np.pi/180.0

        # compare daily outputs at each station point
        invalid_list = ['Ablation Lake','Amery','Bahia Esperanza','Beaver Lake',
            'Cape Roberts','Casey','Doake Ice Rumples','EE4A','EE4B',
            'Eklund Islands','Gerlache C','Groussac','Gurrachaga','Half Moon Is.',
            'Heard Island','Hobbs Pool','Mawson','McMurdo','Mikkelsen','Palmer',
            'Primavera','Rutford GL','Rutford GPS','Rothera','Scott Base',
            'Seymour Is','Terra Nova Bay']
        # remove coastal stations from the list
        valid_stations=[i for i,s in enumerate(shortname) if s not in invalid_list]
        # will verify differences between model outputs are within tolerance
        eps = np.finfo(np.float16).eps

        # compute validation data from Matlab TMD program using octave
        # https://github.com/EarthAndSpaceResearch/TMD_Matlab_Toolbox_v2.5
        TMDpath = filepath.joinpath('..','TMD_Matlab_Toolbox','TMD').absolute()
        octave.addpath(octave.genpath(str(TMDpath)))
        octave.addpath(str(filepath))
        octave.addpath(str(modelpath))
        # turn off octave warnings
        octave.warning('off', 'all')
        # input control file for model
        CFname = filepath.joinpath('Model_CATS2008')
        assert CFname.exists()
        # run Matlab TMD program with octave
        # MODE: OB time series
        validation,_ = octave.tmd_tide_pred_plus(str(CFname), SDtime,
            station_lat[valid_stations], station_lon[valid_stations],
            TYPE, nout=2)

        # for each valid station
        for i,s in enumerate(valid_stations):
            # calculate constituent oscillation for station
            hc = amp[s,None,:]*np.exp(cph[s,None,:])
            # allocate for out tides at point
            tide = np.ma.zeros((ndays))
            tide.mask = np.zeros((ndays),dtype=bool)
            # predict tidal elevations at time and infer minor corrections
            tide.mask[:] = np.any(hc.mask)
            tide.data[:] = pyTMD.predict.time_series(tide_time, hc, c,
                deltat=deltat, corrections=GRID)
            minor = pyTMD.predict.infer_minor(tide_time, hc, c,
                deltat=deltat, corrections=GRID)
            tide.data[:] += minor.data[:]

            # calculate differences between matlab and python version
            difference = np.ma.zeros((ndays))
            difference.data[:] = tide.data - validation[:,i]
            difference.mask = (tide.mask | np.isnan(validation[:,i]))
            difference.data[difference.mask] = 0.0
            if not np.all(difference.mask):
                assert np.all(np.abs(difference) < eps)

    # PURPOSE: Tests that tidal ellipse results are comparable to Matlab program
    def test_tidal_ellipse(self):
        # model parameters for CATS2008
        modelpath = filepath.joinpath('CATS2008')
        grid_file = modelpath.joinpath('grid_CATS2008')
        model_file = modelpath.joinpath('uv.CATS2008.out')
        TYPES = ['U','V']
        GRID = 'OTIS'
        EPSG = 'CATS2008'

        # open Antarctic Tide Gauge (AntTG) database
        AntTG = filepath.joinpath('AntTG_ocean_height_v1.txt')
        with AntTG.open(mode='r', encoding='utf8') as f:
            file_contents = f.read().splitlines()
        # counts the number of lines in the header
        count = 0
        HEADER = True
        # Reading over header text
        while HEADER:
            # check if file line at count starts with matlab comment string
            HEADER = file_contents[count].startswith('%')
            # add 1 to counter
            count += 1
        # rewind 1 line
        count -= 1
        # iterate over number of stations
        antarctic_stations = (len(file_contents) - count)//10
        stations = [None]*antarctic_stations
        shortname = [None]*antarctic_stations
        station_type = [None]*antarctic_stations
        station_lon = np.zeros((antarctic_stations))
        station_lat = np.zeros((antarctic_stations))
        for s in range(antarctic_stations):
            i = count + s*10
            stations[s] = file_contents[i + 1].strip()
            shortname[s] = file_contents[i + 3].strip()
            lat,lon,_,_ = file_contents[i + 4].split()
            station_type[s] = file_contents[i + 6].strip()
            station_lon[s] = np.float64(lon)
            station_lat[s] = np.float64(lat)

        # compare outputs at each station point
        invalid_list = ['Ablation Lake','Amery','Bahia Esperanza','Beaver Lake',
            'Cape Roberts','Casey','Doake Ice Rumples','EE4A','EE4B',
            'Eklund Islands','Gerlache C','Groussac','Gurrachaga','Half Moon Is.',
            'Heard Island','Hobbs Pool','Mawson','McMurdo','Mikkelsen','Palmer',
            'Primavera','Rutford GL','Rutford GPS','Rothera','Scott Base',
            'Seymour Is','Terra Nova Bay']
        # remove coastal stations from the list
        i = [i for i,s in enumerate(shortname) if s not in invalid_list]
        valid_stations = len(i)
        # will verify differences between model outputs are within tolerance
        eps = np.finfo(np.float16).eps

        # compute validation data from Matlab TMD program using octave
        # https://github.com/EarthAndSpaceResearch/TMD_Matlab_Toolbox_v2.5
        TMDpath = filepath.joinpath('..','TMD_Matlab_Toolbox','TMD').absolute()
        octave.addpath(octave.genpath(str(TMDpath)))
        octave.addpath(str(filepath))
        octave.addpath(str(modelpath))
        # turn off octave warnings
        octave.warning('off', 'all')
        # input control file for model
        CFname = filepath.joinpath('Model_CATS2008')
        assert CFname.exists()

        # save complex amplitude for each current
        hc1,hc2 = ({},{})
        # iterate over zonal and meridional currents
        for TYPE in TYPES:
            # extract amplitude and phase from tide model
            amp,ph,D,c = pyTMD.io.OTIS.extract_constants(station_lon[i],
                station_lat[i], grid_file, model_file, EPSG, type=TYPE,
                method='spline', grid=GRID)
            # calculate complex phase in radians for Euler's
            cph = -1j*ph*np.pi/180.0
            # calculate constituent oscillation for station
            hc1[TYPE] = amp*np.exp(cph)

            # extract tidal harmonic constants out of a tidal model
            amp,ph,D,cons = octave.tmd_extract_HC(str(CFname),
                station_lat[i], station_lon[i], TYPE, nout=4)
            # calculate complex phase in radians for Euler's
            cph = -1j*ph*np.pi/180.0
            # calculate constituent oscillation for station
            hc2[TYPE] = amp*np.exp(cph)

        # number of constituents
        nc = len(c)
        # compute tidal ellipse parameters for python program
        test = {}
        test['umajor'],test['uminor'],test['uincl'],test['uphase'] = \
            pyTMD.ellipse.ellipse(hc1['U'],hc1['V'])
        # calculate currents using tidal ellipse inverse
        inverse = {}
        inverse['U'],inverse['V'] = pyTMD.ellipse.inverse(
            test['umajor'],test['uminor'],test['uincl'],test['uphase']
        )
        # compute tidal ellipse parameters for TMD matlab program
        valid = {}
        valid['umajor'],valid['uminor'],valid['uincl'],valid['uphase'] = \
            octave.TideEl(hc2['U'],hc2['V'],nout=4)

        # calculate differences between matlab and python version
        for key in ['umajor','uminor','uincl','uphase']:
            difference = np.ma.zeros((valid_stations, nc))
            difference.data[:] = test[key].data - valid[key].T
            difference.mask = (test[key].mask | np.isnan(valid[key].T))
            difference.data[difference.mask] = 0.0
            if not np.all(difference.mask):
                assert np.all(np.abs(difference) < eps)

        # calculate differences between forward and inverse functions
        for key in ['U', 'V']:
            difference = np.ma.zeros((valid_stations, nc), dtype=np.complex128)
            difference.data[:] = hc1[key].data - inverse[key].data
            difference.mask = (hc1[key].mask | inverse[key].mask)
            difference.data[difference.mask] = 0.0
            if not np.all(difference.mask):
                assert np.all(np.abs(difference) < eps)

    # PURPOSE: Tests solving for harmonic constants
    def test_solve(self):
        # get model parameters
        model = pyTMD.io.model(filepath).elevation('CATS2008')

        # calculate a forecast every minute
        minutes = np.arange(366*1440)
        # convert time to days relative to Jan 1, 1992 (48622 MJD)
        year, month, day = 2000, 1, 1
        tide_time = timescale.time.convert_calendar_dates(year, month, day,
            minute=minutes)

        # read tidal constants and interpolate to coordinates
        constituents = pyTMD.io.OTIS.read_constants(
            model.grid_file, model.model_file,
            model.projection, type=model.type,
            grid=model.format)
        c = constituents.fields
        DELTAT = np.zeros_like(tide_time)

        # interpolate constants to a coordinate
        LAT,LON = (-76.0, -40.0)
        amp,ph,D = pyTMD.io.OTIS.interpolate_constants(
            np.atleast_1d(LON), np.atleast_1d(LAT),
            constituents, model.projection, type=model.type,
            method='spline', extrapolate=True)

        # calculate complex form of constituent oscillation
        hc = amp*np.exp(-1j*ph*np.pi/180.0)
        # predict tidal elevations at times
        TIDE = pyTMD.predict.time_series(tide_time, hc, c,
            deltat=DELTAT, corrections=model.format)
        # solve for amplitude and phase
        famp, fph = pyTMD.solve.constants(tide_time, TIDE.data, c)
        # calculate complex form of constituent oscillation
        fhc = famp*np.exp(-1j*fph*np.pi/180.0)
        # verify differences are within tolerance
        eps = 5e-3
        for k,cons in enumerate(c):
            assert np.isclose(hc[0][k], fhc[k], rtol=eps, atol=eps)

    # parameterize type: heights versus currents
    # parameterize interpolation method
    parameters = []
    parameters.append(dict(type='z',model='hf.CATS2008.out',grid='grid_CATS2008'))
    parameters.append(dict(type='U',model='uv.CATS2008.out',grid='grid_CATS2008'))
    parameters.append(dict(type='V',model='uv.CATS2008.out',grid='grid_CATS2008'))
    @pytest.mark.parametrize("parameters", parameters)
    @pytest.mark.parametrize("METHOD", ['spline'])
    # PURPOSE: Tests that interpolated results are comparable
    def test_compare_constituents(self, parameters, METHOD):
        # model parameters for CATS2008
        modelpath = filepath.joinpath('CATS2008')
        grid_file = modelpath.joinpath(parameters['grid'])
        model_file = modelpath.joinpath(parameters['model'])
        TYPE = parameters['type']
        GRID = 'OTIS'
        EPSG = 'CATS2008'

        # open Antarctic Tide Gauge (AntTG) database
        AntTG = filepath.joinpath('AntTG_ocean_height_v1.txt')
        with AntTG.open(mode='r', encoding='utf8') as f:
            file_contents = f.read().splitlines()
        # counts the number of lines in the header
        count = 0
        HEADER = True
        # Reading over header text
        while HEADER:
            # check if file line at count starts with matlab comment string
            HEADER = file_contents[count].startswith('%')
            # add 1 to counter
            count += 1
        # rewind 1 line
        count -= 1
        # iterate over number of stations
        antarctic_stations = (len(file_contents) - count)//10
        stations = [None]*antarctic_stations
        shortname = [None]*antarctic_stations
        station_type = [None]*antarctic_stations
        station_lon = np.zeros((antarctic_stations))
        station_lat = np.zeros((antarctic_stations))
        for s in range(antarctic_stations):
            i = count + s*10
            stations[s] = file_contents[i + 1].strip()
            shortname[s] = file_contents[i + 3].strip()
            lat,lon,_,_ = file_contents[i + 4].split()
            station_type[s] = file_contents[i + 6].strip()
            station_lon[s] = np.float64(lon)
            station_lat[s] = np.float64(lat)

        # compare outputs at each station point
        invalid_list = ['Ablation Lake','Amery','Bahia Esperanza','Beaver Lake',
            'Cape Roberts','Casey','Doake Ice Rumples','EE4A','EE4B',
            'Eklund Islands','Gerlache C','Groussac','Gurrachaga','Half Moon Is.',
            'Heard Island','Hobbs Pool','Mawson','McMurdo','Mikkelsen','Palmer',
            'Primavera','Rutford GL','Rutford GPS','Rothera','Scott Base',
            'Seymour Is','Terra Nova Bay']
        # remove coastal stations from the list
        i = [i for i,s in enumerate(shortname) if s not in invalid_list]
        valid_stations = len(i)
        # will verify differences between model outputs are within tolerance
        eps = np.finfo(np.float16).eps

        # extract amplitude and phase from tide model
        amp1, ph1, D1, c = pyTMD.io.OTIS.extract_constants(station_lon[i],
            station_lat[i], grid_file, model_file, EPSG, type=TYPE,
            method=METHOD, grid=GRID)
        # calculate complex form of constituent oscillation
        hc1 = amp1*np.exp(-1j*ph1*np.pi/180.0)

        # read complex constituents from tide model
        constituents = pyTMD.io.OTIS.read_constants(grid_file, model_file,
            EPSG, type=TYPE, grid=GRID)
        # interpolate constituents to station coordinates
        amp2, ph2, D2 = pyTMD.io.OTIS.interpolate_constants(station_lon[i],
            station_lat[i], constituents, EPSG, type=TYPE,
            method=METHOD)
        # calculate complex form of constituent oscillation
        hc2 = amp2*np.exp(-1j*ph2*np.pi/180.0)

        # calculate differences between methods
        difference = np.ma.zeros((valid_stations, len(c)), dtype=np.complex128)
        difference.data[:] = hc1.data - hc2.data
        difference.mask = (hc1.mask | hc2.mask)
        difference.data[difference.mask] = 0.0
        if not np.all(difference.mask):
            assert np.all(np.abs(difference) < eps)

    # parameterize interpolation method
    # only use fast interpolation routines
    @pytest.mark.parametrize("METHOD", ['spline','nearest'])
    @pytest.mark.parametrize("EXTRAPOLATE", [True])
    # PURPOSE: test the tide correction wrapper function
    def test_Ross_Ice_Shelf(self, METHOD, EXTRAPOLATE):
        # create a drift track along the Ross Ice Shelf
        xlimits = np.array([-740000,520000])
        ylimits = np.array([-1430000,-300000])
        # x and y coordinates
        x = np.linspace(xlimits[0],xlimits[1],24)
        y = np.linspace(ylimits[0],ylimits[1],24)
        # time dimension
        delta_time = np.zeros((24))*3600
        # calculate tide drift corrections
        tide = pyTMD.compute.tide_elevations(x, y, delta_time,
            DIRECTORY=filepath, MODEL='CATS2008', GZIP=False,
            EPOCH=timescale.time._j2000_epoch, TYPE='drift', TIME='UTC',
            EPSG=3031, METHOD=METHOD, EXTRAPOLATE=EXTRAPOLATE)
        assert np.any(tide)

    # parameterize interpolation method
    # only use fast interpolation routines
    @pytest.mark.parametrize("METHOD", ['spline','nearest'])
    @pytest.mark.parametrize("EXTRAPOLATE", [True])
    # PURPOSE: test the tide currents wrapper function
    def test_Ross_Ice_Shelf_currents(self, METHOD, EXTRAPOLATE):
        # create a drift track along the Ross Ice Shelf
        xlimits = np.array([-740000,520000])
        ylimits = np.array([-1430000,-300000])
        # x and y coordinates
        x = np.linspace(xlimits[0],xlimits[1],24)
        y = np.linspace(ylimits[0],ylimits[1],24)
        # time dimension
        delta_time = np.zeros((24))*3600
        # calculate tide drift corrections
        tide = pyTMD.compute.tide_currents(x, y, delta_time,
            DIRECTORY=filepath, MODEL='CATS2008', GZIP=False,
            EPOCH=timescale.time._j2000_epoch, TYPE='drift', TIME='UTC',
            EPSG=3031, METHOD=METHOD, EXTRAPOLATE=EXTRAPOLATE)
        # iterate over zonal and meridional currents
        for key,val in tide.items():
            assert np.any(val)

    # PURPOSE: test definition file functionality
    @pytest.mark.parametrize("MODEL", ['CATS2008'])
    def test_definition_file(self, MODEL):
        # get model parameters
        model = pyTMD.io.model(filepath).elevation(MODEL)
        # create model definition file
        fid = io.StringIO()
        attrs = ['name','format','grid_file','model_file','type','projection']
        for attr in attrs:
            val = getattr(model,attr)
            if isinstance(val,list):
                fid.write('{0}\t{1}\n'.format(attr,','.join(val)))
            else:
                fid.write('{0}\t{1}\n'.format(attr,val))
        fid.seek(0)
        # use model definition file as input
        m = pyTMD.io.model().from_file(fid)
        for attr in attrs:
            assert getattr(model,attr) == getattr(m,attr)


# PURPOSE: Test and Verify AOTIM-5-2018 model read and prediction programs
class Test_AOTIM5_2018:
    # PURPOSE: Download AOTIM-5-2018 from NSF ArcticData server
    @pytest.fixture(scope="class", autouse=True)
    def download_AOTIM5_2018(self):
        # build host url for model
        doi = '10.18739/A21R6N14K'
        resource_map_doi = f'resource_map_doi:{doi}'
        HOST = ['https://arcticdata.io','metacat','d1','mn','v2','packages',
            pyTMD.utilities.quote_plus(posixpath.join('application','bagit-097')),
            pyTMD.utilities.quote_plus(resource_map_doi)]
        # download zipfile from host
        FILE = pyTMD.utilities.from_http(HOST)
        zfile = zipfile.ZipFile(FILE)
        print(f'{posixpath.join(*HOST)} -->\n')
        # find model files within zip file
        rx = re.compile(r'(grid|h[0f]?|UV[0]?|Model|xy)[_\.](.*?)',re.IGNORECASE)
        m = [m for m in zfile.filelist if rx.match(posixpath.basename(m.filename))]
        # verify that model files are within downloaded zip file
        assert all(m)
        # output tide directory for model
        modelpath = filepath.joinpath('Arc5km2018')
        # extract each member (model and configuration files)
        for member in m:
            # strip directories from member filename
            member.filename = posixpath.basename(member.filename)
            print(f'\t{modelpath.joinpath(member.filename)}\n')
            # extract file
            zfile.extract(member, path=modelpath)
        # close the zipfile object
        zfile.close()
        # output control file for tide model
        CFname = filepath.joinpath('Model_Arc5km2018')
        fid = CFname.open(mode='w', encoding='utf8')
        for model_file in ['h_Arc5km2018','UV_Arc5km2018','grid_Arc5km2018']:
            print(modelpath.joinpath(model_file), file=fid)
        print('xy_ll_Arc5km2018', file=fid)
        fid.close()
        # verify control file
        assert CFname.exists()
        # run tests
        yield
        # clean up model
        shutil.rmtree(modelpath)
        # clean up
        CFname.unlink()

    # PURPOSE: Download Arctic Tidal Current Atlas list of records
    @pytest.fixture(scope="class", autouse=True)
    def download_Arctic_Tide_Atlas(self):
        HOST = ['https://arcticdata.io','metacat','d1','mn','v2','object',
            'urn%3Auuid%3Ae3abe2cc-f903-44de-9758-0c6bfc5b66c9']
        local = filepath.joinpath('List_of_records.txt')
        pyTMD.utilities.from_http(HOST, local=local)
        assert local.exists()
        # run tests
        yield
        # clean up
        local.unlink()

    # parameterize type: heights versus currents
    parameters = []
    parameters.append(dict(type='z',model='h_Arc5km2018',grid='grid_Arc5km2018'))
    parameters.append(dict(type='U',model='UV_Arc5km2018',grid='grid_Arc5km2018'))
    parameters.append(dict(type='V',model='UV_Arc5km2018',grid='grid_Arc5km2018'))
    @pytest.mark.parametrize("parameters", parameters)
    # PURPOSE: Tests that interpolated results are comparable to Matlab program
    def test_verify_AOTIM5_2018(self, parameters):
        # model parameters for AOTIM-5-2018
        modelpath = filepath.joinpath('Arc5km2018')
        grid_file = modelpath.joinpath(parameters['grid'])
        model_file = modelpath.joinpath(parameters['model'])
        TYPE = parameters['type']
        GRID = 'OTIS'
        EPSG = 'PSNorth'

        # open Arctic Tidal Current Atlas list of records
        ATLAS = filepath.joinpath('List_of_records.txt')
        with ATLAS.open(mode='r', encoding='utf8') as f:
            file_contents = f.read().splitlines()
        # skip 2 header rows
        count = 2
        # iterate over number of stations
        arctic_stations = len(file_contents) - count
        stations = [None]*arctic_stations
        shortname = [None]*arctic_stations
        station_lon = np.zeros((arctic_stations))
        station_lat = np.zeros((arctic_stations))
        for s in range(arctic_stations):
            line_contents = file_contents[count+s].split()
            stations[s] = line_contents[1]
            shortname[s] = line_contents[2]
            station_lat[s] = np.float64(line_contents[10])
            station_lon[s] = np.float64(line_contents[11])

        # calculate daily results for a time period
        # convert time to days since 1992-01-01T00:00:00
        tide_time = np.arange(timescale.time.convert_calendar_dates(2000,1,1),
            timescale.time.convert_calendar_dates(2000,12,31)+1)
        # serial dates for matlab program (days since 0000-01-01T00:00:00)
        SDtime = np.arange(convert_calendar_serial(2000,1,1),
            convert_calendar_serial(2000,12,31)+1)
        # presently not converting times to dynamic times for model comparisons
        deltat = np.zeros_like(tide_time)
        # number of days
        ndays = len(tide_time)

        # extract amplitude and phase from tide model
        amp,ph,D,c = pyTMD.io.OTIS.extract_constants(station_lon,
            station_lat, grid_file, model_file, EPSG, type=TYPE,
            method='spline', grid=GRID)
        # calculate complex phase in radians for Euler's
        cph = -1j*ph*np.pi/180.0
        # will verify differences between model outputs are within tolerance
        eps = np.finfo(np.float16).eps

        # compare daily outputs at each station point
        invalid_list = ['BC1','KS12','KS14','BI3','BI4']
        # remove coastal stations from the list
        valid_stations=[i for i,s in enumerate(shortname) if s not in invalid_list]

        # compute validation data from Matlab TMD program using octave
        # https://github.com/EarthAndSpaceResearch/TMD_Matlab_Toolbox_v2.5
        TMDpath = filepath.joinpath('..','TMD_Matlab_Toolbox','TMD').absolute()
        octave.addpath(octave.genpath(str(TMDpath)))
        octave.addpath(str(filepath))
        octave.addpath(str(modelpath))
        # turn off octave warnings
        octave.warning('off', 'all')
        # input control file for model
        CFname = filepath.joinpath('Model_Arc5km2018')
        assert CFname.exists()
        # run Matlab TMD program with octave
        # MODE: OB time series
        validation,_ = octave.tmd_tide_pred_plus(str(CFname), SDtime,
            station_lat[valid_stations], station_lon[valid_stations],
            TYPE, nout=2)

        # for each valid station
        for i,s in enumerate(valid_stations):
            # calculate constituent oscillation for station
            hc = amp[s,None,:]*np.exp(cph[s,None,:])
            # allocate for out tides at point
            tide = np.ma.zeros((ndays))
            tide.mask = np.zeros((ndays),dtype=bool)
            # predict tidal elevations at time and infer minor corrections
            tide.mask[:] = np.any(hc.mask)
            tide.data[:] = pyTMD.predict.time_series(tide_time, hc, c,
                deltat=deltat, corrections=GRID)
            minor = pyTMD.predict.infer_minor(tide_time, hc, c,
                deltat=deltat, corrections=GRID)
            tide.data[:] += minor.data[:]

            # calculate differences between matlab and python version
            difference = np.ma.zeros((ndays))
            difference.data[:] = tide.data - validation[:,i]
            difference.mask = (tide.mask | np.isnan(validation[:,i]))
            difference.data[difference.mask] = 0.0
            if not np.all(difference.mask):
                assert np.all(np.abs(difference) < eps)

    # parameterize type: heights versus currents
    # parameterize interpolation method
    parameters = []
    parameters.append(dict(type='z',model='h_Arc5km2018',grid='grid_Arc5km2018'))
    parameters.append(dict(type='U',model='UV_Arc5km2018',grid='grid_Arc5km2018'))
    parameters.append(dict(type='V',model='UV_Arc5km2018',grid='grid_Arc5km2018'))
    @pytest.mark.parametrize("parameters", parameters)
    @pytest.mark.parametrize("METHOD", ['spline'])
    # PURPOSE: Tests that interpolated results are comparable
    def test_compare_constituents(self, parameters, METHOD):
        # model parameters for AOTIM-5-2018
        modelpath = filepath.joinpath('Arc5km2018')
        grid_file = modelpath.joinpath(parameters['grid'])
        model_file = modelpath.joinpath(parameters['model'])
        TYPE = parameters['type']
        GRID = 'OTIS'
        EPSG = 'PSNorth'

        # open Arctic Tidal Current Atlas list of records
        ATLAS = filepath.joinpath('List_of_records.txt')
        with ATLAS.open(mode='r', encoding='utf8') as f:
            file_contents = f.read().splitlines()
        # skip 2 header rows
        count = 2
        # iterate over number of stations
        arctic_stations = len(file_contents) - count
        stations = [None]*arctic_stations
        shortname = [None]*arctic_stations
        station_lon = np.zeros((arctic_stations))
        station_lat = np.zeros((arctic_stations))
        for s in range(arctic_stations):
            line_contents = file_contents[count+s].split()
            stations[s] = line_contents[1]
            shortname[s] = line_contents[2]
            station_lat[s] = np.float64(line_contents[10])
            station_lon[s] = np.float64(line_contents[11])

        # compare outputs at each station point
        invalid_list = ['BC1','KS12','KS14','BI3','BI4']
        # remove coastal stations from the list
        i = [i for i,s in enumerate(shortname) if s not in invalid_list]
        valid_stations = len(i)
        # will verify differences between model outputs are within tolerance
        eps = np.finfo(np.float16).eps

        # extract amplitude and phase from tide model
        amp1,ph1,D1,c = pyTMD.io.OTIS.extract_constants(station_lon[i],
            station_lat[i], grid_file, model_file, EPSG, type=TYPE,
            method=METHOD, grid=GRID)
        # calculate complex form of constituent oscillation
        hc1 = amp1*np.exp(-1j*ph1*np.pi/180.0)

        # read complex constituents from tide model
        constituents = pyTMD.io.OTIS.read_constants(grid_file, model_file,
            EPSG, type=TYPE, grid=GRID)
        # interpolate constituents to station coordinates
        amp2,ph2,D2 = pyTMD.io.OTIS.interpolate_constants(station_lon[i],
            station_lat[i], constituents, EPSG, type=TYPE,
            method=METHOD)
        # calculate complex form of constituent oscillation
        hc2 = amp2*np.exp(-1j*ph2*np.pi/180.0)

        # calculate differences between methods
        difference = np.ma.zeros((valid_stations, len(c)), dtype=np.complex128)
        difference.data[:] = hc1.data - hc2.data
        difference.mask = (hc1.mask | hc2.mask)
        difference.data[difference.mask] = 0.0
        if not np.all(difference.mask):
            assert np.all(np.abs(difference) < eps)

    # parameterize interpolation method
    # only use fast interpolation routines
    @pytest.mark.parametrize("METHOD", ['spline','nearest'])
    @pytest.mark.parametrize("EXTRAPOLATE", [True])
    # PURPOSE: test the tide correction wrapper function
    def test_Arctic_Ocean(self, METHOD, EXTRAPOLATE):
        # create an image around the Arctic Ocean
        # use NSIDC Polar Stereographic definitions
        # https://nsidc.org/data/polar-stereo/ps_grids.html
        xlimits = [-3850000,3750000]
        ylimits = [-5350000,5850000]
        spacing = [50e3,-50e3]
        # x and y coordinates
        x = np.arange(xlimits[0],xlimits[1]+spacing[0],spacing[0])
        y = np.arange(ylimits[1],ylimits[0]+spacing[1],spacing[1])
        xgrid,ygrid = np.meshgrid(x,y)
        # time dimension
        delta_time = 0.0
        # calculate tide map
        tide = pyTMD.compute.tide_elevations(xgrid, ygrid, delta_time,
            DIRECTORY=filepath, MODEL='AOTIM-5-2018', GZIP=False,
            EPOCH=timescale.time._j2000_epoch, TYPE='grid', TIME='UTC',
            EPSG=3413, METHOD=METHOD, EXTRAPOLATE=EXTRAPOLATE)
        assert np.any(tide)

    # PURPOSE: test definition file functionality
    @pytest.mark.parametrize("MODEL", ['AOTIM-5-2018'])
    def test_definition_file(self, MODEL):
        # get model parameters
        model = pyTMD.io.model(filepath).elevation(MODEL)
        # create model definition file
        fid = io.StringIO()
        attrs = ['name','format','grid_file','model_file','type','projection']
        for attr in attrs:
            val = getattr(model,attr)
            if isinstance(val,list):
                var = ','.join(str(v) for v in val)
                fid.write(f'{attr}\t{var}\n')
            else:
                fid.write(f'{attr}\t{val}\n')
        fid.seek(0)
        # use model definition file as input
        m = pyTMD.io.model().from_file(fid)
        for attr in attrs:
            assert getattr(model,attr) == getattr(m,attr)

# PURPOSE: test extend function
def test_extend_array():
    dlon = 1
    lon = np.arange(0, 360, dlon)
    valid = np.arange(-dlon, 360 + dlon, dlon)
    test = pyTMD.io.OTIS._extend_array(lon, dlon)
    assert np.all(test == valid)
