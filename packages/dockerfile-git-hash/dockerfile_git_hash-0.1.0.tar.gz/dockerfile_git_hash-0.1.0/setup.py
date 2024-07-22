from setuptools import setup, find_packages

setup(
    name="dockerfile-git-hash",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Add any dependencies here
    ],
    entry_points={
        'console_scripts': [
            'dockerfile-git-hash=dockerfile_git_hash.dockerfile_git_hash:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to update commit hashes in Dockerfiles",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Ralf12358/dockerfile-git-hash",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
