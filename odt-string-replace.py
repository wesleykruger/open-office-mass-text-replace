import os, fnmatch, zipfile, sys
from pathlib import Path


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

def zipFolder(directory):
    for folder in os.listdir(directory):
        if folder != 'desktop.zip':
            zipf = zipfile.ZipFile('{0}.zip'.format(os.path.join(directory, folder)), 'w', zipfile.ZIP_DEFLATED)
            for root, dirs, files in os.walk(os.path.join(directory, folder)):
                for filename in files:
                    zipf.write(os.path.abspath(os.path.join(root, filename)), arcname=filename)
            zipf.close()



data_folder = Path("C:/Path/To/File")
renameFileExtension(data_folder, ".odt", ".zip")
unzipToSeparateDirectories(data_folder)
findReplace(data_folder, "TEXT TO REPLACE", "TEXT TO INSERT", "*.xml")
zipFolder(data_folder)
renameFileExtension(data_folder, ".zip", ".odt")