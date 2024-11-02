import argparse
from pathlib import Path
from shutil import copyfile
from threading import Thread
import logging


parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="dist")


args = vars(parser.parse_args())
source = Path(args.get("source"))
output = Path(args.get("output"))

folders = []

def grabs_folder(directory: Path) -> None:
    for el in directory.iterdir():
        if el.is_dir():
            folders.append(el)
            grabs_folder(el)


def copy_file(file_path: Path) -> None:
    for el in file_path.iterdir():
        if el.is_file():
            ext = el.suffix[1:]
            ext_folder = output / ext
            try:
                ext_folder.mkdir(exist_ok=True, parents=True)
                copyfile(el, ext_folder / el.name)
                logging.info(f"Copied {file_path} to {ext_folder}")
            except OSError as err:
                logging.error(f"Error copying {file_path}: {err}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")

    folders.append(source)
    grabs_folder(source)

    threads = []
    for folder in folders:
        th = Thread(target=copy_file, args=(folder,))
        th.start()
        threads.append(th)

    [th.join() for th in threads]
    print(f"Processed all files in {source}. You can  now delete this folder if needed.")
