# ------------------------------------------------------------------
# Copyright (c) 2020 PyInstaller Development Team.
#
# This file is distributed under the terms of the GNU General Public
# License (version 2.0 or later).
#
# The full license is available in LICENSE.GPL.txt, distributed with
# this software.
#
# SPDX-License-Identifier: GPL-2.0-or-later
# ------------------------------------------------------------------
import pytest
from pathlib import Path
from PyInstaller.compat import is_darwin, is_linux, is_py39, is_win
from PyInstaller.utils.hooks import is_module_satisfies, can_import_module
from PyInstaller.utils.tests import importorskip, requires, xfail


@importorskip('fiona')
def test_fiona(pyi_builder):
    pyi_builder.test_source(
        '''
        import fiona
        '''
    )

@importorskip('jinxed')
def test_jinxed(pyi_builder):
    pyi_builder.test_source(
        '''
        import jinxed
        jinxed.setupterm('xterm')
        assert jinxed._terminal.TERM.terminfo is jinxed.terminfo.xterm
        '''
    )


def tensorflow_onedir_only(test):
    def wrapped(pyi_builder):
        if pyi_builder._mode != 'onedir':
            pytest.skip('Tensorflow tests support only onedir mode '
                        'due to potential distribution size.')
        test(pyi_builder)

    return wrapped


@importorskip('tensorflow')
@tensorflow_onedir_only
def test_tensorflow(pyi_builder):
    pyi_builder.test_source(
        """
        from tensorflow import *
        """
    )


@importorskip('tensorflow')
@tensorflow_onedir_only
def test_tensorflow_layer(pyi_builder):
    pyi_builder.test_script('pyi_lib_tensorflow_layer.py')


@importorskip('tensorflow')
@tensorflow_onedir_only
def test_tensorflow_mnist(pyi_builder):
    pyi_builder.test_script('pyi_lib_tensorflow_mnist.py')


@importorskip('trimesh')
def test_trimesh(pyi_builder):
    pyi_builder.test_source(
        """
        import trimesh
        """
    )


@importorskip('apscheduler')
def test_apscheduler(pyi_builder):
    pyi_builder.test_source(
        """
        import apscheduler
        import pytz
        import asyncio
        import random
        import datetime as dt
        from apscheduler.schedulers.asyncio import AsyncIOScheduler
        from apscheduler.triggers.interval import IntervalTrigger
        loop = asyncio.get_event_loop()
        async def test_function(data=0):
            print(dt.datetime.now(), random.randint(0, 100))
        test_scheduler = AsyncIOScheduler()
        test_scheduler.add_job(
            test_function,
            id="TestJob",
            trigger=IntervalTrigger(
                seconds=1,
                start_date=dt.datetime.now(tz=pytz.UTC)
            )
        )
        test_scheduler.start()
        loop.run_until_complete(asyncio.sleep(5))
    """
    )


@importorskip('boto')
@xfail(reason='boto does not fully support Python 3')
def test_boto(pyi_builder):
    pyi_builder.test_script('pyi_lib_boto.py')


@xfail(reason='Issue #1844.')
@importorskip('boto3')
def test_boto3(pyi_builder):
    pyi_builder.test_source(
        """
        import boto3
        session = boto3.Session(region_name='us-west-2')

        # verify all clients
        for service in session.get_available_services():
            session.client(service)

        # verify all resources
        for resource in session.get_available_resources():
            session.resource(resource)
        """)


@xfail(reason='Issue #1844.')
@importorskip('botocore')
def test_botocore(pyi_builder):
    pyi_builder.test_source(
        """
        import botocore
        from botocore.session import Session
        session = Session()
        # verify all services
        for service in session.get_available_services():
            session.create_client(service, region_name='us-west-2')
        """)


@xfail(is_darwin, reason='Issue #1895.')
@importorskip('enchant')
def test_enchant(pyi_builder):
    pyi_builder.test_script('pyi_lib_enchant.py')


