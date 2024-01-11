import glob

if __name__ == "__main__":
    for filename in glob.glob("./recipes/*.md"):
        print(filename)