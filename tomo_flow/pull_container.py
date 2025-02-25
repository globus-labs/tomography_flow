def ensure_container_latest(container_url: str, runtime: str) -> dict:
    """
    Ensure the latest version of a container is available locally. 
    If the container is missing or outdated, pull the latest version.

    Supported Runtimes:
    - Docker (`docker://`)
    - Podman (`docker://`)
    - Singularity (`https://`, `shub://`, `library://`)
    - OCI registries (`oras://`)

    Parameters:
    - container_url (str): The identifier or URL of the container.
    - runtime (str): The container runtime ('docker', 'podman', 'singularity', or 'oras').

    Returns:
    - dict: Contains status information about the container.
    """
    import subprocess
    import requests

    valid_runtimes = ["singularity", "docker", "podman", "oras"]
    if runtime not in valid_runtimes:
        return {"error": f"Unsupported runtime. Choose from {valid_runtimes}."}

    # Validate HTTP-based container URLs
    if container_url.startswith(("http", "https")):
        try:
            response = requests.head(container_url, timeout=10)
            if response.status_code != 200:
                return {"error": f"Invalid container URL: {container_url} (HTTP {response.status_code})"}
        except requests.RequestException as e:
            return {"error": f"Failed to verify container URL: {str(e)}"}

    try:
        if runtime in ["docker", "podman"]:
            cli = "podman" if runtime == "podman" else "docker"
            image_name = container_url.split("docker://")[-1]

            # Check if image exists locally
            check_cmd = [cli, "images", "-q", image_name]
            local_image = subprocess.run(check_cmd, capture_output=True, text=True).stdout.strip()

            if local_image:
                # Pull latest image
                pull_cmd = [cli, "pull", image_name]
                pull_result = subprocess.run(pull_cmd, capture_output=True, text=True)

                # Check if the image was updated
                new_image = subprocess.run(check_cmd, capture_output=True, text=True).stdout.strip()
                if new_image == local_image:
                    return {"status": "Container is already up to date."}
                else:
                    return {"status": "Updated to latest version.", "stdout": pull_result.stdout, "stderr": pull_result.stderr}
            else:
                # Pull if the image is missing
                pull_cmd = [cli, "pull", image_name]
                pull_result = subprocess.run(pull_cmd, capture_output=True, text=True)
                return {"status": "Container pulled successfully.", "stdout": pull_result.stdout, "stderr": pull_result.stderr}

        elif runtime == "singularity":
            image_filename = container_url.split("/")[-1]
            local_path = f"{image_filename}.sif"

            # Check if image exists locally
            check_cmd = ["singularity", "inspect", local_path]
            local_exists = subprocess.run(check_cmd, capture_output=True, text=True).returncode == 0

            if local_exists:
                # Force-pull to update
                pull_cmd = ["singularity", "pull", "--force", local_path, container_url]
                pull_result = subprocess.run(pull_cmd, capture_output=True, text=True)
                return {"status": "Updated to latest version.", "stdout": pull_result.stdout, "stderr": pull_result.stderr}
            else:
                # Pull if missing
                pull_cmd = ["singularity", "pull", local_path, container_url]
                pull_result = subprocess.run(pull_cmd, capture_output=True, text=True)
                return {"status": "Container pulled successfully.", "stdout": pull_result.stdout, "stderr": pull_result.stderr}

        elif runtime == "oras":
            image_name = container_url.split("oras://")[-1]

            # Check if the OCI image exists locally
            check_cmd = ["oras", "discover", image_name]
            local_exists = subprocess.run(check_cmd, capture_output=True, text=True).returncode == 0

            if local_exists:
                # Attempt to pull and update
                pull_cmd = ["oras", "pull", image_name]
                pull_result = subprocess.run(pull_cmd, capture_output=True, text=True)
                return {"status": "Updated OCI container to latest version.", "stdout": pull_result.stdout, "stderr": pull_result.stderr}
            else:
                # Pull if missing
                pull_cmd = ["oras", "pull", image_name]
                pull_result = subprocess.run(pull_cmd, capture_output=True, text=True)
                return {"status": "OCI container pulled successfully.", "stdout": pull_result.stdout, "stderr": pull_result.stderr}

    except Exception as e:
        return {"error": str(e)}