@importorskip('zmq')
def test_zmq(pyi_builder):
    pyi_builder.test_source(
        """
        import zmq
        print(zmq.__version__)
        print(zmq.zmq_version())
        # This is a problematic module and might cause some issues.
        import zmq.utils.strtypes
        """)


@importorskip('pylint')
def test_pylint(pyi_builder):
    pyi_builder.test_source(
        """
        # The following more obvious test doesn't work::
        #
        #   import pylint
        #   pylint.run_pylint()
        #
        # because pylint will exit with 32, since a valid command
        # line wasn't given. Instead, provide a valid command line below.

        from pylint.lint import Run
        Run(['-h'])
        """)


@importorskip('markdown')
def test_markdown(pyi_builder):
    # Markdown uses __import__ed extensions. Make sure these work by
    # trying to use the 'toc' extension, using both short and long format.
    pyi_builder.test_source(
        """
        import markdown
        print(markdown.markdown('testing',
            extensions=['toc']))
        print(markdown.markdown('testing',
            extensions=['markdown.extensions.toc']))
        """)


@importorskip('lxml')
def test_lxml_isoschematron(pyi_builder):
    pyi_builder.test_source(
        """
        # The import of this module triggers the loading of some
        # required XML files.
        from lxml import isoschematron
        """)


@importorskip('openpyxl')
def test_openpyxl(pyi_builder):
    pyi_builder.test_source(
        """
        # Test the hook to openpyxl
        from openpyxl import __version__
        """)


@importorskip('pyodbc')
def test_pyodbc(pyi_builder):
    pyi_builder.test_source(
        """
        # pyodbc is a binary Python module. On Windows when installed with easy_install
        # it is installed as zipped Python egg. This binary module is extracted
        # to PYTHON_EGG_CACHE directory. PyInstaller should find the binary there and
        # include it with frozen executable.
        import pyodbc
        """)


@importorskip('pyttsx')
def test_pyttsx(pyi_builder):
    pyi_builder.test_source(
        """
        # Basic code example from pyttsx tutorial.
        # http://packages.python.org/pyttsx/engine.html#examples
        import pyttsx
        engine = pyttsx.init()
        engine.say('Sally sells seashells by the seashore.')
        engine.say('The quick brown fox jumped over the lazy dog.')
        engine.runAndWait()
        """)


@importorskip('pyttsx3')
def test_pyttsx3(pyi_builder):
    pyi_builder.test_source("""
        import pyttsx3
        engine = pyttsx3.init()
    """)


@importorskip('pycparser')
def test_pycparser(pyi_builder):
    pyi_builder.test_script('pyi_lib_pycparser.py')


@importorskip('Crypto')
def test_pycrypto(pyi_builder):
    pyi_builder.test_source(
        """
        import binascii
        from Crypto.Cipher import AES
        BLOCK_SIZE = 16
        print('AES null encryption, block size', BLOCK_SIZE)
        # Just for testing functionality after all
        print('HEX', binascii.hexlify(
            AES.new(b"\\0" * BLOCK_SIZE, AES.MODE_ECB).encrypt(b"\\0" * BLOCK_SIZE)))
        from Crypto.PublicKey import ECC
        """)


@importorskip('Cryptodome')
def test_cryptodome(pyi_builder):
    pyi_builder.test_source(
        """
        from Cryptodome import Cipher
        from Cryptodome.PublicKey import ECC
        print('Cryptodome Cipher Module:', Cipher)
        """)


@importorskip('h5py')
def test_h5py(pyi_builder):
    pyi_builder.test_source("""
        import h5py
        """)


@importorskip('unidecode')
def test_unidecode(pyi_builder):
    pyi_builder.test_source("""
        from unidecode import unidecode

        # Unidecode should not skip non-ASCII chars if mappings for them exist.
        assert unidecode(u"kožušček") == "kozuscek"
        """)


