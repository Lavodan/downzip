import sevzhandler, downloader
from sys import argv
from os import path, remove, listdir, mkdir, rename
from shutil import rmtree
from subprocess import run

def main(args=[]):
    if len(args) == 0:
        args = argv[1::]

    FLAGS = []
    for flag in ["-y", "-launch"]:
        if flag in [arg.lower() for arg in args]:
             FLAGS.append(flag)
             args = [arg for arg in args if arg.lower() != flag]

    try:
        if len(args) < 1 or len(args) > 2:  # Corrected the condition for checking the number of arguments
            print("Usage: downzip <valid archive download url> [\"valid output folder\"] [-y]")
            return 1
        elif args[0].find(".") == -1:
            print("Invalid url!")
            return 1
    except IndexError:
        pass

    url = args[0]
    try:
        output = args[1].lstrip("./")
    except IndexError:
        output = None
    
    archive = downloader.download(url, FLAGS, output)
    
    if not path.isfile(archive):
        output = archive
    else:
        output = archive+"_OUT"
    
    if not path.isdir(output):
        mkdir(output)
        
    print(f"File downloaded to {archive}")
       
    sevzhandler.extract(archive, output, FLAGS)
    print(f"First file extracted to {output}")
    
    remove(archive)
    print("Original archive deleted")
    
    
    outer_name = listdir(output)[0]
    inner_name = listdir(path.join(output, outer_name))[0]
    innerarchive = path.join(output, outer_name, inner_name)
    sevzhandler.extract(innerarchive, output.rstrip("_OUT"), FLAGS)
    print(f"Inner archive extracted to {output.rstrip("_OUT")}")
    
    if output == output.rstrip("_OUT"):
        rmtree(path.join(output, outer_name))
    else:
        rmtree(output)
    print("Intermediate files deleted")
    
    try:
        inkscape_folder = rename_inkscape(output.rstrip("_OUT"))
        
        if "-launch" in FLAGS:
            location = launch_inkscape(inkscape_folder)
            print(f"Launching inkscape from {location}")
    except FileNotFoundError:
        print("Archive wasn't inkscape, skipping renaming...")
    
    return 0
    
def rename_inkscape(inner_folder):
    inkscape = False
    highest = 0
    for folder in listdir(inner_folder):
        if folder == "inkscape":
            inkscape = True
        elif folder.startswith("inkscape"):
            highest = int(folder.split(" ")[1])
        else:
            pass
            
    if not inkscape:
        return FileNotFoundError
    else:
        newname = path.join(inner_folder, "inkscape "+str(highest+1))
        rename(path.join(inner_folder, "inkscape"), newname)
        
        return newname
    
def launch_inkscape(inkscape_folder):
    breakpoint()
    location = path.join(inkscape_folder, "bin", "inkscape.exe")
    run(f"\"{location}\"")
    
    return location
    
    
if __name__ == "__main__":
    main()
    