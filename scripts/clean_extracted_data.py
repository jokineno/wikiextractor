import json 
import glob 


wiki_files = glob.glob("./text/*/wiki_*")


for wiki in wiki_files:
    with open(wiki, "r") as f:
        data = f.read()
    for sample in data.splitlines():
        sample = json.loads(sample)
        sample_id = sample["id"]
        reference_list = sample["introduction_references"]
        