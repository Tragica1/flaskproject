from setuptools import setup, find_packages
from sphinx.setup_command import BuildDoc

cmdclass = {'build_sphinx': BuildDoc}

name = 'kuxny'
version = '1.0'
release = '1.3.0'

setup(
    name=name,
    author='Maxim Odinokov, Danil Egorkin, Georgy Samonin',
    version=release,
    description='KUXNY',
    packages=find_packages(),
    scripts=['kuxny/app.py', 'kuxny/models.py', 'kuxny/config.py'],
    cmdclass=cmdclass,
    package_data={
        name: ['kuxny/static/images']
    },
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', release),
            'source_dir': ('setup.py', './source')}},
)