@importorskip('pinyin')
def test_pinyin(pyi_builder):
    pyi_builder.test_source("""
        import pinyin
        """)


@importorskip('uvloop')
@pytest.mark.darwin
@pytest.mark.linux
def test_uvloop(pyi_builder):
    pyi_builder.test_source("import uvloop")


@importorskip('web3')
def test_web3(pyi_builder):
    pyi_builder.test_source("import web3")


@importorskip('phonenumbers')
def test_phonenumbers(pyi_builder):
    pyi_builder.test_source("""
        import phonenumbers

        number = '+17034820623'
        parsed_number = phonenumbers.parse(number)

        assert(parsed_number.country_code == 1)
        assert(parsed_number.national_number == 7034820623)
        """)


@importorskip('pendulum')
def test_pendulum(pyi_builder):
    pyi_builder.test_source("""
        import pendulum

        print(pendulum.now().isoformat())
        """)


@importorskip('humanize')
def test_humanize(pyi_builder):
    pyi_builder.test_source("""
        import humanize
        from datetime import timedelta

        print(humanize.naturaldelta(timedelta(seconds=125)))
        """)


@importorskip('argon2')
def test_argon2(pyi_builder):
    pyi_builder.test_source("""
        from argon2 import PasswordHasher

        ph = PasswordHasher()
        hash = ph.hash("s3kr3tp4ssw0rd")
        ph.verify(hash, "s3kr3tp4ssw0rd")
        """)


@importorskip('pytest')
def test_pytest_runner(pyi_builder):
    """
    Check if pytest runner builds correctly.
    """
    pyi_builder.test_source(
        """
        import pytest
        import sys
        sys.exit(pytest.main(['--help']))
        """)


@importorskip('eel')
def test_eel(pyi_builder):
    pyi_builder.test_source("import eel")


@importorskip('sentry_sdk')
def test_sentry(pyi_builder):
    pyi_builder.test_source(
        """
        import sentry_sdk
        sentry_sdk.init()
        """)


@importorskip('iminuit')
def test_iminuit(pyi_builder):
    pyi_builder.test_source("""
        from iminuit import Minuit
        """)


@importorskip('av')
def test_av(pyi_builder):
    pyi_builder.test_source("""
        import av
        """)


@importorskip('passlib')
@xfail(is_linux and is_py39 and not is_module_satisfies('passlib > 1.7.4'),
       reason='Passlib does not account for crypt() behavior change that '
              'was introduced in 3.9.x (python #39289).')
def test_passlib(pyi_builder):
    pyi_builder.test_source("""
        import passlib.apache
        """)


@importorskip('publicsuffix2')
def test_publicsuffix2(pyi_builder):
    pyi_builder.test_source("""
        import publicsuffix2
        publicsuffix2.PublicSuffixList()
        """)


@importorskip('pydivert')
def test_pydivert(pyi_builder):
    pyi_builder.test_source("""
        import pydivert
        pydivert.WinDivert.check_filter("inbound")
        """)


@pytest.mark.slow
@importorskip('skimage')
@pytest.mark.skipif(not is_module_satisfies('scikit_image >= 0.16'),
                    reason='The test supports only scikit-image >= 0.16.')
@pytest.mark.parametrize('submodule', [
    'color', 'data', 'draw', 'exposure', 'feature', 'filters', 'future',
    'graph', 'io', 'measure', 'metrics', 'morphology', 'registration',
    'restoration', 'segmentation', 'transform', 'util', 'viewer'
])
def test_skimage(pyi_builder, submodule):
    pyi_builder.test_source("""
        import skimage.{0}
        """.format(submodule))


@pytest.mark.slow
@importorskip('sklearn')
@pytest.mark.skipif(not is_module_satisfies('scikit_learn >= 0.21'),
                    reason='The test supports only scikit-learn >= 0.21.')
