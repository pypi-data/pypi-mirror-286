import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="robot_list",
    version="0.0.6",
    author="Venixa Innovations",
    author_email="venixainnovations@gmail.com",
    description="This is a package which lists the robot framework tests using robot command line arguments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Venixa/robot_list",
    project_urls={
        "Bug Tracker": "https://github.com/Venixa/robot_list/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=['robot framework list', 'list robotframework tests', 'list robot'],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where="src", include=['robot_list']),
    python_requires=">=3.6",
    install_requires=[
        'xmltodict==0.13.0'
    ]
)
