from setuptools import setup, find_packages
setup(
    name='tamper02',
    version='3.0',
    packages=find_packages(),
    install_requires=[
        #Add dependencies here.
        #'flask<=0.5',
    ],
    entry_points={
        "console_scripts": [
            "tamper02 = tamper02:hello",
        ],
    },
)