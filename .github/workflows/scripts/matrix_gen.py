import json
import os


def main():
    version_split: str = json.dumps({"include": [{"version_range": ["1.1", "1.2", "1.3"]}, {"version_range": ["1.4", "1.5", "1.6"]}]})
    os.environ["GITHUB_OUTPUT"] = f"versions={version_split}"
    print(os.getenv("GITHUB_OUTPUT"))


if __name__ == '__main__':
    main()
