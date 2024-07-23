import docker
import os

# Search all images on the Host system for images matching a pattern and copies all files matching pattern 2.
def copy_logs_from_containers(image_name_pattern,
                              file_to_copy_pattern,
                              destination_directory,
                              verbose=False):
    """
    Search for Docker images with a specified pattern, and copy all log files matching a specified pattern from running containers
    to a destination directory on the host.

    :param image_name_pattern: Pattern to match Docker image names (e.g., '_spider')
    :param file_to_copy_pattern: Pattern to match log file names inside the container (e.g., '*.log')
    :param destination_directory: Directory on the host to save the copied files
    """

    try:
        # Get a client relating to the Docker on this host system where this script runs
        client = docker.from_env()

        # Ensure the destination directory exists
        os.makedirs(destination_directory, exist_ok=True)

        # List all images
        images = client.images.list()

        # Filter images with the specified pattern
        matching_images = [image for image in images for tag in image.tags if image_name_pattern in tag]

        # Iterate over every image and get all related containers to the image id
        for image in matching_images:
            # List containers running the current image
            containers = client.containers.list(filters={"ancestor": image.id})

            # Iterate over every container that relates has loaded the image.id
            for container in containers:
                container_id = container.id[:12]  # Get the short container ID

                # Get a list of files in the container's /app/logFile directory
                files_in_container = container.exec_run(['find', '/app/logFile', '-type', 'f']).output.decode('utf-8').splitlines()

                # Iterate over each file in the container's /app/logFile directory
                for file in files_in_container:
                    # Check if the file matches the file pattern
                    filename = os.path.split(file)[1]

                    # Copy the file from the container to the host if it matches target pattern
                    if filename.lower().endswith(file_to_copy_pattern.lower()):

                        # Given a target match file in the target container, attempt to copy to host
                        try:
                            # Read the file content directly from the container
                            file_content = container.exec_run(f'cat {file}').output

                            # Define the destination file path
                            destination_file_path = os.path.join(destination_directory,
                                                                 f"{container_id}_{filename}")

                            # Write the file content to the destination file path
                            with open(destination_file_path, 'wb') as dest_file:
                                dest_file.write(file_content)
                        # If there was a docker APIError, print a warning.
                        except docker.errors.APIError as e:
                            print(f'Could not copy target file, {file}, due to {e}')

                    print(f"Copied log files from container {container_id} to {destination_directory}")
    except Exception as e:
        print('An exception occurred: ')
        print(str(e))

    if verbose:
        try:
            print('The images were: ')
            print(images)
            print('\n')
            print('The images matching the pattern were: ')
            print(matching_images)
            print(f'Last image that matched was {image}...')
            print(f'Last container match had the id {container_id}')
            print('Got the following files in the container: ')
            print(files_in_container)
            print('Found a filename like: ')
            print(filename)
            print(f'Got file content for {file}')
            print(f'Destination file path is like {destination_file_path}')
            print(f'Wrote file, {file}, to destination.')
        except:
            print('Could not print full debug')
            print(str(e))


# If we run this script directly, collect all logs from images that match our patterns.
if __name__ == '__main__':
    # Example usage
    copy_logs_from_containers(
        image_name_pattern='_spider',
        file_to_copy_pattern='log.txt',
        destination_directory='filesFromContainer',
        verbose=True
    )