@pytest.mark.parametrize('submodule', [
    'calibration', 'cluster', 'covariance', 'cross_decomposition',
    'datasets', 'decomposition', 'dummy', 'ensemble', 'exceptions',
    'experimental', 'externals', 'feature_extraction',
    'feature_selection', 'gaussian_process', 'inspection',
    'isotonic', 'kernel_approximation', 'kernel_ridge',
    'linear_model', 'manifold', 'metrics', 'mixture',
    'model_selection', 'multiclass', 'multioutput',
    'naive_bayes', 'neighbors', 'neural_network', 'pipeline',
    'preprocessing', 'random_projection', 'semi_supervised',
    'svm', 'tree', 'discriminant_analysis', 'impute', 'compose'
])
def test_sklearn(pyi_builder, submodule):
    pyi_builder.test_source("""
        import sklearn.{0}
        """.format(submodule))


@importorskip('statsmodels')
@pytest.mark.skipif(not is_module_satisfies('statsmodels >= 0.12'),
                    reason='This has only been tested with statsmodels >= 0.12.')
def test_statsmodels(pyi_builder):
    pyi_builder.test_source("""
        import statsmodels.api as sm
        """)


@importorskip('win32ctypes')
@pytest.mark.skipif(not is_win, reason='pywin32-ctypes is supported only on Windows')
@pytest.mark.parametrize('submodule', ['win32api', 'win32cred', 'pywintypes'])
def test_pywin32ctypes(pyi_builder, submodule):
    pyi_builder.test_source("""
        from win32ctypes.pywin32 import {0}
        """.format(submodule))


@importorskip('pyproj')
@pytest.mark.skipif(not is_module_satisfies('pyproj >= 2.1.3'),
                    reason='The test supports only pyproj >= 2.1.3.')
def test_pyproj(pyi_builder):
    pyi_builder.test_source("""
        import pyproj
        tf = pyproj.Transformer.from_crs(
            7789,
            8401
        )
        result = tf.transform(
            xx=3496737.2679,
            yy=743254.4507,
            zz=5264462.9620,
            tt=2019.0
        )
        print(result)
        """)


@importorskip('pydantic')
def test_pydantic(pyi_builder):
    pyi_builder.test_source("""
        import pydantic
        """)


def torch_onedir_only(test):
    def wrapped(pyi_builder):
        if pyi_builder._mode != 'onedir':
            pytest.skip('PyTorch tests support only onedir mode '
                        'due to potential distribution size.')
        test(pyi_builder)

    return wrapped


@importorskip('torchvision')
@torch_onedir_only
def test_torchvision_nms(pyi_builder):
    pyi_builder.test_source("""
        import torch
        import torchvision
        # boxes: Nx4 tensor (x1, y1, x2, y2)
        boxes = torch.tensor([
            [0.0, 0.0, 1.0, 1.0],
            [0.45, 0.0, 1.0, 1.0],
        ])
        # scores: Nx1 tensor
        scores = torch.tensor([
            1.0,
            1.1
        ])
        keep = torchvision.ops.nms(boxes, scores, 0.5)
        # The boxes have IoU of 0.55, and the second one has a slightly
        # higher score, so we expect it to be kept while the first one
        # is discarded.
        assert keep == 1
    """)


@importorskip('googleapiclient')
def test_googleapiclient(pyi_builder):
    pyi_builder.test_source("""
        from googleapiclient.discovery import build
        """)


@importorskip('plotly')
@importorskip('pandas')
def test_plotly(pyi_builder):
    pyi_builder.test_source("""
        import pandas as pd
        import plotly.express as px

        data = [(1, 1), (2, 1), (3, 5), (4, -3)]
        df = pd.DataFrame.from_records(data, columns=['col_1', 'col_2'])
        fig = px.scatter(df, x='col_1', y='col_2')
        """)


