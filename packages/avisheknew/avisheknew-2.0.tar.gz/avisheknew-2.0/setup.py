from setuptools import setup, find_packages
setup(
    name='avisheknew',
    version='2.0',
    packages=find_packages(),
    install_requires=[
        #Add dependencies here.
        #'flask<=0.5',
    ],
    entry_points={
        "console_scripts": [
            "avisheknew = avisheknew:hello",
        ],
    },
)
