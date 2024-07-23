from setuptools import setup, find_packages
setup(
    name='codetampermirror',
    version='1.1',
    packages=find_packages(),
    install_requires=[
        #Add dependencies here.
        #'flask<=0.5',
    ],
    entry_points={
        "console_scripts": [
            "codetampermirror = codetampermirror:hello",
        ],
    },
)
