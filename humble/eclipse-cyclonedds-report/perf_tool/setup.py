
from setuptools import setup


setup(
    name='ros-dds-performance',
    version='0.0.1',
    description='Tools to run and analyze ROS2 performance tests',
    author='Eclipse Cyclone DDS Committers',
    maintainer='Thijs Miedema',
    maintainer_email='thijs.miedema@adlinktech.com',
    url="https://cyclonedds.io",
    project_urls={
        "Source Code": "https://github.com/eclipse-cyclonedds/ros-dds-performance"
    },
    license="EPL-2.0, BSD-3-Clause",
    platforms=["Windows", "Linux", "Mac OS-X", "Unix"],
    keywords=[
        "eclipse", "cyclone", "dds", "pub", "sub",
        "pubsub", "iot", "cyclonedds", "cdr", "omg",
        "idl", "middleware", "ros", "ros2", "performance"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=['perf_tool'],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'perf_tool=perf_tool:main'
        ]
    },
    install_requires=[
        "numpy",
        "matplotlib"
    ],
    zip_safe=False
)