@pytest.mark.timeout(600)
@importorskip('dash')
def test_dash(pyi_builder):
    pyi_builder.test_source("""
        import dash
        import dash_core_components as dcc
        import dash_html_components as html
        from dash.dependencies import Input, Output

        app = dash.Dash(__name__)
        app.layout = html.Div(
            [
                dcc.Input(id='input_text', type='text', placeholder='input type text'),
                html.Div(id='out-all-types'),
            ]
        )

        @app.callback(
            Output('out-all-types', 'children'),
            [Input('input_text', 'value')],
        )
        def cb_render(val):
            return val
        """)


@importorskip('dash_table')
def test_dash_table(pyi_builder):
    pyi_builder.test_source("""
        import dash
        import dash_table

        app = dash.Dash(__name__)
        app.layout = dash_table.DataTable(
            id='table',
            columns=[{'name': 'a', 'id': 'a'}, {'name': 'b', 'id': 'b'}],
            data=[{'a': 1, 'b': 2}, {'a': 3, 'b': 4}],
        )
        """)


@importorskip('dash_bootstrap_components')
def test_dash_bootstrap_components(pyi_builder):
    pyi_builder.test_source("""
        import dash
        import dash_bootstrap_components as dbc
        import dash_html_components as html

        app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
        alert = dbc.Alert([html.H4('Well done!', className='alert-heading')])
        """)


@importorskip('blspy')
def test_blspy(pyi_builder):
    pyi_builder.test_source("""
        import blspy
        """)


@importorskip('flirpy')
def test_flirpy(pyi_builder):
    pyi_builder.test_source("""
        from flirpy.camera.lepton import Lepton

        print(Lepton.find_video_device())
        """)


@importorskip('office365')
def test_office365(pyi_builder):
    pyi_builder.test_source("""
        from office365.runtime.auth.providers.saml_token_provider import SamlTokenProvider

        SamlTokenProvider._prepare_request_from_template('FederatedSAML.xml', {})
        SamlTokenProvider._prepare_request_from_template('RST2.xml', {})
        SamlTokenProvider._prepare_request_from_template('SAML.xml', {})
        """)


@importorskip('thinc')
def test_thinc(pyi_builder):
    pyi_builder.test_source("""
        from thinc.backends import numpy_ops
        """)


@importorskip('srsly')
def test_srsly(pyi_builder):
    pyi_builder.test_source("""
        import srsly
        """)


@importorskip('spacy')
def test_spacy(pyi_builder):
    pyi_builder.test_source("""
        import spacy
        """)


@importorskip('shotgun_api3')
def test_shotgun_api3(pyi_builder):
    pyi_builder.test_source("""
        import shotgun_api3
        """)


@importorskip('msoffcrypto')
def test_msoffcrypto(pyi_builder):
    pyi_builder.test_source("""
        import msoffcrypto
        """)


@importorskip('mariadb')
def test_mariadb(pyi_builder):
    pyi_builder.test_source("""
        import mariadb
        """)


@importorskip('dash_uploader')
def test_dash_uploader(pyi_builder):
    pyi_builder.test_source("""
        import dash_uploader
        """)


@importorskip('cloudscraper')
def test_cloudscraper(pyi_builder):
    pyi_builder.test_source("""
        import cloudscraper
        scraper = cloudscraper.create_scraper()
        """)


@importorskip('mnemonic')
def test_mnemonic(pyi_builder):
    pyi_builder.test_source("""
        import mnemonic
        mnemonic.Mnemonic("english")
        """)


@importorskip('pynput')
def test_pynput(pyi_builder):
    pyi_builder.test_source("""
        import pynput
        """)


@importorskip('pystray')
def test_pystray(pyi_builder):
    pyi_builder.test_source("""
        import pystray
        """)


@importorskip('rtree')
def test_rtree(pyi_builder):
    pyi_builder.test_source("""
        import rtree
        """)


@importorskip('pingouin')
def test_pingouin(pyi_builder):
    pyi_builder.test_source("""
        import pingouin
        """)


