from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="torchaudio-tnr",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    author="Thunder Compute",
    author_email="support@thundercompute.com",
    description="",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
)