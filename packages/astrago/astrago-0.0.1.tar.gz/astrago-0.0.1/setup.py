from setuptools import setup, find_packages

setup(
    name='astrago',
    version='0.0.1',
    description='The Astrago package helps track model training data, allowing you to efficiently collect and manage various metrics and log data generated during the training process.',
    author='hc.park',
    author_email='hc.park@xiilab.com',
    url='https://github.com/xiilab/astrago',
    packages=find_packages(exclude=[]),
    keywords=['astrago','xiilab','uyuni'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
)
