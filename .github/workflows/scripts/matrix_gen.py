import json
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


def split_in_jobs(n_jobs: int, versions: list[str]) -> list[dict[str, list[str]]]:
    versions_per_job: int = math.ceil(len(versions) / n_jobs)
    start: int = 0
    result: list[dict[str, list[str]]] = []
    for i in range(n_jobs):
        result.append({"version_range": versions[start:start+versions_per_job]})
        start += versions_per_job
    return result


def main():
    minecraft_versions: list[str] = list(set(find_minecraft_versions()))
    print(minecraft_versions)
    jobs: list[dict[str, list[str]]] = split_in_jobs(19, minecraft_versions)
    version_split: str = json.dumps({"include": jobs})
    with open(os.environ["GITHUB_OUTPUT"], "w") as f:
        f.write(f"versions={version_split}\n")
    print(os.getenv("GITHUB_OUTPUT"))


if __name__ == '__main__':
    main()
