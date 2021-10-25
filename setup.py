from setuptools import find_packages, setup


setup(
    name='PyDM',
    version='0.1.0',
    author='wocks1123',
    author_email='wocks1123@gmail.com',
    url='https://github.com/wocks1123/PyDM',
    license='MIT',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.6',
    install_requires=[
        'python-dotenv',
        'pyzmq',
        'zmq==0.0.0'
    ]
)
