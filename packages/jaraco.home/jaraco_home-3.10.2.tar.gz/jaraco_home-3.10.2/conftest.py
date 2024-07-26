import platform

import pytest
from mockproc import mockprocess

win_ignore = [
    'jaraco/home/hdhomerun.py',
] * (platform.system() == 'Windows')

collect_ignore = [
    'jaraco/home/relay.py',
] + win_ignore


@pytest.fixture(scope='session', autouse=True)
def hdhomerun_config_mocked():
    import jaraco.home.hdhomerun as hd
    from jaraco.home.compat.py38 import resources

    hd.hdhomerun_config = 'hdhomerun_config'
    scripts = mockprocess.MockProc()
    script = (
        resources.files('jaraco.home')
        .joinpath('mock hdhomerun.py')
        .read_text(encoding='utf-8')
    )
    scripts.append('hdhomerun_config', returncode=0, script=script)
    with scripts:
        yield
