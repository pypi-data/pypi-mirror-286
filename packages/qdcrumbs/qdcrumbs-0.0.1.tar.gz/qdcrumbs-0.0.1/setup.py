from setuptools import setup, find_packages

with open("./README.md") as f:
    long_desc = f.read()

setup(
    name='qdcrumbs',
    version='0.0.1',
    description='Easy to use breadcrumbs for webpages using Flask.',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    license="MIT",
    author='etpcdev',
    author_email='etpcdev@gmail.com',
    platforms='any',
    url='https://github.com/etpcdev/QDcrumbs',
    readme="README.md",
    classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
                 ],

    install_requires=['Flask>=3.0.0'],
    python_requires=">=3.8",
)
