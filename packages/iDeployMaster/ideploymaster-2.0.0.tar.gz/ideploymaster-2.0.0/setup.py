from setuptools import setup

setup(
    name='iDeployMaster',
    version='2.0.0',
    packages=['iDeployMaster'],
    entry_points={
        'console_scripts': [
            'iDeployMaster=iDeployMaster.main:initialize_ui',
        ],
    },
    install_requires=[
        'Pillow',
        'requests',
    ],
    include_package_data=True,
    package_data={
        '': ['*.png'],
    },
    zip_safe=False,
)
