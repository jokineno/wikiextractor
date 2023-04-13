import glob 
import json

from common import setup_logging
import sys
log_file = sys.argv[0] + ".log"
logger = setup_logging(log_output=log_file)

def get_files():
  print("Reading all wiki files...")
  wiki_files = glob.glob("./text/*/wiki*")
  print("Done reading.")
  return wiki_files 

valid_ids = set()


def build_metadata():
  global valid_ids
  wiki_files = get_files()
  metadata = {}
  for i,wiki in enumerate(wiki_files):
    logger.info(f"Handling {i+1}/{len(wiki_files)}, {wiki}")
    with open(wiki, "r") as f:
      data = f.read()
    metadata = handle_wiki(data, metadata)
  output_path = "metadata.json"
  write_data(output_path, metadata)
  write_data("valid_ids.json", list(valid_ids))


def write_data(output_path, data):
  logger.info("Saving data to path {}".format(output_path))
  with open(output_path, "w") as f:
    f.write(json.dumps(data))
  logger.info("Saved.")


def handle_wiki(data, metadata):  
  global valid_ids
  for sample in data.splitlines():
    try:
      sample = json.loads(sample)
    except Exception as e:
      raise Exception(e)
    paper_id = sample["id"]

    try:
      introduction_list_of_sentences = sample["introduction"][0] #list of list
    except IndexError:
      introduction_list_of_sentences = sample["introduction"]
    #print(introduction_list_of_sentences); break;
    introduction_text = " ".join(introduction_list_of_sentences) #join sentences
    title = sample["title"]

    character_count_filter = 50
    if len(introduction_text) < character_count_filter: #skip introductions that are less than 50 characters. Do configurable.
      logger.debug("Skipping article {}".format(title))
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

def main():
  build_metadata()


if __name__ == "__main__":
  main()
   

