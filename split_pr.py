import subprocess
import sys


def run_command(command, check=True):
    """Run a shell command, capture its output, and return the output."""
    # Add a special case for git checkout to force it
    if command[0] == "git" and command[1] == "checkout":
        command.insert(2, "-f")
    
    print(f"Running: {' '.join(command)}")
    result = subprocess.run(command, text=True, capture_output=True)
    if check and result.returncode != 0:
        print(result.stderr)
        sys.exit(result.returncode)
    return result.stdout.strip()

def create_branches_from_files(main_branch, feature_branch, branch_file_map):
    """Create new branches from files specified in the branch_file_map."""
    run_command(["git", "checkout", main_branch])

    for target_branch_name, file_paths in branch_file_map.items():
        print(f"\n=== Processing branch: {target_branch_name} ===")

        # Create or switch to the target branch
        run_command(["git", "checkout", "-B", target_branch_name, main_branch])

        # Verify branch change
        current_branch = run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        if current_branch != target_branch_name:
            run_command(["git", "checkout", target_branch_name])
        
        print(f"✓ Created and switched to branch: {current_branch}")

        # Merge without committing
        run_command(["git", "merge", "--no-commit", "--no-ff", feature_branch])
        
        # Reset changes
        run_command(["git", "reset"])

        # Add specified files to commit
        for file_path in file_paths:
            run_command(["git", "add", file_path])

        # Commit changes
        commit_message = f"Split changes from {feature_branch} into {target_branch_name}"
        run_command(["git", "commit", "-m", commit_message])

        # Push changes to remote
        run_command(["git", "push", "-u", "origin", target_branch_name])
        print(f"✓ Successfully pushed branch: {target_branch_name}")

if __name__ == "__main__":
    main_branch = "main"
    feature_branch = ""  # Replace with the branch to split
    branch_file_map = {}  # Modify this to match the files you want to split

    create_branches_from_files(main_branch, feature_branch, branch_file_map)
