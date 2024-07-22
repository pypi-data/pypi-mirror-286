# dockerfile-git-hash

dockerfile-git-hash is a command-line tool to update the commit hashes in a Dockerfile. It parses the Dockerfile for git checkouts, fetches the latest commit hashes for the repositories, and updates the Dockerfile accordingly.

## Installation

You can install dockerfile-git-hash using pip:

```
pip install dockerfile-git-hash
```

## Usage

```
dockerfile-git-hash <dockerfile_path> <destination_path>
```

- `<dockerfile_path>`: Path to the Dockerfile or directory containing the Dockerfile
- `<destination_path>`: Destination path for the updated Dockerfile

If a directory is provided instead of a Dockerfile, dockerfile-git-hash will look for a file named "Dockerfile" in that directory.

## Features

1. Parses Dockerfiles for git checkouts
2. Fetches the latest commit hash for each repository
3. Updates the Dockerfile with the new commit hashes
4. Writes the updated Dockerfile to the specified destination
5. Copies additional files (run.sh, run.bat, build.sh, build.bat, docker-compose.yaml) if present

## Example

```
dockerfile-git-hash ./my_project/Dockerfile ./updated_dockerfile/Dockerfile
```

This command will update the Dockerfile in the `my_project` directory and save the updated version in the `updated_dockerfile` directory.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Releasing on PyPI

To release a new version of dockerfile-git-hash on PyPI, follow these steps:

1. Update the version number in `setup.py`.
2. Create a new tag with the version number:
   ```
   git tag v<version_number>
   git push origin v<version_number>
   ```
3. Build the distribution packages:
   ```
   python setup.py sdist
   ```
4. Upload the packages to PyPI:
   ```
   twine upload dist/*
   ```

Make sure you have `twine` installed (`pip install twine`) and that you have the necessary credentials to upload to PyPI.
