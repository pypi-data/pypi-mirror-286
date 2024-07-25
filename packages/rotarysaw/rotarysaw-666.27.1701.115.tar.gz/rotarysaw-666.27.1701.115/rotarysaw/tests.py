#!/usr/bin/env python3
import pytest

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





