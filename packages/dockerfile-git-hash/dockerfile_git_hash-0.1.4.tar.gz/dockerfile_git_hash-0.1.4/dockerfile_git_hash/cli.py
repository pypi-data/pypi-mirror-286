import argparse
import re
import subprocess
from pathlib import Path
import shutil

def extract_repo_url(git_command):
    match = re.search(r'git clone.*?(https?://.*?)\.git', git_command)
    return f"{match.group(1)}.git" if match else None

def parse_dockerfile(dockerfile_path):
    with open(dockerfile_path, 'r') as f:
        content = f.read()

    pattern = r'git clone.*?git checkout FETCH_HEAD'
    matches = re.findall(pattern, content, re.DOTALL)
    return matches

def get_latest_commit(repo_url, branch=None):
    # Remove the hash from the repo_url
    cmd = ['git', 'ls-remote', repo_url]
    if branch:
        cmd.append(branch)
    else:
        cmd.append('HEAD')

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Failed to get latest commit: {result.stderr}")

    lines = result.stdout.strip().split('\n')
    if not lines:
        raise Exception("No output from git ls-remote command")
    commit_hash = lines[0].split()[0]
    return commit_hash

def update_dockerfile(dockerfile_path, dest_dir):
    with open(dockerfile_path, 'r') as f:
        content = f.read()

    git_commands = parse_dockerfile(dockerfile_path)

    for git_command in git_commands:
        repo_url = extract_repo_url(git_command)
        print(f"Checking repository: {repo_url}")

        branch_match = re.search(r'git clone\s+(?:-b\s+(\S+))?\s+', git_command)
        branch = branch_match.group(1) if branch_match and branch_match.group(1) else None

        new_commit = get_latest_commit(repo_url, branch)
        old_fetch = re.search(r'git fetch.*?origin\s+(\w+)', git_command).group(1)

        if old_fetch != new_commit:
            print(f"Version hash changed for {repo_url}: {old_fetch} -> {new_commit}")
            content = content.replace(old_fetch, new_commit)

    dest_dir.mkdir(parents=True, exist_ok=True)
    with open(dest_dir / "Dockerfile", 'w') as f:
        f.write(content)

def copy_additional_files(src_dir, dest_dir):
    additional_files = ['run.sh', 'run.bat', 'build.sh', 'build.bat', 'docker-compose.yml']
    for file in additional_files:
        src_file = src_dir / file
        if src_file.exists():
            shutil.copy2(src_file, dest_dir)

def main():
    parser = argparse.ArgumentParser(description="Update commit hashes in a Dockerfile")
    parser.add_argument("dockerfile", help="Path to the Dockerfile or directory containing the Dockerfile")
    parser.add_argument("destination", help="Destination directory for the updated Dockerfile and additional files")

    args = parser.parse_args()

    dockerfile_path = Path(args.dockerfile)
    if dockerfile_path.is_dir():
        dockerfile_path = dockerfile_path / "Dockerfile"

    if not dockerfile_path.exists():
        raise FileNotFoundError(f"Dockerfile not found at {dockerfile_path}")

    dest_dir = Path(args.destination)

    update_dockerfile(dockerfile_path, dest_dir)
    copy_additional_files(dockerfile_path.parent, dest_dir)

    print(f"Updated Dockerfile written to {dest_dir / 'Dockerfile'}")

if __name__ == "__main__":
    main()
