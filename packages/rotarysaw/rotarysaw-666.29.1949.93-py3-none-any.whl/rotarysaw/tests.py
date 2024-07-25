#!/usr/bin/env python3
import sys
import io

import pytest
import pytest_mock
import logging as log
import basic

from basic import *

class TestSimples():
    def test_file_datum(self):
        a = file_datum()
        log.info(a)
        b = from_datum(a)
        assert isinstance(b, datetime)
        assert str(datetime.now().year) in a
        assert isinstance(a, str)

        dt = datetime.now()-timedelta(days=123)
        a = file_datum(t=dt, accuracy=True)
        log.info(a)
        b = from_datum(a)
        assert isinstance(b, datetime)
        assert isinstance(a, str)
        assert str(datetime.now().year) in a
        assert dt == b

    def test_force(self):
        td = 'testdir'
        if os.path.exists('testdir'):
            if os.path.isfile(td):
                os.unlink(td)
            else:
                os.rmdir('testdir')

        force_mkdir('testdir')
        assert os.path.exists('testdir')
        os.rmdir('testdir')

        open('testdir','w').write('moi')

        with pytest.raises(FileExistsError):
            force_mkdir('testdir',critical=True)

    def test_hostname(self):
        hname = hostname()
        assert isinstance(hname, str)
        assert len(hname) > 0
        assert hname in ['F','opal','turrican','turrican.q.uraanikaivos.com','alex','alexlinux']

    def test_log_trace(self):
        log_trace()

        backup = sys.stderr
        sys.stderr = io.StringIO()
        # Setting because using it for sensing binary mode.
        sys.stderr.mode = 'w'

        log_trace(stderr=True)

        assert len(sys.stderr.getvalue())>50
        assert 'pytest' in sys.stderr.getvalue()

        sys.stderr = backup
        del backup

    def test_sigint_handler(self):

        unlink_if_exists('debug')
        install_log_trace()
        assert(log_trace.count > 4)

        if sys.platform != 'win32':
            from signal import SIGINT
            os.kill(os.getpid(), SIGINT)
        else:
            pytest.skip("Cannot sigint on windows")

    def test_keyboard_interrupt(self):
        unlink_if_exists('debug')
        with pytest.raises(KeyboardInterrupt):
            sigint_handler()
            sigint_handler()
            sigint_handler()
            sigint_handler()
            sigint_handler()

    def test_debug_mode(self, mocker):

        f = open('debug', 'w')
        f.write('moi')
        f.close()

        import pdb
        success = False

        def kraut(*argk):
            nonlocal success
            success = True

        backup = sys.stderr
        sys.stderr = io.StringIO()
        # Setting because using it for sensing binary mode.
        sys.stderr.mode = 'w'

        log_trace(stderr=True)

        assert len(sys.stderr.getvalue()) > 50
        assert 'pytest' in sys.stderr.getvalue()

        st = pdb.set_trace
        pdb.set_trace = kraut
        sigint_handler()
        pdb.set_trace = st

        assert success

        unlink_if_exists('debug')

    def test_chdirabs(self):
        kraut = '/humprcpahrueheoaua/e/ua/oeu/oa/ue/oaue/uuuu'.replace('/',os.sep)
        kraut2 = '/humprcpahrueheoaua/e/ua/oeu/oa/ue/oaue'.replace('/',os.sep)

        assert absdirname(kraut).replace('C:','') == kraut2

        old = os.getcwd()
        r = chdirabsdirname()
        assert r == os.getcwd()
        assert os.getcwd() == absdirname(__file__)
        assert os.getcwd() == old


