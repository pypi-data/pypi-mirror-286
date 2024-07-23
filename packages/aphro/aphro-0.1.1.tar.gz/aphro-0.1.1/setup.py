from setuptools import setup, find_packages

setup(
    name="aphro",
    version="0.1.1",
    author="Abhishek Saini",
    author_email="abhisaini880@gmail.com",
    description="Python scripting framework for building complex pipelines",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/abhisaini880/Aphro.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        # Add any dependencies your package needs here
        # 'requests>=2.20.0',
    ],
    entry_points={
        "console_scripts": [
            # Define command-line scripts here
            # 'spy-monitor=spy.module:function',
        ],
    },
)
