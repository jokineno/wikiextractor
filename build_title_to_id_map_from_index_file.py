import json 

def build_mapping():
    mapping = {}
    mapping2 = {}
    data_path = "../data/fiwiki-20220301-pages-articles-multistream-index.txt"
    with open(data_path, "r") as f:
        data = f.read()
    
    data = data.split("\n")
    for line in data:
        try:
            if line == "":
                continue
            parts = line.split(":", 1)
            title_id, title_name = parts[1].split(":", 1)
            title_name = title_name.lower()
            
            title2id = {title_name:title_id}
            id2title = {title_id:title_name}
            mapping.update(title2id)
            mapping2.update(id2title)
        except Exception as e:
            print(line, parts)
            raise Exception("STOPPING due to errtors.")

    return mapping, mapping2


title2id, id2title = build_mapping()

path1 = "title2id.json"
path2= "id2title.json"
with open(path1, "w") as f:
    f.write(json.dumps(title2id))
    print(f"Wrote title2id to path {path1}")

with open(path2, "w") as f:
    f.write(json.dumps(id2title))
    print(f"Wrote id2title to path {path2}")
