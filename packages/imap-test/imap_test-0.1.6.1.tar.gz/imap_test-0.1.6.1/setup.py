import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="imap_test",
    version="0.1.6.1",
    author="JunhaoChen",
    author_email="609752056@qq.com",
    description="Apollo map and Opendrive map converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jh271441/imap_test",
    project_urls={
        "Bug Tracker": "https://github.com/Jh271441/imap_test/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    install_requires=[
        'protobuf<=3.19.4',
        'matplotlib',
        'pyproj',
        # 'record_msg<=0.1.1',
    ],
    entry_points={
        'console_scripts': [
            'imap = imap.main:main',
        ],
    },
    python_requires=">=3.6",
)