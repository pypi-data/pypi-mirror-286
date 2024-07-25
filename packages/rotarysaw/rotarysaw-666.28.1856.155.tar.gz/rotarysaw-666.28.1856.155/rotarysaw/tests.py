#!/usr/bin/env python3
import sys

import pytest
import logging as log
import basic

from basic import *
log.getLogger().setLevel(log.DEBUG)

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
        import io
        sys.stderr = io.StringIO()
        # Setting because using it for sensing binary mode.
        sys.stderr.mode = 'w'

        log_trace(stderr=True)

        assert len(sys.stderr.getvalue())>50
        assert 'pytest' in sys.stderr.getvalue()

        sys.stderr = backup
        del backup

    def test_sigint_handler(self):

        install_log_trace()
        assert(log_trace.count > 4)

        if sys.platform != 'win32':
            from signal import SIGINT
            os.kill(os.getpid(), SIGINT)
        else:
            pytest.skip("Cannot sigint on windows")

    def test_keyboard_interrupt(self):
        with pytest.raises(KeyboardInterrupt):
            sigint_handler()
            sigint_handler()
            sigint_handler()
            sigint_handler()
            sigint_handler()

    def test_debug_mode(self):
        f = open('debug', 'w')
        f.write('moi')
        f.close()
        backup = basic.jump
        success = False

        def newjump(*arg):
            nonlocal success
            success = True

        basic.jump = newjump

        sigint_handler()
        os.unlink('debug')
        assert success

        basic.jump = backup