@importorskip('timezonefinder')
def test_timezonefinder(pyi_builder):
    pyi_builder.test_source("""
        from timezonefinder import TimezoneFinder
        TimezoneFinder()
        """)


@importorskip('uvicorn')
def test_uvicorn(pyi_builder):
    pyi_builder.test_source("""
        from uvicorn import lifespan, loops
        """)


@importorskip("langdetect")
def test_langdetect(pyi_builder):
    pyi_builder.test_source("""
        import langdetect
        print(langdetect.detect("this is a test"))
        """)


@importorskip("swagger_spec_validator")
def test_swagger_spec_validator(pyi_builder):
    pyi_builder.test_source("""
        from swagger_spec_validator.common import read_resource_file
        read_resource_file("schemas/v1.2/resourceListing.json")
        read_resource_file("schemas/v2.0/schema.json")
        """)


@requires('pythonnet < 3.dev')
@pytest.mark.skipif(not is_win, reason='pythonnet 2 does not support .Net Core, so its only supported by Windows')
def test_pythonnet2(pyi_builder):
    pyi_builder.test_source("""
        import clr
        """)


@requires('pythonnet >= 3.dev')
def test_pythonnet3(pyi_builder):
    runtime_cfg_path = str((Path(__file__) / '../data/netcore5_runtime_config.json').resolve(strict=True).as_posix())
    pyi_builder.test_source(f"""
        from pathlib import Path
        from clr_loader import get_coreclr
        from pythonnet import set_runtime
        set_runtime(get_coreclr('{runtime_cfg_path}'))

        import clr
        """)


if is_win:
    # This is a hack to prevent monkeypatch from interfering with PyQt5's additional PATH entries. See:
    # https://github.com/pyinstaller/pyinstaller/commit/b66c9021129e9e875ddd138a298ce542483dd6c9
    try:
        import PyQt5  # noqa: F401
    except ImportError:
        pass


@importorskip("qtmodern")
@importorskip("PyQt5")
def test_qtmodern(pyi_builder):
    pyi_builder.test_source("""
        import sys
        from PyQt5 import QtWidgets
        import qtmodern.styles
        import qtmodern.windows

        app = QtWidgets.QApplication(sys.argv)
        window = QtWidgets.QWidget()
        qtmodern.styles.dark(app)
        modern_window = qtmodern.windows.ModernWindow(window)
        modern_window.show()
        """)


@importorskip("platformdirs")
def test_platformdirs(pyi_builder):
    pyi_builder.test_source("""
        import platformdirs
        platformdirs.user_data_dir("FooApp", "Mr Foo")
        """)


@importorskip("websockets")
def test_websockets(pyi_builder):
    pyi_builder.test_source("import websockets")


@importorskip("tableauhyperapi")
def test_tableauhyperapi(pyi_builder):
    pyi_builder.test_source("""
        import tableauhyperapi
        """)


@importorskip("pymssql")
def test_pymssql(pyi_builder):
    pyi_builder.test_source("""
        import pymssql
        """)


@importorskip("branca")
def test_branca(pyi_builder):
    pyi_builder.test_source("""
        import branca
        """)


@importorskip("folium")
def test_folium(pyi_builder):
    pyi_builder.test_source("""
        import folium
        m = folium.Map(location=[0, 0], zoom_start=5)
        """)


@importorskip("metpy")
def test_metpy(pyi_builder):
    # Import metpy.plots, which triggers search for colortables data.
    pyi_builder.test_source("""
        import metpy.plots
        """)


@importorskip("pyvjoy")
def test_pyvjoy(pyi_builder):
    pyi_builder.test_source("""
        import pyvjoy
        """)


