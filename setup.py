import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = []
with open("requirements.txt") as requirements:
    for line in requirements:
        line = line.strip()
        if len(line) == 0:
            continue
        if line[0] == '#':
            continue

        version_pin = line.split()[0]
        install_requires.append(version_pin)

data_files = [('api', ['candig_authz_service/api/api_definition.yaml'])]

setuptools.setup(
    name="candig_authz_service",
    version="0.0.1",
    author="BCGSC",
    author_email="jimli@bcgsc.ca",
    description="Implementation of Authorization Service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    test_suite='tests',
    url="https://github.com/CanDIG/candig_authz_service",
    packages=setuptools.find_packages(),
    include_package_data=True,
    data_files=data_files,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",        
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "candig_authz_service = candig_authz_service.__main__:main",
        ]
    },
)