import glob
import os
import re
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader("./src/templates"),
    autoescape=select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True
)


def extract_source(markdown_string):
    pattern = r"\s\[([^\]]+)\]\(([^\)]+)\)"
    matches = re.findall(pattern, markdown_string)
    return matches[0]


def parse_metadata(metadata):
    title = metadata[0].replace("# ", "")
    source_name, source_link = extract_source(metadata[1])
    servings = metadata[2]

    source = {
        "name": source_name,
        "link": source_link
    }

    return title, source, servings


def parse_list(lines, section_marker):
    sections = []
    section = []
    for line in lines:
        if line.startswith(section_marker):
            if len(section):
                sections.append(section)

            section = [line.strip()]
        elif line.strip():
            section.append(line.strip())

    sections.append(section)

    if len(sections) == 1:
        return sections[0]

    return sections


def generate_section(section):
    if len(section[0]) > 1:
        heading, *items = section
        heading_level = f"h{heading.count("#") + 1}"
        heading = heading.replace("# ", "").replace("#", "")

        items = [item[2:] for item in items]

        template = env.get_template("list.jinja")

        return template.render(heading=heading, items=items, heading_level=heading_level)
    else:
        heading, *items = section
        heading = heading[0]
        heading_level = f"h{heading.count("#") + 1}"
        heading = heading.replace("# ", "").replace("#", "")

        items = [generate_section(item) for item in items]

        template = env.get_template("list.jinja")

        return template.render(heading=heading, items=items, heading_level=heading_level)


def get_id(section):
    if (isinstance(section[0], list)):
        return section[0][0].replace("#", "").strip().lower()

    return section[0].replace("#", "").strip().lower()


def generate_recipe_content(path):
    with open(path, "r", encoding="utf-8") as file:
        md_sections = parse_list(file, "# ")
        metadata, *raw_sections = md_sections

        title, source, servings = parse_metadata(metadata)

        sections = [parse_list(s, "## ") for s in raw_sections]
        sections_content = [(get_id(section), generate_section(section)) for section in sections]

        template = env.get_template("recipe.jinja")

        return template.render(sections=sections_content, title=title, source=source, servings=servings)


def get_url_name(path):
    return os.path.basename(path).replace(".md", "").replace(" ", "-").lower()


def generate_recipe(path):
    content = generate_recipe_content(path)
    url_name = get_url_name(path)

    with open(f"./dist/{url_name}.html", "w", encoding="utf-8") as output:
        output.write(content)


def generate_index(paths):
    items = []

    for path in paths:
        name = os.path.basename(path).replace(".md", "").title()
        url = f"./{get_url_name(path)}.html"

        items.append((name, url))

    template = env.get_template("index.jinja")

    with open("./dist/index.html", "w") as output:
        output.write(template.render(items=items))


def main():
    os.makedirs("./dist", exist_ok=True)
    paths = [path for path in glob.glob("./recipes/*.md")]

    generate_index(paths)

    for path in paths:
        generate_recipe(path)


if __name__ == "__main__":
    main()
