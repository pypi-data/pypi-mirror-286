from setuptools import setup, find_packages

setup(
    name="tar_paint",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "tkinter",
    ],
    entry_points={
        "console_scripts": [
            "tar_paint=tar_paint.main:main",
        ],
    },
    author="Your Name",
    author_email="jaroenpronprasit@gmail.com",
    description="tar paint application",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/natthphong/tar_pain",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
