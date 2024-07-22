from setuptools import setup, find_packages

setup(
    name="files_flattener",
    version="0.1.2",
    packages=find_packages(),
    install_requires=["pathspec", "colorlog"],
    entry_points={
        "console_scripts": [
            "flt = files_flattener.cli:main",
        ],
    },
    author="sweetbrulee",
    author_email="sparrowking002@gmail.com",
    description="Use files-flattener to flatten your whole structured code project into a single file.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sweetbrulee/files-flattener",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
