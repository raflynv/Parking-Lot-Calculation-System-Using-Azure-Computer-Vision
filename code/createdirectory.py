import os
import datetime

def datetimeformat(ts):
    return datetime.datetime.fromtimestamp(ts) 
    
def createdir(dirname):
    # Function to create directory if needed
    import os.path
    from os import path
    if path.os.path.isdir(dirname) :
        print("Directory:", dirname, "exists!")
    else:
        print("Creating directory:", dirname)
        os.mkdir(dirname)
        print("Done!")

def datetimeformat(ts):
    return datetime.datetime.fromtimestamp(ts)

def nbfiles(mydir):
    for root, _, files in os.walk(mydir):
        print("Directory:", root, "with", len(files), "files.")

