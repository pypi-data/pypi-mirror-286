import setuptools
import os

own_dir = os.path.dirname(__file__)


def version():
    with open(os.path.join('version')) as f:
        return f.read()


setuptools.setup(
    name='digistore24-client',
    version=version(),
    descriptions='an API client for API exposed by digistore24.com',
    python_requires='>=3.11',
    packages=('digistore',),
    install_request=(
        'dacite',
        'requests',
    ),
)
