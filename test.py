#!/usr/bin/env python
#coding:utf-8
 
from __future__ import print_function, unicode_literals

from wiz.client import Wiz
from wiz.note import Note
from wiz.customfuncs import _mkdir
import os
import re
import getpass

wizUsername=''
wizPassword='' 
 
if not wizUsername:
    wizUsername=raw_input("Input your wizUsername:")
if not wizPassword:
    wizPassword=getpass.getpass("Input your wizPassword:")

def down_images(note,imageFolder):
    assert isinstance(note, Note)
    for image in note.data.images:
        #直接链接不下载到本地,相对链接才下载到本地
        if image.url.find(":/") >0:
            pass
        else:
            with open(os.path.join(imageFolder,image.name), 'wb') as fd:
                try:
                    fd.write(image.data)
                except:
                    print(" ! download image error:{0}".format(image.url))

def down_attachments(note,attachmentFolder):
    assert isinstance(note, Note)
    for attachment in note.data.attachments:
        with open(os.path.join(attachmentFolder, attachment.name), 'wb') as fd:
            fd.write(attachment.data)

def fix_note_urls(note,noteFilePath):
    assert isinstance(note,Note)
    if os.path.exists(noteFilePath):
        # replace each image url with newone
        with open(noteFilePath,"rw+") as notefile:
            content=notefile.read().decode('utf8')
            for img in note.data.images:
                if img.url.find(":/") >0:
                    pass
                else:
                    content=re.sub(re.escape(img.url),img.name,content,flags=re.I|re.MULTILINE|re.UNICODE)
            
            for attachment in note.data.attachments:
                content=re.sub(re.escape(attachment.url),attachment.name,content,flags=re.I|re.MULTILINE|re.UNICODE)
            if len(note.data.images)>0 or len(note.data.attachments) >0:
                notefile.truncate(0)
                notefile.write(content.encode('utf8'))
            
# login with username and password

wiz = Wiz(wizUsername,wizPassword )

# get home folder

# set default download path,and make sure wizexport folder exist
wizExportFolder=os.path.join(os.path.expanduser("~"),"Documents","wizexport",wizUsername)
_mkdir(wizExportFolder)


# list all folders and download all notes
for notebook in wiz.ls_notebooks():
    print("working on folder {0}".format(notebook.name))
    # limit folder name and file name to 50 
    notebookFolderPath=os.path.join(wizExportFolder,notebook.path.strip("/").replace("/",os.path.sep)[0:50])
    _mkdir(notebookFolderPath)
    for note in notebook.ls():
        print(" + downloading " + note.title)
        noteFilePath=os.path.join(notebookFolderPath,note.title.replace("/","-")[0:50] +".html")
        with open(noteFilePath,"w") as file:
            file.write(note.data.body.encode('utf8'))
        down_images(note,notebookFolderPath)
        down_attachments(note,notebookFolderPath)
        fix_note_urls(note,noteFilePath)

print("all files are exported to {0}".format(wizExportFolder))
