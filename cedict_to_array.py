import json


def parse_line(line):
    parts = line.split(" ")
    traditional = parts[0]
    simplified = parts[1]
    rest = " ".join(parts[2:])
    pinyin_start = rest.find("[") + 1
    pinyin_end = rest.find("]")
    pinyin = rest[pinyin_start:pinyin_end]
    definitions = rest[pinyin_end + 2 :].strip().split("/")[1:-1]
    return traditional, simplified, pinyin, definitions


def process_cedict(file_path):
    data = {}
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if not line.startswith("#"):
                traditional, simplified, pinyin, definitions = parse_line(line)
                if traditional not in data:
                    data[traditional] = {
                        "t": traditional,
                        "s": simplified,
                        "p": pinyin,
                        "d": ";".join(definitions),
                    }
                else:
                    data[traditional]["p"] += "/" + pinyin
                    data[traditional]["d"] += "/" + ";".join(definitions)

    # Convert dictionary to array of objects
    result = list(data.values())

    # Handle deduplication
    for entry in result:
        if entry["s"] == entry["t"]:
            entry.pop("s")  # Remove the simplified entry if same as traditional

    return result


# Path to your CEDICT file
file_path = "cedict_ts.u8"
cedict_data = process_cedict(file_path)

# Optionally, write to a JSON file
with open("cedict_processed.json", "w", encoding="utf-8") as outfile:
    json.dump(cedict_data, outfile, ensure_ascii=False, indent=2)
