import os
import shutil
import subprocess
import sys
import time
from typing import Optional


class GradleProcess:
    def __init__(self, version: str):
        self._PUBLISH_TEMP_DIR: str = "publish_temp"
        self._version: str = version
        self._gradle_command: str = "gradlew" if os.name == "nt" else "./gradlew"
        self._process: Optional[subprocess.Popen] = None
        self._times_run: int = 0
        self._TO_COPY: list[str] = ["gradle", "mappings", "build.gradle", "gradle.properties", "gradlew", "gradlew.bat", "settings.gradle"]

    def __enter__(self):
        if not os.path.exists(self._PUBLISH_TEMP_DIR):
            os.mkdir(self._PUBLISH_TEMP_DIR)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if os.path.exists(self._PUBLISH_TEMP_DIR):
            shutil.rmtree(self._PUBLISH_TEMP_DIR)

    def start(self) -> None:
        while self._should_retry():
            self._times_run += 1
            print(f"Version {self._version}")
            self._delete_dir()
            os.mkdir(os.path.join(self._PUBLISH_TEMP_DIR, self._version))
            self._get_ready()
            self._run_gradle_command()
            self._process_listener()
            while self._process.poll() is None:
                time.sleep(0.5)
            self._delete_dir()
            if self.get_exit_code() == 0:
                return

    def _should_retry(self) -> bool:
        return self._times_run <= 2

    def _delete_dir(self) -> None:
        if os.path.isdir(os.path.join(self._PUBLISH_TEMP_DIR, self._version)):
            shutil.rmtree(os.path.join(self._PUBLISH_TEMP_DIR, self._version))

    def _get_ready(self) -> None:
        for element in self._TO_COPY:
            if os.path.isdir(element):
                shutil.copytree(element, os.path.join(self._PUBLISH_TEMP_DIR, self._version, element))
            else:
                shutil.copy(element, os.path.join(self._PUBLISH_TEMP_DIR, self._version, element))

    def get_exit_code(self) -> int:
        return self._process.returncode

    def get_version(self) -> str:
        return self._version

    def _run_gradle_command(self) -> None:
        env = os.environ.copy()
        env["MC_VERSION"] = self._version
        # shell=True, check=True, env=env
        self._process = subprocess.Popen(
            f"{self._gradle_command} publish --stacktrace",
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            env=env,
            cwd=os.path.join(self._PUBLISH_TEMP_DIR, self._version)
        )

    def _process_listener(self) -> None:
        while True:
            try:
                text: bytes = next(iter(self._process.stdout))
            except StopIteration:
                break
            else:
                print(f"[{self._version}] {text.decode('utf-8')[:-1]}")


def main():
    version: str = os.getenv("MC_VER", "")
    if not version:
        sys.exit(0)
    with GradleProcess(version) as process:
        process.start()
        exit_code: int = process.get_exit_code()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
