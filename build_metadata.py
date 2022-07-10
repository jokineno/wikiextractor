import glob 
import json 
def get_files():
  wiki_files = glob.glob("./text/*/wiki*")
  return wiki_files 

valid_ids = set()

def build_metadata():
  global valid_ids
  wiki_files = get_files()
  metadata = {}
  for i,wiki in enumerate(wiki_files):
    print(f"Handling {i+1}/{len(wiki_files)}, {wiki=}")
    with open(wiki, "r") as f:
      data = f.read()
    metadata = handle_wiki(data, metadata)
  output_path = "metadata.json"
  write_data(output_path, metadata)
  write_data("valid_ids.json", list(valid_ids))

def write_data(output_path, data):
  with open(output_path, "w") as f:
    f.write(json.dumps(data))

def handle_wiki(data, metadata):  
  global valid_ids
  for sample in data.splitlines():
    try:
      sample = json.loads(sample)
    except Exception as e:
      raise Exception(e)
    paper_id = sample["id"]

    try:
      introduction_list_of_sentences = sample["introduction"][0]
    except IndexError:
      introduction_list_of_sentences = sample["introduction"]
    #print(introduction_list_of_sentences); break;
    introduction_text = " ".join(introduction_list_of_sentences)
    title = sample["title"]

    if len(introduction_text) < 50:
      pass
    elif "(täsmennyssivu)" in title:
      pass
    else:
      metadata[paper_id] = {}
      metadata[paper_id]["abstract"] = introduction_text
      metadata[paper_id]["title"] = title
      metadata[paper_id]["paper_id"] = paper_id
      valid_ids.add(paper_id)
  return metadata

build_metadata()
   

