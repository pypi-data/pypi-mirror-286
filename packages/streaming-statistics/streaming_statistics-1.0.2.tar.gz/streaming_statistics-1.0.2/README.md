[![Python package](https://github.com/willf/streaming_stats/actions/workflows/test.yml/badge.svg)](https://github.com/willf/streaming_stats/actions)

## Streaming statistics

This is module for streaming statistics. It can efficiently calculate statistics on a stream of numbers in a minimum amount of memory.

It provides the following statistics:

| Statistic  | Description        |
| ---------- | ------------------ |
| `n`        | Number of values   |
| `min`      | Minimum value      |
| `max`      | Maximum value      |
| `sum`      | Sum of values      |
| `mean`     | Mean value         |
| `stddev`   | Standard deviation |
| `variance` | Variance           |

In addition to the above statistics, it also provides the following percentiles: 1st, 5th, 25th, 50th, 75th, 95th, and 99th.

Here is an example result:

```json
{
  "n": 177966,
  "mean": 237.02426306148718,
  "variance": 184870.5448188569,
  "stddev": 429.9657484252169,
  "min": 0,
  "max": 33408,
  "sum": 42182260,
  "1st": 5.002829575110743,
  "5th": 17.994143369901202,
  "10th": 25.791844500743554,
  "25th": 49.90296094906744,
  "50th": 100.4945677085671,
  "75th": 242.2894312639693,
  "90th": 607.9931874110874,
  "95th": 925.3552129773512,
  "99th": 1826.5794537820188
}
```

A script, `script/stats` will read numbers from standard input and print the statistics to standard output.

### Installation

This code uses the `poetry` system to install Python dependencies. To install, clone this
repository, and then:

```sh
$ poetry install
$ poetry shell
```

It is also available as a Python package on PyPI.

```sh
$ pip install streaming_statistics
```
