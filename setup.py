from setuptools import setup

setup(
    name="GRRMTools",
    version="0.0.1",
    install_requires=[],
    entry_points={
        'console_scripts': [
            'grrmlist2xyz=GRRMTools.grrmlist2xyz:main',
        ],
    },
    author="Michio Katouda",
    author_email="katouda@rist.or.jp",
    description="Tools for GRRM job anaysis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT",
    ],
    python_requires='>=3.7',
)
