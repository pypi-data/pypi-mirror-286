import os

def renameFiles(directoryPath, # Path to the target directory containing the files.
                additionalText, # Additional text to append to the filename.
                prefix='', # Empty string that is a placeholder for a user supplied prefix to the filename.
                fileKind='Video', # Default assumption about the video type.
                verbose=False # Whether to print names and types. Off by default.
                ):

    count = 1

    # Loop through all files in the directory
    for filename in os.listdir(directoryPath):

        # Get the file extension
        original_file_name = os.path.splitext(filename)[0]
        file_extension = os.path.splitext(filename)[1]
        # Print of filetype
        if verbose:
            print('The file extension was:')
            print(file_extension)

        # Create the new file name with the incremented count
        new_filename = f"{prefix}{original_file_name} - {additionalText} - {fileKind} {count}{file_extension}"
        # Print of entire proposed new name
        if verbose:
            print('The proposed entire new name is:')
            print(new_filename)

        # Replace the original file name with the new one
        os.rename(os.path.join(directoryPath, filename), os.path.join(directoryPath, new_filename))

        # Increment the count
        count = count + 1


# If we run this script, we'll add additionalText + " - Video n" for every video in the video folder.
if __name__ == '__main__':

    directoryPath = r'C:\Users\lukep\OneDrive\Personal\Photo Folder\SortBox\Maidstone Mycology'
    additionalText = 'Maidstone Mycology Adventures'
    prefix = 'Luke Pollen Nature Walks - '
    renameFiles(directoryPath, additionalText, prefix=prefix, fileKind='Video', verbose=True)





















