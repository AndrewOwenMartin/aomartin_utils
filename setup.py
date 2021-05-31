from setuptools import setup

setup(
    name="aomartin_utils",
    version="0.3.0",
    packages=[
        "aomartin_utils",
    ],
    description="Useful scripts to add to your path",
    keywords=["utils", "shell"],
    entry_points={
        "console_scripts": [
            "my-latexmk = aomartin_utils.utils:my_latexmk_main",
            "create-python-app = aomartin_utils.create_py_app:create_py_app_main",
            "csv2sqlite = aomartin_utils.csv2sqlite:csv2sqlite_main",
            "frobnicate-spreadsheet = aomartin_utils.frobnicate:frobnicate_main",
        ],
    },
    install_requires=[
        "openpyxl",
        "pandas",
    ],
    dependencies=[
        "latexmk", # for my-latexmk
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
    ],
    author="Andrew Owen Martin",
    author_email="andrew@aomartin.co.uk",
)
