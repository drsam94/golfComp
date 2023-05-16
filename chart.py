#!/usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np 
import json 

def main():
    import argparse 
    parser = argparse.ArgumentParser("chart", "Script for drawing charts from golf")
    parser.add_argument("--source", type=str, default="results.json")

    args = parser.parse_args()
    with open(args.source, "r") as jf:
        source = json.load(jf)
    entries = []
    problems = []
    for lang, ldata in source.items():
        for user, p in ldata.items():
            entries.append((lang,user))
            problems = p 
    data_counts = {
        p : np.array(
        [
            source[lang][user][p] for lang,user in entries
        ]
        ) for p in problems
    }
    print(data_counts)
    entries = tuple([f"{lang}|{user}" for lang,user in entries])
    width = 0.6
    fix, ax = plt.subplots()
    bottom = np.zeros(len(entries))
    for problem, counts in data_counts.items():
        plot = ax.bar(entries, counts, width, label=problem, bottom=bottom)
        bottom += counts

        ax.bar_label(plot, label_type='center')
    ax.set_title('Code Golf Scores')
    ax.legend()

    plt.savefig("figure.png")

if __name__ == "__main__":
    main()