@importorskip("adbutils")
def test_adbutils(pyi_builder):
    # adbutils 0.15.0 renamed adbutils._utils.get_adb_exe() to adb_path()
    if is_module_satisfies("adbutils >= 0.15.0"):
        pyi_builder.test_source("""
            from adbutils._utils import adb_path; adb_path()
            """)
    else:
        pyi_builder.test_source("""
            from adbutils._utils import get_adb_exe; get_adb_exe()
            """)


@importorskip("pymediainfo")
def test_pymediainfo(pyi_builder):
    pyi_builder.test_source("""
        from pymediainfo import MediaInfo
        MediaInfo._get_library()  # Trigger search for shared library.
        """)


@importorskip("sacremoses")
def test_sacremoses(pyi_builder):
    pyi_builder.test_source("""
        import sacremoses
        """)


@importorskip("pypeteer")
def test_pypeteer(pyi_builder):
    pyi_builder.test_source("""
        import pypeteer
        print(pypeteer.version)
        """)


@importorskip("tzdata")
@pytest.mark.skipif(not is_py39 and not can_import_module('importlib_resources'),
                    reason='importlib_resources is required on python < 3.9.')
def test_tzdata(pyi_builder):
    pyi_builder.test_source("""
        import tzdata.zoneinfo  # hiddenimport

        try:
            import importlib.resources as importlib_resources
        except ImportError:
            import importlib_resources

        # This emulates time-zone data retrieval from tzdata, as peformed by
        # zoneinfo / backports.zoneinfo
        zone_name = "Europe/Ljubljana"

        components = zone_name.split("/")
        package_name = ".".join(["tzdata.zoneinfo"] + components[:-1])
        resource_name = components[-1]

        with importlib_resources.open_binary(package_name, resource_name) as fp:
            data = fp.read()

        print(data)
        """)


@importorskip("backports.zoneinfo")
@pytest.mark.skipif(is_win and not can_import_module('tzdata'),
                    reason='On Windows, backports.zoneinfo requires tzdata.')
def test_backports_zoneinfo(pyi_builder):
    pyi_builder.test_source("""
        from backports import zoneinfo
        tz = zoneinfo.ZoneInfo("Europe/Ljubljana")
        print(tz)
        """)


@importorskip("zoneinfo")
@pytest.mark.skipif(is_win and not can_import_module('tzdata'),
                    reason='On Windows, zoneinfo requires tzdata.')
def test_zoneinfo(pyi_builder):
    pyi_builder.test_source("""
        import zoneinfo
        tz = zoneinfo.ZoneInfo("Europe/Ljubljana")
        print(tz)
        """)


@importorskip("panel")
def test_panel(pyi_builder):
    pyi_builder.test_source("""
        import panel

        # Load the Ace extension to trigger lazy-loading of model
        panel.extension("ace")
        """)


@importorskip("pyviz_comms")
def test_pyviz_comms(pyi_builder):
    pyi_builder.test_source("""
        import pyviz_comms
        """)


@importorskip("pyphen")
def test_pyphen(pyi_builder):
    pyi_builder.test_source("""
        import pyphen
        """)


@importorskip("pandas")
@importorskip("plotly")
@importorskip("kaleido")
def test_kaleido(pyi_builder):
    pyi_builder.test_source("""
        import plotly.express as px
        fig = px.scatter(px.data.iris(), x="sepal_length", y="sepal_width", color="species")
        fig.write_image("figure.png", engine="kaleido")
        """)


@pytest.mark.skipif(is_win,
                    reason='On Windows, Cairo dependencies cannot be installed using Chocolatey.')
@importorskip("cairocffi")
def test_cairocffi(pyi_builder):
    pyi_builder.test_source("""
        import cairocffi
        """)


@pytest.mark.skipif(is_win,
                    reason='On Windows, Cairo dependencies cannot be installed using Chocolatey.')
@importorskip("cairosvg")
def test_cairosvg(pyi_builder):
    pyi_builder.test_source("""
        import cairosvg
        """)


