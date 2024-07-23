import os
import abcli
from abcli import file
from abcli.file.functions import build_from_template
from abcli.plugins import markdown
from kamangir import NAME, VERSION
from kamangir.content import content
from kamangir.logger import logger

NAME = f"{NAME}.README"


def build(filename: str = ""):
    if not filename:
        filename = os.path.join(file.path(__file__), "../README.md")

    logger.info(
        "{}.build: {}: {} item(s) loaded: {}".format(
            NAME,
            filename,
            len(content["items"]),
            ", ".join(list(content["items"].keys())),
        )
    )

    items = [
        "{}[`{}`]({}) [![image]({})]({}) {} {}".format(
            item["icon"],
            item["name"].replace("_", "-"),
            f"https://github.com/kamangir/{name}",
            item["image"],
            f"https://github.com/kamangir/{name}",
            item["description"],
            item["pypi"],
        )
        for name, item in content["items"].items()
        if name != "template"
    ]

    table = markdown.generate_table(items, content["cols"])

    signature = [
        "---",
        "built by [`{}`]({}), based on [`{}-{}`]({}).".format(
            abcli.fullname(),
            "https://github.com/kamangir/awesome-bash-cli",
            NAME,
            VERSION,
            "https://github.com/kamangir/kamangir",
        ),
    ]

    return file.build_from_template(
        os.path.join(file.path(__file__), "./assets/README.md"),
        {
            "--table--": table,
            "--signature": signature,
        },
        filename,
    )
