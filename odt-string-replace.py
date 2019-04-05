import os, fnmatch, zipfile, sys, shutil
from pathlib import Path


textToReplace = ""
textToInsert = ""
# Use forward slashes for this path even if you are on Windows, pathlib's Path functionality handles it this way
pathToOdtDirectory = ""


def renameFileExtension(directory, startingExtension, endingExtension):
    for filename in os.listdir(directory):
        if filename.lower().endswith(startingExtension):
            base = os.path.splitext(filename)[0]
            newFileName = base + endingExtension
            os.replace(os.path.join(directory, filename), os.path.join(directory, newFileName))


def findReplace(directory, find, replace, filePattern):
    for path, dirs, files in os.walk(os.path.abspath(directory)):
        for filename in fnmatch.filter(files, filePattern):
            filepath = os.path.join(path, filename)
            with open(filepath) as f:
                s = f.read()
            s = s.replace(find, replace)
            with open(filepath, "w") as f:
                f.write(s)


def unzipToSeparateDirectories(directory):
    pattern = '*.zip'
    for root, dirs, files in os.walk(directory):
        for filename in fnmatch.filter(files, pattern):
            '''I have no idea where this is coming from'''
            if filename != 'desktop.zip':
                print(os.path.join(root, filename))
                zipfile.ZipFile(os.path.join(root, filename)).extractall(os.path.join(root, os.path.splitext(filename)[0]))
    deleteOldZips(directory)


def deleteOldZips(directory):
    for root, dirs, files in os.walk(directory):
        for currentFile in files:
            if currentFile.lower().endswith('.zip'):
                os.remove(os.path.join(root, currentFile))


def get_all_file_paths(directory):
    # initializing empty file paths list
    file_paths = []

    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

            # returning all file paths
    return file_paths


def zipFolder(directory):
    # Open Office expects that all files be deflated except for the mimetype file.
    # Mimetype must not be compressed in any way, so we need 2 ZipFile vars,
    # The 2nd will append the uncompressed mimetype file
    for folder in os.listdir(directory):
        if folder != 'desktop.ini':
                parent_folder = os.path.dirname(os.path.join(directory, folder))
                # Retrieve the paths of the folder contents.
                contents = os.walk(os.path.join(directory, folder))
                try:
                    zip_file = zipfile.ZipFile(os.path.join(directory, folder) + '.zip', 'w', zipfile.ZIP_DEFLATED)
                    for root, folders, files in contents:
                        # Include all subfolders, including empty ones.
                        for folder_name in folders:
                            absolute_path = os.path.join(root, folder_name)
                            relative_path = absolute_path.replace(parent_folder + '\\',
                                                                  '')
                            relative_path = relative_path.replace(folder + '\\', '')
                            zip_file.write(absolute_path, relative_path)
                        for file_name in files:
                                if file_name != 'mimetype':
                                    absolute_path = os.path.join(root, file_name)
                                    relative_path = absolute_path.replace(parent_folder + '\\',
                                                                          '')
                                    relative_path = relative_path.replace(folder + '\\', '')
                                    zip_file.write(absolute_path, relative_path)
                finally:
                    zip_file.close()
    for folder in os.listdir(directory):
        if folder != 'desktop.ini' and not folder.endswith('.zip'):
            parent_folder = os.path.dirname(os.path.join(directory, folder))
            # Retrieve the paths of the folder contents.
            contents = os.walk(os.path.join(directory, folder))
            try:
                zip_file2 = zipfile.ZipFile(os.path.join(directory, folder) + '.zip', 'a', zipfile.ZIP_STORED)
                for root, folders, files in contents:
                    for file_name in files:
                            if file_name == 'mimetype':
                                absolute_path = os.path.join(root, file_name)
                                relative_path = absolute_path.replace(parent_folder + '\\',
                                                                      '')
                                relative_path = relative_path.replace(folder + '\\', '')
                                zip_file2.write(absolute_path, relative_path)
            finally:
                zip_file2.close()


def deleteLeftoverFolders(directory):
    for root, dirs, files in os.walk(directory):
        for folder in dirs:
            shutil.rmtree(os.path.join(directory, folder))


data_folder = Path(pathToOdtDirectory)
renameFileExtension(data_folder, ".odt", ".zip")
unzipToSeparateDirectories(data_folder)
findReplace(data_folder, textToReplace, textToInsert, "*.xml")
zipFolder(data_folder)
renameFileExtension(data_folder, ".zip", ".odt")
deleteLeftoverFolders(data_folder)