import setuptools
import md_tangle

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=md_tangle.__title__,
    version=md_tangle.__version__,
    license=md_tangle.__license__,
    author=md_tangle.__author__,
    author_email=md_tangle.__author_email__,
    description="Generates ('tangles') source code from Markdown documents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joakimmj/md-tangle",
    packages=setuptools.find_packages(),
    keywords=['markdown', 'tangle', 'literate programming'],
    platforms=['any'],
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        'Topic :: Text Processing :: Markup',
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3"
    ],
    entry_points={
        'console_scripts': [
            'md-tangle = md_tangle.main:main',
        ]
    },
)
