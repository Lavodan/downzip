import sevzhandler, downloader
from sys import argv
from os import path, remove, listdir, mkdir, rename
from shutil import rmtree, move
from subprocess import run
import tempfile   

def main(args=[]):    
    try:
        url, output, args, FLAGS = parse_args(args)
    except InvalidArgumentError as e:
        print(str(e))
        print(f"Usage: {path.basename(__file__)} <valid archive download url> [\"valid output folder\"] [-y] [-launch]")
        exit(1)
    
    archive_file = downloader.download(url, FLAGS)
    archive = archive_file.name
    print(f"File downloaded to {archive}")
    
    archive_folder_file = tempfile.TemporaryDirectory()
    archive_folder = archive_folder_file.name
    sevzhandler.extract(archive, archive_folder, FLAGS)
    print(f"Original archive extracted to {archive_folder}")
    
    remove(archive_file.name)
    print("Original archive deleted")
    
    inner_name, innerarchive = get_innerarchive(archive_folder)

    if not output:
        output = path.join("down_temp", inner_name)
        while path.isdir(output):
            output += "_"
    
    sevzhandler.extract(innerarchive, output, FLAGS)
    print(f"Inner archive extracted to {output}")
    
    archive_folder_file.cleanup()
    print("Intermediate files deleted")

    archive_contents = os.listdir(output)
    archive_contets_folder = path.join(output, archive_contents[0])
    if len(archive_contents) == 1 and os.is_dirarchive_contets_folder):
        output = move_content_up(archive_contets_folder)
        print(f"Deleted redundant folder at {archive_contets_folder}")
    print(f"Inner content moved to {output} folder")
    
    try:
        if "-launch" in FLAGS:
            location = launch_inkscape(output)
            print(f"Launching inkscape from {location}")
    except FileNotFoundError:
        print("Archive wasn't inkscape, skipping renaming...")
    
    exit(0)
    
def parse_args(args):
    if len(args) == 0:
        args = argv[1::]

    FLAGS = []
    for flag in ["-y", "-launch"]:
        if flag in [arg.lower() for arg in args]:
             FLAGS.append(flag)
             args = [arg for arg in args if arg.lower() != flag]

    if len(args) < 1 or len(args) > 2:
        raise InvalidArgumentError("Invalid number of arguments")
    elif args[0].find(".") == -1:
        raise InvalidArgumentError("Invalid url")
        
    url = args[0]
     
    try:
        output = args[1].lstrip("./")
    except IndexError:
        output = None
        
    return (url, output, args, FLAGS)
    
def get_innerarchive(archive_folder):
    outer_name = listdir(archive_folder)[0]
    inner_name = listdir(path.join(archive_folder, outer_name))[0]
    innerarchive = path.join(archive_folder, outer_name, inner_name)
    
    return inner_name, innerarchive
    
def move_content_up(root_folder, nested_folder):
    for file in listdir(nested_folder):
        file_path = path.join(nested_folder, file)
        move(file_path, root_folder)
    rmtree(nested_folder)
    return root_folder
    
def rename_inkscape(inner_folder):
    inkscape = False
    highest = 0
    for folder in listdir(inner_folder):
        if folder == "inkscape":
            inkscape = True
        elif folder.startswith("inkscape"):
            highest = max(int(folder.split(" ")[1]), highest)
        else:
            pass
            
    if not inkscape:
        return FileNotFoundError
    else:
        newname = path.join(inner_folder, "inkscape "+str(highest+1))
        rename(path.join(inner_folder, "inkscape"), newname)
        
        return newname
    
def launch_inkscape(inkscape_folder):
    location = path.join(inkscape_folder, "bin", "inkscape.exe")
    run(f"\"{location}\"")
    
    return location
    
class InvalidArgumentError(Exception):
    def __init__(self, message):
        if message:
            self.message = message + "!"

    def __str__(self):
        return self.message
    
    
if __name__ == "__main__":
    main()
    
