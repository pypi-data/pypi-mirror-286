import importlib as il
import logging as log
import subprocess as sp
import sys


class PIPFailed(Exception):
    pass

def pip_install(package):
    if isinstance(package, str):
        try:
            if package.index(','):
                package = [x.strip() for x in package.split(',') if x != '']
        except ValueError:
            pass

    if isinstance(package, str):
        package = [package]

    if not isinstance(package, list):
        log.error(f"Pip install is getting fed whatever '{package}'")
        raise AssertionError()

    log.info(f"Pip requested to install: {', '.join(package)}")
    ro = sp.run(["pip", "install"]+package, shell=False, capture_output=True)
    if ro.returncode != 0:
        log.error(f"{package} install failed, code {ro.returncode}")
        errstring = ''
        for x in ro.stderr.split('\n'):
            log.error(x.strip())
        raise PIPFailed(f"PIP run returncode {ro.returncode} : '" + ro.stderr + "'")
    else:
        log.info(f"PIP Install {package} was successful.")

def import_or_install(modname, package=None):
    if package is None:
        package = modname

    try:
        mod = il.import_module(modname)
        globals()[modname] = mod
        il.invalidate_caches()
        return
    except ModuleNotFoundError:
        pip_install(package)

    try:
        mod = il.import_module(modname)
        globals()[modname] = mod
    except ModuleNotFoundError:
        log.error(f"{package} is still missing.")
        raise FileNotFoundError(f"{modname} is missing after install")

    log.info(f"{modname} can now be imported")




