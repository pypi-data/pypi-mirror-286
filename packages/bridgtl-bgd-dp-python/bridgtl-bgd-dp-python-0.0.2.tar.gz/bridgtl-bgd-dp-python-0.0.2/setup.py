from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Bank Raya Indonesia - Big Data Python Package'
LONG_DESCRIPTION = DESCRIPTION

setup(
    name="bridgtl-bgd-dp-python",
    version=VERSION,
    author="Dafa Wiratama",
    author_email="dafa.wiratama@bankraya.co.id",
    maintainer="Dafa Wiratama",
    maintainer_email="dafa.wiratama@bankraya.co.id",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    extras_require={
        "spark": [
            "pyspark==3.5.1",
            # Add any other dependencies for Spark extension here
        ],
    },
)
