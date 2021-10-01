import numpy as np
from enum import Enum


def verify_numerical_sequence(data, subtype, operation):
    try:
        converted = [subtype(v) for v in data]
    except:
        return None

    for c in converted:
        if np.isnan(c) or np.isinf(c):
            return None

    return subtype(operation(converted))


def test_results(data, host, subs):
    data = data.copy()

    ind = []
    for i, recv in enumerate(data['received']):
        if int(recv.strip()) == 0:
            ind.append(i)

    if len(ind) > 0.75 * len(data['received']):
        # if more than 75% of data entries are empty reject
        return None

    for key in data.keys():
        subdata = data[key]
        for index in reversed(ind):
            del subdata[index]
        data[key] = subdata

    received = verify_numerical_sequence(data['received'], int, np.sum)
    if received is None or received == 0:
        return None

    sent = verify_numerical_sequence(data['sent'], int, np.sum)
    if sent is None:
        return None

    lost = verify_numerical_sequence(data['lost'], int, np.sum)
    if lost is None:
        return None

    data_received = verify_numerical_sequence(data['data_received'], int, np.sum)
    if data_received is None:
        return None

    latency_min = verify_numerical_sequence(data['latency_min'], float, np.min)
    if latency_min is None:
        return None

    latency_max = verify_numerical_sequence(data['latency_max'], float, np.max)
    if latency_max is None:
        return None

    latency_mean = verify_numerical_sequence(data['latency_mean'], float, np.mean)
    if latency_mean is None:
        return None

    latency_variance = verify_numerical_sequence(data['latency_variance'], float, np.mean)
    if latency_variance is None:
        return None

    cpu_usage = verify_numerical_sequence(data['cpu_usage'], float, np.mean)
    if cpu_usage is None:
        return None

    ram_usage = verify_numerical_sequence([data['ru_maxrss'][-1]], float, np.mean)
    if ram_usage is None:
        return None

    ram_usage /= 1000.0

    if 'mac' in host.lower():
        # for some reason getrusage() on mac returns bytes
        ram_usage /= 1024.0


    return {
        'received': received,
        'sent': sent,
        'lost': lost,
        'data_received': data_received,
        'latency_min': latency_min,
        'latency_max': latency_max,
        'latency_mean': latency_mean,
        'latency_variance': latency_variance,
        'jitter': np.sqrt(latency_variance + 0.000001),
        'cpu_usage': cpu_usage,
        'rel_cpu_usage': cpu_usage / float(received),
        'ram_usage': ram_usage,
        'length': len(data['data_received']),
        'throughput': data_received / 1024.0 / 1024.0 / float(len(data['data_received'])) / float(subs)
    }


class Status(Enum):
    CYCLONEDDS_WIN = 1
    FASTRTPS_WIN = 2
    FASTRTPS_FAIL = 3
    CYCLONEDDS_FAIL = 4


def make_comparison(cyclonedds, fastrtps):
    if cyclonedds is None:
        return {
            'cpu_usage': Status.CYCLONEDDS_FAIL.value,
            'cpu_usage_diff': 0,
            'rel_cpu_usage': Status.CYCLONEDDS_FAIL.value,
            'rel_cpu_usage_diff': 0,
            'ram_usage': Status.CYCLONEDDS_FAIL.value,
            'ram_usage_diff': 0,
            'latency_mean': Status.CYCLONEDDS_FAIL.value,
            'latency_mean_diff': 0,
            'jitter': Status.CYCLONEDDS_FAIL.value,
            'jitter_diff': 0,
            'throughput': Status.CYCLONEDDS_FAIL.value,
            'throughput_diff': 0
        }
    if fastrtps is None:
        return {
            'cpu_usage': Status.FASTRTPS_FAIL.value,
            'cpu_usage_diff': 0,
            'rel_cpu_usage': Status.FASTRTPS_FAIL.value,
            'rel_cpu_usage_diff': 0,
            'ram_usage': Status.FASTRTPS_FAIL.value,
            'ram_usage_diff': 0,
            'latency_mean': Status.FASTRTPS_FAIL.value,
            'latency_mean_diff': 0,
            'jitter': Status.FASTRTPS_FAIL.value,
            'jitter_diff': 0,
            'throughput': Status.FASTRTPS_FAIL.value,
            'throughput_diff': 0
        }

    result = {}

    for var in ['cpu_usage', 'rel_cpu_usage', 'ram_usage', 'latency_mean', 'jitter']:
        if cyclonedds[var] < fastrtps[var]:
            result[var] = Status.CYCLONEDDS_WIN.value
            result[f"{var}_diff"] = fastrtps[var] / (cyclonedds[var] + 0.000001)
        else:
            result[var] = Status.FASTRTPS_WIN.value
            result[f"{var}_diff"] = cyclonedds[var] / (fastrtps[var] + 0.000001)

    for var in ['throughput']:
        if cyclonedds[var] > fastrtps[var]:
            result[var] = Status.CYCLONEDDS_WIN.value
            result[f"{var}_diff"] = cyclonedds[var] / (fastrtps[var] + 0.000001)
        else:
            result[var] = Status.FASTRTPS_WIN.value
            result[f"{var}_diff"] = fastrtps[var] / (cyclonedds[var] + 0.000001)

    return result


def boolify(x):
    return x if type(x) == bool else x.lower().strip() in ['1', 'true']

def process_results(database):
    data = database["raw"]
    results = []

    # This monstrous iteration will ensure that our results are ordered nicely
    for host, hdata in sorted(data.items()):
        for mode, mdata in sorted(hdata.items()):
            for topic, tdata in sorted(mdata.items()):
                for rate, rtdata in sorted(tdata.items(), key=lambda x: int(x[0])):
                    for subs, sdata in sorted(rtdata.items(), key=lambda x: int(x[0])):
                        for zero_copy, zcdata in sorted(sdata.items(), key=lambda x: boolify(x[0])):
                            for reliable, rldata in sorted(zcdata.items(), key=lambda x: boolify(x[0])):
                                for transient, trdata in sorted(rldata.items(), key=lambda x: boolify(x[0])):
                                    cyclonedds = test_results(trdata["cyclonedds"], host, subs) if "cyclonedds" in trdata else None
                                    fastrtps = test_results(trdata["fastrtps"], host, subs) if "fastrtps" in trdata else None
                                    raw = test_results(trdata["raw_cyclonedds"], host, subs) if "raw_cyclonedds" in trdata else None

                                    if cyclonedds is None and fastrtps is None and raw is None:
                                        # No point saving it if both fail
                                        continue

                                    results.append({
                                        "host": host,
                                        "mode": mode,
                                        "topic": topic,
                                        "rate": int(rate),
                                        "subs": int(subs),
                                        "zero_copy": boolify(zero_copy),
                                        "reliable": boolify(reliable),
                                        "transient": boolify(transient),
                                        "cyclonedds": cyclonedds,
                                        "fastrtps": fastrtps,
                                        "raw": raw,
                                        "comparison": make_comparison(cyclonedds, fastrtps)
                                    })

    database["processed"] = results