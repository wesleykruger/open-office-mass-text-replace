import os, fnmatch, zipfile, sys, shutil
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
            # I have no idea where this is coming from
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
        if folder != 'desktop.ini':
            zipf = zipfile.ZipFile('{0}.zip'.format(os.path.join(directory, folder)), 'w', zipfile.ZIP_DEFLATED)
            zipf.write(folder)
            zipf.close()


data_folder = Path("C:/Users/wesleykruger/Documents/Encore/single-line-fix/rename-these")
renameFileExtension(data_folder, ".odt", ".zip")
unzipToSeparateDirectories(data_folder)
findReplace(data_folder, "#if ( $PAGETWOARR.size() == 1 )", "#if ( $PAGETWOARR.size() == 1 || (($foreach.count - 1) % 4 == 0 and $foreach.count == $PAGETWOARR.size() ))", "*.xml")
zipFolder(data_folder)
renameFileExtension(data_folder, ".zip", ".odt")
