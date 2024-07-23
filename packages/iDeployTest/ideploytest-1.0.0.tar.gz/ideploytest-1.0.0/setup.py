from setuptools import setup

setup(
    name='iDeployTest',
    version='1.0.0',
    packages=['iDeployTest'],
    entry_points={
        'console_scripts': [
            'iDeployTest=iDeployTest.main:initialize_ui',
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
