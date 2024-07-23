from setuptools import setup

setup(
    name="dracula-metadata-updater",
    version="1.0",
    py_modules=["dracula.py"],
    install_requires=[
        "mutagen",
    ],
    entry_points={
        'console_scripts':[
            'dracula_=dracula:main',
        ],
    },
    author="Hankan1918",
    description="A script to update metadata of 뮤지컬 드라큘라(Dracula) OST 〈10TH ANNIVERSARY CAST RECORDING〉",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)