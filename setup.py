from setuptools import setup, find_packages

setup(
    name="inextremis",
    version="0.0.0",
    author="Paul Sembereka",
    author_email="psemberekajr@gmail.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    license="MIT",
    scripts=["src/__init__.py"],
    entry_points={
        'console_scripts': [
            'start=__init__.py',
        ]
    },
    data_files=[('assets', ['assets/song.wav', 'assets/song.mp3'])],
    python_requires=">=3.6"
)