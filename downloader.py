from requests import get, head
from os import path, remove
import tempfile


def download(url, FLAGS, output=None):
    response = get(url, stream=True)   
    
    with tempfile.NamedTemporaryFile(delete=False) as file:
        print("Downloading file...")
        chunk_size = 5 * 2**20
        for idx, chunk in enumerate(response.iter_content(chunk_size = chunk_size)):
            file.write(chunk)
            print(f"{round(chunk_size*(idx+1)/1000000, 3)}MB downloaded")
    return file

def checkfile(filepath, filesize, netsize, FLAGS):
    while path.isdir(filepath):
        filepath += "_"
        print("Added _ to folder name because a folder with the same name already exists")
    
    if not path.isfile(filepath):
        return (filepath, False)
        
    elif netsize >= filesize:
        choice = choose("File with that name already exists... [o]verwrite, [e]xit, [r]ename:\n", FLAGS, [x for x in "oer"])
        if choice == 0:
            remove(filepath)
            return (filepath, False)
        elif choice == 1:
            raise Exception
        else:
            ext = filepath[-1 * (filepath[::-1].find(".")+1)::]
            filepath = filepath.rstrip(ext)+"_(1)"+ext
            return checkfile(filepath, filesize, netsize, FLAGS)
            
    elif filesize < netsize:
        choice = choose("File with that name already exists... [c]ontinue paused download, [o]verwrite, [e]xit, [r]ename, :\n", FLAGS, [x for x in "coer"])
        if choice == 0:
            remove(filepath)
            return (filepath, True)
        if choice == 1:
            return (filepath, False)
        elif choice == 2:
            raise Exception
        else:
            ext = filepath[-1 * (filepath[::-1].find(".")+1)::]
            filepath = filepath.rstrip(ext)+"_(1)"+ext
            checkfile(filepath, filesize, netsize)
                
def choose(text, FLAGS, options=["y", "n"]):
    options = [x.lower() for x in options]
    if "-y" in FLAGS:
        print(text)
        print("-y active, choosing first option")
        return 0
    else:
        ret = -1
        while ret not in range(0, len(options)):
            try:
                ret = options.index(input(text).lower())
            except ValueError:
                continue
        return ret