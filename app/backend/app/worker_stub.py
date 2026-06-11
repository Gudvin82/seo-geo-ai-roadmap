from __future__ import annotations

import time


def main() -> None:
    while True:
        print("worker-stub: waiting for future scheduled jobs...")
        time.sleep(60)


if __name__ == "__main__":
    main()
