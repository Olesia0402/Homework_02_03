import argparse
import shutil
import sys
from threading import Thread
from pathlib import Path

import normalize
import scan


parser = argparse.ArgumentParser(description='Sorting folder')
parser.add_argument("source", help="Source folder")

args = vars(parser.parse_args())

source = args.get("source")


folders = []


def handle_file(path, root_folder, dist) -> None:
    target_folder = root_folder/dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/normalize.normalize(path.name))


def handle_archive(path, root_folder, dist) -> None:
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    new_name = normalize.normalize(path.name.replace((".zip", ".gz", ".tar"), ''))

    archive_folder = target_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(archive_folder.resolve()))
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()


def remove_empty_folders(path) -> None:
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass


def grabs_folder(path: Path) -> None:
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            grabs_folder(el)


def main(folder_path):
    scan.scan(folder_path)

    for file in scan.images_files:
        handle_file(file, folder_path, ('JPEG', 'PNG', 'JPG', 'SVG'))

    for file in scan.documents_files:
        handle_file(file, folder_path, ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'))

    for file in scan.audio_files:
        handle_file(file, folder_path, ('MP3', 'OGG', 'WAV', 'AMR'))

    for file in scan.video_files:
        handle_file(file, folder_path, ('AVI', 'MP4', 'MOV', 'MKV'))

    for file in scan.others:
        handle_file(file, folder_path, 'OTHER')

    for file in scan.archives:
        handle_archive(file, folder_path, ('TAR', 'GZ', 'ZIP'))

    remove_empty_folders(folder_path)


if __name__ == '__main__':
    path = sys.argv[1]
    print(f'Start in {path}')

    folder = Path(path)
   
    threads = []

    for folder in folders:
        th = Thread(target=main, args=(folder,))
        th.start()
        threads.append(th)

    [th.join() for th in threads]

    print('Please delete the old folder if you need')