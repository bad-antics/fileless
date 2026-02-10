from setuptools import setup,find_packages
setup(name="fileless",version="2.0.0",author="bad-antics",description="Fileless malware research and detection framework",packages=find_packages(where="src"),package_dir={"":"src"},python_requires=">=3.8")
