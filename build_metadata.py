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
count = 0


def read_title2id():
    with open("title2id.json", "r") as f:
        data = json.load(f)
        return data


def build_metadata():
    global valid_ids, count
    wiki_files = get_files()
    title2id = read_title2id()
    metadata = {}
    for i, wiki in enumerate(wiki_files):
        # logger.info(f"Handling {i+1}/{len(wiki_files)}, {wiki}")
        with open(wiki, "r") as f:
            data = f.read()
        metadata = handle_wiki(data, metadata, title2id, wiki)
    output_path = "metadata.json"
    write_data(output_path, metadata)
    write_data("valid_ids.json", list(valid_ids))


def write_data(output_path, data):
    logger.info("Saving data to path {}".format(output_path))
    with open(output_path, "w") as f:
        f.write(json.dumps(data))
    logger.info("Saved.")


def handle_classes(title, paper_id, classes, title2id):
    global count
    for c in classes:
        try:
            class_name = c['match'].lower() \
                .replace(": ", ":", 1) \
                .replace("\u200e", "") \
                .replace("\xa0", " ") \
                .replace("  ", " ") \
                .replace("   ", "") \
                .replace("\n", "") \
                .strip()
            c['class_id'] = title2id[class_name]
        except KeyError as e:
            # print("class name: {} => {} || Error: {}".format(c['match'], class_name, e))
            try:
                class_name = class_name.replace("_", " ")
                c['class_id'] = title2id[class_name]
                # print("SUCCESS", class_name, c['class_id'])
            except KeyError:
                if class_name == 'luokka:magic:the gathering -pelaajat':
                    c['class_id'] = title2id['luokka:magic: the gathering -pelaajat']
                    continue
                if class_name == 'luokka:wolfenstein:enemy territoryn modit':
                    c['class_id'] = title2id['luokka:wolfenstein: enemy territoryn modit']
                    continue
                if class_name == "luokka:suomalaiset   tieteilijät":
                    c['class_id'] = title2id['luokka:suomalaiset tieteilijät']
                    continue

                print("Skipping", title, paper_id, class_name)
                c['class_id'] = None
                count += 1
        except Exception as e:
            raise Exception(e)


def handle_wiki(data, metadata, title2id, wiki_filename):
    global valid_ids, count
    for sample in data.split("\n\n"):

        try:
            if sample == "":
                continue

            sample = json.loads(sample)
        except Exception as e:
            print("=======WIKIFILENAME=======", wiki_filename)
            # print("data", data)
            print("\n")
            print("sample", sample)
            raise Exception(e)
        paper_id = sample["id"]

        try:
            introduction_list_of_sentences = sample["introduction"][0]  # list of list
        except IndexError:
            introduction_list_of_sentences = sample["introduction"]
        # print(introduction_list_of_sentences); break;
        introduction_text = " ".join(introduction_list_of_sentences)  # join sentences
        title = sample["title"]
        references = sample['references']
        handle_classes(title, paper_id, sample['classes'], title2id)
        character_count_filter = 50
        if len(introduction_text) < character_count_filter:  # skip introductions that are less than 50 characters. Do configurable.
            logger.debug("Skipping article {}".format(title))
            pass
        elif "(täsmennyssivu)" in title:
            pass
        else:
            metadata[paper_id] = {}
            metadata[paper_id]["abstract"] = introduction_text
            metadata[paper_id]["title"] = title
            metadata[paper_id]["paper_id"] = paper_id
            metadata[paper_id]['references'] = references
            metadata[paper_id]['classes'] = [item['class_id'] for item in sample['classes'] if item['class_id'] is not None]
            valid_ids.add(paper_id)
    return metadata


def main():
    build_metadata()


if __name__ == "__main__":
    main()
    print("COUNT", count)
