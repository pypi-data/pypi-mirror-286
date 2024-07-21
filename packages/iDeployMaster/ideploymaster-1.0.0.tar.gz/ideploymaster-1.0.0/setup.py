from setuptools import setup

setup(
    name='iDeployMaster',
    version='1.0.0',
    packages=['iDeployMaster'],
    entry_points={
        'console_scripts': [
            'node-selector=iDeployMaster.main:initialize_ui',
        ],
    },
    install_requires=[
        'Pillow',
    ],
    include_package_data=True,
    package_data={
        '': ['*.png'],
    },
    zip_safe=False,
)
