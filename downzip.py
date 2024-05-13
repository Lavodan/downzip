import sevzhandler, downloader
from sys import argv
from os import path, remove, listdir, mkdir
from shutil import rmtree

def main(args=[]):
    if len(args) == 0:
        args = argv[1::]

    FLAGS = []
    if "-y" in [arg.lower() for arg in args]:  # Corrected to call lower() as a method
        FLAGS.append("-y")  # Changed to append the flag to the list
        args = [arg for arg in args if arg.lower() != "-y"]  # Remove the flag from the args list

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
    inner_name = listdir(f"{output}/{outer_name}")[0]
    innerarchive = f"{output}/{outer_name}/{inner_name}"
    sevzhandler.extract(innerarchive, output.rstrip("_OUT"), FLAGS)
    print(f"Inner archive extracted to {output.rstrip("_OUT")}")
    
    if output == output.rstrip("_OUT"):
        rmtree(f"{output}/{outer_name}")
    else:
        rmtree(output)
    print("Intermediate files deleted")
    
    return 0
    
    
    
if __name__ == "__main__":
    main()
    