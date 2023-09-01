import math
import os
from typing import Generator


def find_minecraft_versions() -> Generator[str, str, None]:
    for filename in os.listdir("mappings"):
        if filename.endswith(".tiny"):
            yield filename.removesuffix(".tiny")
        elif filename.endswith(".tinydiff"):
            if len(pair := filename.removesuffix(".tinydiff").split("#")) == 2:
                yield pair[-1]


def split_in_workflows(max_versions: int, versions: list[str]) -> list[list[str]]:
    n_workflows: int = math.ceil(len(versions) / max_versions)
    start: int = 0
    result: list[list[str]] = []
    for i in range(n_workflows):
        result.append(versions[start:start+max_versions])
        start += max_versions
    return result


def main():
    minecraft_versions: list[str] = list(set(find_minecraft_versions()))
    minecraft_versions.sort()
    workflows: list[list[str]] = split_in_workflows(230, minecraft_versions)
    for i, versions in enumerate(workflows):
        with open(".github/workflows/templates/publish_runner_template.yml", "r") as r_template:
            template: str = r_template.read()
            template: str = template.replace("PUBLISH_NUMBER", str(i))
            template: str = template.replace("PUBLISH_VERSIONS", f"{versions}")
        with open(f".github/workflows/publish_{i}.yml", "w") as publish:
            publish.write(template)


if __name__ == '__main__':
    main()
