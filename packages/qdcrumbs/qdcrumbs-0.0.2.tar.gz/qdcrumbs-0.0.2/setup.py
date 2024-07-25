from setuptools import setup, find_packages

with open("./README.md") as f:
    long_desc = f.read()

with open("./CHANGELOG.md") as f:
    change_log = f.read()

with open("./version.txt") as f:
    version = f.read()

setup(
    name='qdcrumbs',
    version=version,
    description='Easy to use breadcrumbs for webpages using Flask.',
    long_description=long_desc + "\n" + change_log,
    long_description_content_type="text/markdown",
    license="MIT",
    author='etpcdev',
    author_email='etpcdev@gmail.com',
    platforms='any',
    url='https://github.com/etpcdev/QDcrumbs',
    classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
                 ],

    install_requires=['Flask>=3.0.0'],
    python_requires=">=3.8",
)
