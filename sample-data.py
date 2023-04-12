import random
import json

def main():

    data_path = "final_citation_data.json"
    print("Reading {}..".format(data_path))
    with open(data_path, "r") as f:
        data = json.load(f)

    print("Generating sample with 100 keys")
    sample = {key: data[key] for key in random.sample(list(data.keys()), 100)}
    sample_path = "sample.json"
    with open(sample_path, "w") as f:
        f.write(json.dumps(sample))
    print(f"Wrote sample data to {sample_path}")

if __name__ == "__main__":
    main()