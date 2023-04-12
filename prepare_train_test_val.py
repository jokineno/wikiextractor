import json 
from sklearn.model_selection import train_test_split
import argparse
import random 

random.seed(10)

parser = argparse.ArgumentParser()

parser.add_argument("--sample_size", type=int, help="sample x articles from all data.")
args = parser.parse_args()
sample_size = args.sample_size


with open("metadata.json", "r") as f:
    data = json.load(f)

articles = list(data.keys())

if isinstance(sample_size, int):
    articles = random.sample(articles, sample_size)

total = len(articles)

train_and_val, test = train_test_split(articles, test_size = 0.2, random_state=1)

# 0.8x * y = 0.1x
# 0.1x / 0.8x = y

train, val = train_test_split(train_and_val, test_size=0.125, random_state=1)

test_fraq = len(test)/total
val_fraq = len(val)/total
train_fraq = len(train)/total


print(f"train size: {len(train)} ({train_fraq}),\ntest_size = {len(test)} ({test_fraq}),\n validation size = {len(val)} ({val_fraq})")

class Writer():
    def __init__(self, output_path):
        self.output_path = output_path
        self.out = open(output_path, "w")

    def write(self, data):
        line = data + "\n"
        self.out.write(line)
    
    def close(self):
        self.out.close()
        print(f"Finished writing {self.output_path}")
        

for name, dataset in zip(["train.txt", "test.txt", "val.txt"], [train, test, val]):
    name = f"./training/{name}"
    writer = Writer(name)
    for sample_id in dataset:
        writer.write(sample_id)
    
    writer.close()

