import numpy as np
import string

from .resulter import Status


headers = [
    'rmw', 'host', 'mode', 'topic', 'rate',
    '#subscribers', 'zero_copy','reliable', 'transient',
    '#msg received', '#msg sent', '#msg lost',
    'data received', 'latency_min (ms)', 'latency_max (ms)',
    'latency_mean (ms)', 'latency_variance (ms)', 'cpu usage (%)',
    'max ram usage (MB)',
    'CPU WIN', 'CPU COMPARE',
    'RAM WIN', 'RAM COMPARE',
    'LATENCY_MEAN WIN', 'LATENCY_MEAN COMPARE',
    'JITTER_MEAN WIN', 'JITTER_MEAN COMPARE',
]

prekeys = ['rmw']
testkeys = ['host', 'mode', 'topic', 'rate', 'subs', 'zero_copy', 'reliable', 'transient']
datakeys = ['received', 'sent', 'lost', 'data_received',
            'latency_min', 'latency_max', 'latency_mean',
            'latency_variance', 'cpu_usage', 'ram_usage']

status_value_strings = {
    Status.CYCLONEDDS_WIN.value: 'CYCLONE',
    Status.FASTRTPS_WIN.value: 'FAST',
    Status.CYCLONEDDS_FAIL.value: 'FAST BYDEF',
    Status.FASTRTPS_FAIL.value: 'CYCLONE BYDEF'
}


def cellname(x, y):
    if x > 26:
        first = string.ascii_uppercase[x // 26]
        second = string.ascii_uppercase[x % 26]
        return f"{first}{second}{y+1}"
    else:
        return f"{string.ascii_uppercase[x]}{y+1}"


def summation_rows(n_tests):
    xoffset = len(prekeys) + len(testkeys) + len(datakeys)
    empty_pre_space = [' '] * (xoffset - 1)

    cyclonedds_win = sum(([
        f"=COUNTIF({cellname(xoffset+2*i, 1)}:{cellname(xoffset+2*i, 1+2*n_tests)}, \"CYCLONE\") + " +
        f"COUNTIF({cellname(xoffset+2*i, 1)}:{cellname(xoffset+2*i, 1+2*n_tests)}, \"CYCLONE BYDEF\")",
        " "] for i in range(4)), [])
    fastrtps_win = sum(([
        f"=COUNTIF({cellname(xoffset+2*i, 1)}:{cellname(xoffset+2*i, 1+2*n_tests)}, \"FAST\") + " +
        f"COUNTIF({cellname(xoffset+2*i, 1)}:{cellname(xoffset+2*i, 1+2*n_tests)}, \"FAST BYDEF\")",
        " "] for i in range(4)), [])
    cyclonedds_fail = sum(([f"=COUNTIF({cellname(xoffset+2*i, 1)}:{cellname(xoffset+2*i, 1+2*n_tests)}, \"FAST BYDEF\")", " "] for i in range(4)), [])
    fastrtps_fail = sum(([f"=COUNTIF({cellname(xoffset+2*i, 1)}:{cellname(xoffset+2*i, 1+2*n_tests)}, \"CYCLONE BYDEF\")", " "] for i in range(4)), [])
    total_test = sum(([n_tests, ' '] for i in range(4)), [])

    return [
        ['-'] * len(headers),
        empty_pre_space + ['Cyclone DDS Wins'] + cyclonedds_win,
        empty_pre_space + ['FastRTPS Wins'] + fastrtps_win,
        empty_pre_space + ['Cyclone DDS Failed tests'] + cyclonedds_fail,
        empty_pre_space + ['FastRTPS Failed tests'] + fastrtps_fail,
        empty_pre_space + ['Total tests'] + total_test,
    ]


def tabulate_database(db, filter_host=None, filter_rate_limited=False, filter_rate_unlimited=False):
    tests = db["processed"]
    n_tests = 0

    rows = []

    for test in tests:
        if filter_host is not None and test['host'] != filter_host:
            continue

        if filter_rate_limited and test['rate'] == 0:
            continue

        if filter_rate_unlimited and test['rate'] != 0:
            continue

        row_template = [test[key] for key in testkeys]
        comparison_data = test['comparison']
        comparison_template = [
            status_value_strings[comparison_data['cpu_usage']],
            comparison_data['cpu_usage_diff'],
            status_value_strings[comparison_data['ram_usage']],
            comparison_data['ram_usage_diff'],
            status_value_strings[comparison_data['latency_mean']],
            comparison_data['latency_mean_diff'],
            status_value_strings[comparison_data['jitter']],
            comparison_data['jitter_diff']
        ]
        n_tests += 1

        if test['cyclonedds'] is None:
            rows.append(['rmw_cyclonedds_cpp'] + row_template + ['FAIL'] * len(datakeys) + comparison_template)
        else:
            rows.append(['rmw_cyclonedds_cpp'] + row_template + [test['cyclonedds'][key] for key in datakeys] + comparison_template)

        if test['fastrtps'] is None:
            rows.append(['rmw_fastrtps_cpp'] + row_template + ['FAIL'] * len(datakeys) + [' '] * len(comparison_template))
        else:
            rows.append(['rmw_fastrtps_cpp'] + row_template + [test['fastrtps'][key] for key in datakeys] + [' '] * len(comparison_template))

    rows.extend(summation_rows(n_tests))

    return rows
