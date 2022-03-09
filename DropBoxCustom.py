import os, sys
import time
import dropbox
import requests
from datetime import datetime

DROPBOX_ROOT_FOLDER = '/'
DROPBOX_PROJECT_FOLDER = 'HDI'
DROPBOX_AUTORENAME_IF_FILE_EXIST=True

DROPBOX_ACCESS_TOKEN = 'YOUR_DROPBOX_ACCESS_TOKEN'
DROPBOX_ROOT_PATH = '/Apps/YOUR_DROPBOX_PROJECT_PATH/'

_DROPBOX_FOLDER = (DROPBOX_ROOT_FOLDER if DROPBOX_ROOT_FOLDER else '/')
_DROPBOX_SUBFOLDER = (DROPBOX_PROJECT_FOLDER if DROPBOX_PROJECT_FOLDER else '')
_AUTO_RENAME_FILES = (True if DROPBOX_AUTORENAME_IF_FILE_EXIST == True else False)


class DropBoxCustom:
    def __init__(self, full_local_file_path, dbox_filename, overwrite=False):
        self.access_token = DROPBOX_ACCESS_TOKEN
        self.dbox_folder = _DROPBOX_FOLDER
        self.dbox_subfolder = _DROPBOX_SUBFOLDER
        self.autorename = _AUTO_RENAME_FILES
        self.dbox_filename = dbox_filename
        self.full_local_file_path = full_local_file_path
        print(self.full_local_file_path)
        self.overwrite = (True if overwrite == True else False)
        # self.dbx = dropbox.Dropbox(self.access_token)

    def get_dropbox_file_path(self, withfile=1):
        """To return formatted file path for dropbox"""
        if withfile:
            dropbox_file_path = '/%s/%s/%s' % (
            self.dbox_folder, self.dbox_subfolder.replace(os.path.sep, '/'), self.dbox_filename)
        else:
            dropbox_file_path = '/%s/%s' % (self.dbox_folder, self.dbox_subfolder.replace(os.path.sep, '/'))
        while '//' in dropbox_file_path:
            dropbox_file_path = dropbox_file_path.replace('//', '/')
        print('*** Dropbox Upload Location: ', dropbox_file_path)
        return dropbox_file_path

    def dropbox_file_exist(self):
        """To check if requested file exist or not"""
        dbx = dropbox.Dropbox(self.access_token, timeout=None)
        file_list = [e.name if e.name == self.dbox_filename else '' for e in
                     dbx.files_list_folder(path=self.get_dropbox_file_path(0)).entries]
        dbx.close()
        return file_list

    def upload(self):
        """Upload a file.
        Return the request response, or None in case of error.
        """
        try:
            dbx = dropbox.Dropbox(self.access_token, timeout=None)
            path = self.get_dropbox_file_path()
            while '//' in path:
                path = path.replace('//', '/')
            mode = (dropbox.files.WriteMode.overwrite if self.overwrite else dropbox.files.WriteMode.add)
            mtime = os.path.getmtime(self.full_local_file_path)
            with open(self.full_local_file_path, 'rb') as f:
                data = f.read()
            try:
                res = dbx.files_upload(
                    data, path, mode,
                    client_modified=datetime(*time.gmtime(mtime)[:6]),
                    autorename=self.autorename,
                    mute=True)
            except dropbox.exceptions.ApiError as err:
                print('*** DropBox API error', err)
                dbx.close()
                return None
            print('uploaded as', res.name.encode('utf8'))
            dbx.close()
            return res
        except requests.exceptions.ConnectionError as e:
            print(e)
            return 'Got error'

    def getFileShareLink(self, getFileShareLinkCounter=0):
        dbx = dropbox.Dropbox(self.access_token, timeout=None)
        isFileFound = self.dropbox_file_exist()
        print(isFileFound)
        if isFileFound != ['']:
            dropbox_file_path = self.get_dropbox_file_path(1)
            print(dropbox_file_path)
            isLinkCreated = dbx.sharing_list_shared_links(dropbox_file_path)
            getFileShareLinkCounter += 1
            if not isLinkCreated.links:
                try:
                    print('Creating shared link')
                    # desired_shared_link_settings = dropbox.sharing.SharedLinkSettings(require_password=True, link_password=link_password, expires=None)
                    # expires = datetime.datetime.now() + datetime.timedelta(days=30)
                    requested_visibility = dropbox.sharing.RequestedVisibility.public
                    desired_shared_link_settings = dropbox.sharing.SharedLinkSettings(
                        requested_visibility=requested_visibility, expires=None)
                    shared_link_metadata = dbx.sharing_create_shared_link_with_settings(dropbox_file_path,
                                                                                        settings=desired_shared_link_settings)
                    # print(shared_link_metadata)
                    isLinkCreated = dbx.sharing_list_shared_links(dropbox_file_path)
                    url = isLinkCreated.links[0].url.replace('www.', 'dl.')
                    dbx.close()
                    return url

                except dropbox.exceptions.ApiError as err:
                    print('*** API error', err)
                    dbx.close()
                    return None
                else:
                    if getFileShareLinkCounter == 5:
                        dbx.close()
                        return None
                    self.getFileShareLink(getFileShareLinkCounter)
            else:
                url = isLinkCreated.links[0].url.replace('www.', 'dl.')
                # print(url)
                dbx.close()
                return url
        else:
            print('File not found in DropBox')
            dbx.close()
            return None