@importorskip("ffpyplayer")
def test_ffpyplayer(pyi_builder):
    pyi_builder.test_source("""
        import ffpyplayer.player
        """)


@importorskip("cv2")
def test_cv2(pyi_builder):
    pyi_builder.test_source("""
        import cv2
        """)


@importorskip("twisted")
def test_twisted_default_reactor(pyi_builder):
    pyi_builder.test_source("""
        from twisted.internet import reactor
        assert callable(reactor.listenTCP)
        """)


@importorskip("twisted")
def test_twisted_custom_reactor(pyi_builder):
    pyi_builder.test_source("""
        import sys
        if sys.platform.startswith("win") and sys.version_info >= (3,7):
            import asyncio
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        from twisted.internet import asyncioreactor
        asyncioreactor.install()
        from twisted.internet import reactor
        assert callable(reactor.listenTCP)
        """)


@importorskip("pygraphviz")
def test_pygraphviz_bundled_programs(pyi_builder):
    # Test that the frozen application is using collected graphviz executables instead of system-installed ones.
    pyi_builder.test_source("""
        import sys
        import os
        import pygraphviz

        bundle_dir = os.path.normpath(sys._MEIPASS)
        dot_path = os.path.normpath(pygraphviz.AGraph()._get_prog('dot'))

        assert os.path.commonprefix([dot_path, bundle_dir]) == bundle_dir, \
            f"Invalid program path: {dot_path}!"
        """)


@importorskip("pypsexec")
def test_pypsexec(pyi_builder):
    pyi_builder.test_source("""
        from pypsexec.paexec import paexec_out_stream
        next(paexec_out_stream())
        """)


@importorskip("mimesis")
def test_mimesis(pyi_builder):
    pyi_builder.test_source("""
        from mimesis import Address
        Address().address()
        """)


@importorskip('orjson')
def test_orjson(pyi_builder):
    pyi_builder.test_source("""
        import orjson
        """)


@importorskip('altair')
def test_altair(pyi_builder):
    pyi_builder.test_source("""
        import altair
        """)


@importorskip('fabric')
def test_fabric(pyi_builder):
    pyi_builder.test_source("""
        import fabric
        """)


@importorskip('cassandra')
def test_cassandra(pyi_builder):
    pyi_builder.test_source("""
        import cassandra
        """)


@importorskip('gitlab')
def test_gitlab(pyi_builder):
    pyi_builder.test_source("""
        import gitlab
        """)


@importorskip('shapely')
def test_shapely(pyi_builder):
    pyi_builder.test_source("""
        from shapely.geometry import Point
        patch = Point(0.0, 0.0).buffer(10.0)
        print(patch.area)
        """)


@importorskip('lark')
def test_lark(pyi_builder):
    pyi_builder.test_source("""
        import lark
        parser = lark.Lark('''
            value: "true"
            %import common.SIGNED_NUMBER''',
            start='value')
    """)


@importorskip('stdnum')
def test_stdnum_iban(pyi_builder):
    pyi_builder.test_source("""
        import stdnum.iban
    """)


@importorskip('numcodecs')
def test_numcodecs(pyi_builder):
    pyi_builder.test_source("""
        # numcodecs uses multiprocessing
        import multiprocessing
        multiprocessing.freeze_support()
        from numcodecs import Blosc
    """)


@importorskip('pypemicro')
def test_pypemicro(pyi_builder):
    pyi_builder.test_source("""
        from pypemicro import PyPemicro
        assert PyPemicro.get_pemicro_lib()
    """)


@importorskip('sounddevice')
def test_sounddevice(pyi_builder):
    pyi_builder.test_source("""
        import sounddevice
    """)


@importorskip('soundfile')
def test_soundfile(pyi_builder):
    pyi_builder.test_source("""
        import soundfile
    """)


@importorskip('yt_dlp')
def test_yt_dlp(pyi_builder):
    pyi_builder.test_source("""
        import yt_dlp
    """)
