import os
from openai import OpenAI
def read_files(dir, sysml=True):
    files = []
    for file in os.listdir(dir):
        if os.path.isdir(dir + '/' + file):
            files += read_files(dir + '/' + file)
        else:
            files.append(str(dir + '/' + file))
    if not sysml:
        return files
    dropped = ["Example/SysML v2 Spec Annex A SimpleVehicleModel.sysml"]
    return [file for file in files if file not in dropped and file.endswith(".sysml")]
