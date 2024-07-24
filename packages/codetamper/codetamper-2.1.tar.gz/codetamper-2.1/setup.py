from setuptools import setup, find_packages
setup(
    name='codetamper',
    version='2.1',
    packages=find_packages(),
    install_requires=[
        #Add dependencies here.
        #'flask<=0.5',
    ],
    entry_points={
        "console_scripts": [
            "codetamper = codetamper:hello",
        ],
    },
)
