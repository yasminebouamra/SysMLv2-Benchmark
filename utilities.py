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


def embed(text):
    openai = OpenAI(api_key="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")
    return openai.embed(text, model='text-embedding-3-large')
