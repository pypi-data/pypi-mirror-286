from setuptools import setup


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pythonasm',
    version='0.0.2',
    description='A Python library for ASM',
    author='linhhanpy',
    author_email='lhh_88888888@qq.com',
    packages=['pythonasm'],

    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/linhhpy/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

)