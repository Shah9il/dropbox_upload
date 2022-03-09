import os
import dropbox
from datetime import datetime
from DropBoxCustom import DropBoxCustom


def main():
    BASE_DIR = 'YOUR_CONTENT_BASE_DIRECTORY'
    list_files = [files for roots, dirs, files in os.walk(BASE_DIR)]
    file_link = {}
    for file_name in list_files[0]:
        dbox_file_path = f'{BASE_DIR}/{file_name}'
        dbox_upload = DropBoxCustom(dbox_file_path, file_name)
        file_uploaded = dbox_upload.upload()
        image_url = None
        if type(file_uploaded) == dropbox.files.FileMetadata:
            image_url = dbox_upload.getFileShareLink()
            print(image_url)
            file_link[file_name] = image_url
            if os.path.exists(dbox_file_path):
                print('Removing file after upload trial')
                os.remove(dbox_file_path)
            else:
                print("The file does not exist")
        else:
            print('File was not uploaded')
    print(file_link)


if __name__ == '__main__':
    ini_time_for_now = datetime.now()
    print(f'Script Startup Time: {str(ini_time_for_now)}')
    print(f'Initializing ...')
    main()
    stopage_time = datetime.now()
    print(f'Script Runtime: {str(stopage_time - ini_time_for_now)}')
