from setuptools import setup, find_packages

setup(
    name="notion-logger",
    version="0.0.7",
    author="_Kamikotto_",
    author_email="kamikotto3@gmail.com",
    description="A small logger for notion.so",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/KamikottoGG/NotionLogger",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "requests",
    ],
    python_requires='>=3.10',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
