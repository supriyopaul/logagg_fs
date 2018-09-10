from setuptools import setup
from setuptools import find_packages

setup(
    name="logagg_fs",
    version="0.0.1",
    description="fuse file system for capturing logs",
    keywords="logagg",
    author="Deep Compute, LLC",
    author_email="contact@deepcompute.com",
    url="https://github.com/deep-compute/logagg",
    license='MIT',
    install_requires=[
        "basescript==0.2.6",
        "deeputil==0.2.5",
	"fuse-python==0.3.1"
    ],
    package_dir={'logagg_fs': 'logagg_fs'},
    packages=find_packages('.'),
    include_package_data=True,
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        "console_scripts": [
            "logagg-fs = logagg_fs:main",
        ]
    }
)

