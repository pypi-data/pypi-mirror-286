import setuptools


with open("README.md", "r") as f:
    long_describe = f.read()


with open('requirements.txt') as f:
    required = f.read().splitlines()


packages = setuptools.find_namespace_packages("young_mange_fastapi")
print(packages)
setuptools.setup(
    name="young_manage_fastapi",
    version="0.0.1",
    author="hiyoung",
    author_email="hiyoungliu@gmail.com",
    description="young_manage_fastapi",
    long_description=long_describe,
    long_description_content_type="text/markdown",
    url="https://github.com/hiyoung123",
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    entry_points = {
        "console_scripts":[
            "fastapi = young_manage_fastapi.main:app"
        ]
    },
    install_requires=required,
)