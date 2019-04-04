# open-office-mass-string-replace

This Python script essentially acts as a mass find/replace string for Open Office XML files. This arose from a business need to insert/edit Velocity script within Open Office content.xml files. Editing these files requires that you rename the .odt file extension to .zip, extract it, edit the XML, rezip the directory, then rename the extension back to .odt. 

This process became tedious when it needed to be done for dozens of files, so I created this script to do it for me. Just drop all the ODT files that you want to edit into a directory, then run the script with the data_folder variable pointing at that directory.

## Known bugs
Currently none. The program will only replace one line at a time, and that can be adjusted if a business need arises.
