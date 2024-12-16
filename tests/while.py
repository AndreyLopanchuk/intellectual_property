import subprocess
import time

if __name__ == "__main__":
    time.sleep(3)
    subprocess.run(["pytest", "-vv", "-s", "tests/"])

    while True:
        time.sleep(500)
        pass
