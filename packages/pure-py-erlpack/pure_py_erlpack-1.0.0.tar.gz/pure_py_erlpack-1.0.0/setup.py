from setuptools import setup

setup(
    name='pure_py_erlpack',
    version='1.0.0',
    author='Jake Heinz',
    author_email='jh@discordapp.com',
    url="http://github.com/discord/erlpack",
    description='A erlang term encoder for Python.',
    license='Apache 2.0',
    zip_safe=False,
    package_dir={'': 'py'},
    packages=['erlpack'],
    install_requires=['six~=1.15'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
