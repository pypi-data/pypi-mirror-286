from setuptools import setup, find_packages

setup(
    name="dockerfile-git-hash",
    version="0.1.3",
    packages=find_packages(include=['dockerfile_git_hash']),
    install_requires=[
        # Add any dependencies here
    ],
    entry_points={
        'console_scripts': [
            'dockerfile-git-hash=dockerfile_git_hash:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords='requirements version pip',
    python_requires='>=3.6',
)
