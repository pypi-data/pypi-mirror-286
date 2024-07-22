import setuptools

setuptools.setup(
    name="MPYdata",
    version="1.1.0",
    author="Mahendra Sai Phaneeswar Yerramsetti",
    author_email="mahendrayerramsetti@gmail.com",
    description="""A Python Package for saving data in database.""",
    url="https://github.com/MahendraYerramsetti/PYdata",
    project_description="""A Python Package for saving data in database.
    it uses simple syntaxes to perform advanced queries in python.
    To use this package, simply import it, to kow how to use it please 
    visit https://github.com/MahendraYerramsetti/PYdata.
    where you could know about codes and more.""",
    project_urls={
        "Bug Tracker": "https://github.com/MahendraYerramsetti/PYdata/issues",
    },
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)