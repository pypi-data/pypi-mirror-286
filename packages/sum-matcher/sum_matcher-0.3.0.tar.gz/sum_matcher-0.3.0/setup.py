from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        name="sum_matcher.sum_matcher",
        sources=["sum_matcher/sum_matcher.pyx"],
    )
]

setup(
    name="sum_matcher",
    version="0.3.0",
    author="zimuzhang",
    author_email="zhang0418zimu@gmail.com",
    description="A library to find matching sum pairs in random numbers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=["sum_matcher"],
    ext_modules=cythonize(extensions),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
