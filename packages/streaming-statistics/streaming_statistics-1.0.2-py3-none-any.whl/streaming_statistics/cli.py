#!/usr/bin/env python3
import sys
import json

from streaming_statistics import stats


def stdin_to_iterable():
    for line in sys.stdin:
        yield float(line)


def main():
    s = stats.stats(stdin_to_iterable())
    print(json.dumps(s))


if __name__ == "__main__":
    main()
