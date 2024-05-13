from requests import get, head
from os import path, remove



def download(url, FLAGS, output=None):
    response = get(url, stream=True)
    
    headers = head(url).headers
    if output == None:
        try:
            start_filename = headers["content-disposition"][headers["content-disposition"].find("filename")+len("filename")+1::]
            if start_filename.find(";") == -1:
                name = start_filename[::]
            else:
                name = start_filename[:start_filename.find(";")-1:]
        except KeyError:
            try:
                name1 = headers["location"][-1 * headers["location"][::-1].find("/")::]
                name2 = headers["location"][-20::]
                name = name1 if len(name1) < len(name2) else name2
            except KeyError:
                name = "unnamed"
            
        nname = ""
        for char in name:
            if not char in "<>:\"/\\|?*":
                nname += char
        name = nname
        name = name.rstrip(". ")
        name = name[:-1 * name[::-1].find(".") - 1:]
        output = f"./temp_down/{name}"
            
    if path.exists(output):
        currentsize = path.getsize(output)
    else:
        currentsize = 0
        
    try:
        netsize = int(response.headers["content-length"])
    except KeyError:
        netsize = 2**30-1
        
    output, mo = checkfile(output, currentsize, netsize, FLAGS)
    mode = "ab" if mo else "wb"
    
    if mode == "ab":
        response = get(url, stream = True, headers = {"Range": f"bytes={path.getsize(output)+1}-{response.headers["content-length"]}"})
    
    print(output, mode)
    
    
    
    with open(output, mode=mode) as file:
        print("Downloading file...")
        chunk_size = 5 * 2**20
        for idx, chunk in enumerate(response.iter_content(chunk_size = chunk_size)):
            file.write(chunk)
            print(f"{round(chunk_size*(idx+1)/1000000, 3)}MB downloaded")
    return output

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