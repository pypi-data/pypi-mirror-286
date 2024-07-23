from setuptools import setup, find_packages

setup(
    name="pySQLExport",
    version="0.1.2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "mysql-connector-python",
        "pyyaml"
    ],
    entry_points={
        "console_scripts": [
            "pySQLExport=pySQLExport.__main__:main"
        ]
    },
    author="Aaron Mathis",
    author_email="aaron.mathis@gmail.com",
    description="A command line tool to interact with MySQL databases and export to other formats.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/aaronlmathis/pySQLExport",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
