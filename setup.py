from setuptools import find_packages, setup

setup(
    name="fastapi-filter",
    version="0.1.0",
    description="A filter library for FastAPI with SQLAlchemy support.",
    author="Rami Sfari",
    author_email="rami2sfari@gmail.com",
    packages=find_packages(),
    install_requires=["fastapi>=0.100.0", "SQLAlchemy>=2.0.0", "pydantic>=2.0.0"],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: FastAPI",
        "License :: OSI Approved :: MIT License",
    ],
)
