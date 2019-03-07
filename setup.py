import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

__general_setup = dict(
    version='0.0.9',
    author="Joakim Myrvoll Johansen",
    author_email="joakimmyrvoll@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joakimmj/md_tangle",
    packages=setuptools.find_packages(),
)

__general_classifiers = [
    "Environment :: Console",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Natural Language :: English"
]

setup_v3 = dict(
    name='md-tangle',
    scripts=['src/py3/md-tangle'],
    description="Generates ('tangles') source code from Markdown documents",
    **__general_setup,
    classifiers=[
        "Programming Language :: Python :: 3",
        *__general_classifiers
    ]
)

setup_v2 = dict(
    name='md-tangle2',
    scripts=['src/py2/md-tangle2'],
    description="Generates ('tangles') source code from Markdown documents (python2)",
    **__general_setup,
    classifiers=[
        "Programming Language :: Python :: 2",
        *__general_classifiers
    ]
)

setuptools.setup(**setup_v3)
setuptools.setup(**setup_v2)
