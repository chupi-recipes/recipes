import glob
import os
from jinja2 import Template

def main():
    os.makedirs("./dist", exist_ok=True)
    filenames = [filename for filename in glob.glob("./recipes/*.md")]

    with open("./src/templates/index.html.jinja", "r") as f:
        template = Template(f.read())

        content = template.render(paths=filenames)

        with open("./dist/index.html", "w") as output:
            output.write(content)

if __name__ == "__main__":
    main()