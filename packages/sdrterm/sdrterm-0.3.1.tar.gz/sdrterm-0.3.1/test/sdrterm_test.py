import os
import socket
import time
from multiprocessing import Value
from os import getpid
from threading import Thread

import pytest

import sdrterm
from misc.general_util import shutdownSocket, findPort
from misc.io_args_test import throwingFiles

@pytest.mark.slow
def test_main():
    sdrterm.__setStartMethod()
    VFOS = '15000,-60000'
    # FILE_NAME = '../SDRSharp_20160101_231914Z_12kHz_IQ.wav'
    FILE_NAME = os.path.join('..', 'SDRSharp_20160101_231914Z_12kHz_IQ.wav')
    UINT8_FILE_NAME = os.path.join(*(('/mnt', 'd', 'uint8.wav') if 'posix' in os.name else ('d:', 'uint8.wav')))
    isDead = sdrterm.isDead = Value('b', 0)
    sdrterm.__deletePidFile = sdrterm.__generatePidFile(getpid())

    import importlib.resources as rscs
    ogFiles = rscs.files
    rscs.files = throwingFiles
    sdrterm.main(inFile=FILE_NAME,
                 outFile='/dev/null',
                 correct_iq=True,
                 plot='ps',
                 omegaOut=5000, verbose=1)
    rscs.files = ogFiles
    sdrterm.main(inFile=FILE_NAME,
                 outFile='/dev/null',
                 normalize_input=True,
                 omegaOut=5000, verbose=2)
    sdrterm.main(demod=sdrterm.DemodulationChoices.AM,
                 inFile=FILE_NAME,
                 outFile='/dev/null',
                 normalize_input=True,
                 omegaOut=5000)
    sdrterm.main(demod=sdrterm.DemodulationChoices.REAL,
                 inFile=FILE_NAME,
                 outFile='/dev/null',
                 normalize_input=True,
                 omegaOut=5000)
    sdrterm.main(demod=sdrterm.DemodulationChoices.IMAG,
                 inFile=FILE_NAME,
                 outFile='/dev/null',
                 normalize_input=True,
                 swap_input_endianness=True,
                 omegaOut=5000)
    sdrterm.main(inFile=FILE_NAME,
                 outFile='/dev/null',
                 omegaOut=5000,
                 plot='ps,water,vfo')
    sdrterm.main(demod='p008',
                 inFile=FILE_NAME,
                 outFile='/dev/null',
                 omegaOut=5000,
                 tuned=155685000,
                 center=-350000,
                 vfos='15000,-60000',
                 plot='ps,water,vfo')
    sdrterm.main(inFile=FILE_NAME,
                 outFile='/dev/null',
                 omegaOut=5000,
                 tuned=155685000,
                 center=-350000,
                 vfos='15000,-60000',
                 plot='p008')

    thread = Thread(target=sdrterm.main, kwargs={
        'inFile': 'slowboi.local:1234',
        'fs': 1024000,
        'enc': 'B',
        'outFile': '/dev/null',
        'omegaOut': 5000,
        'tuned': 155685000,
        'center': -87500,
        'vfos': VFOS,
        'plot': 'ps,water,vfo'
    })
    thread.start()
    time.sleep(10)
    isDead.value = 1
    thread.join()
    del thread

    isDead.value = 0
    sdrterm.__deletePidFile = sdrterm.__generatePidFile(getpid())
    port = findPort('localhost')
    thread = Thread(target=sdrterm.main,
                    kwargs={'simo': True,
                            'vfo_host': 'localhost:' + str(port),
                            'inFile': UINT8_FILE_NAME,
                            'outFile': '/dev/null',
                            'omegaOut': 5000,
                            'tuned': 155685000,
                            'center': -350000,
                            'vfos': VFOS,
                            })

    thread.start()
    time.sleep(2)

    socks = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(len(VFOS.split(',')) + 1)]

    for sock in socks:
        if 'posix' not in os.name:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        else:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        sock.settimeout(1)
        sock.connect(('localhost', port))

        def func():
            try:
                with sock.makefile('rb') as f:
                    f.read()
            # except (OSError, socket.gaierror) as e:
            #     print(f'Socket caught: {e}')
            # except BaseException as e:
            #     printException(e)
            finally:
                shutdownSocket(sock)
                sock.close()

        Thread(target=func, daemon=True).start()

    # sdrterm.isDead.value = 1
    thread.join()
    for sock in socks:
        shutdownSocket(sock)
        sock.close()
    del thread
