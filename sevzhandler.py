from os import path
from subprocess import run

SEVZ_PATH = "7zip/7za.exe"

if not path.exists(SEVZ_PATH):
    print("Error! Missing the SEVza executable.")
    raise FileNotFoundError

def extract(archive, output, FLAGS):
    if "-y" in FLAGS:
        yesflag = " -y"
    else:
        yesflag = ""
    archive = path.abspath(archive)
    output = path.abspath(output)
    run(f"{SEVZ_PATH} x -o\"{output}\" \"{archive}\"{yesflag}")
    return 0
    
def compress(archive, files, FLAGS):
    if "-y" in FLAGS:
        yesflag = " -y"
    else:
        yesflag = ""
    archive = path.abspath(archive)
    files = [path.abspath(file) for file in files]
    run(f"{SEVZ_PATH} a {''.join(archive+files)}{yesflag}")
    return 0