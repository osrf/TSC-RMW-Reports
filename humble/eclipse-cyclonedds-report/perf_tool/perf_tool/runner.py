import subprocess
import datetime
import string
import random
import time
import os
import re
import sys
import platform
import uuid


def runner_for_single_process(configuration, output_dir):
    env = os.environ.copy()
    matrix = configuration["matrix"]
    exclude = configuration.get('exclude', [])
    max_runtime = configuration["runtime"]["max"]
    ignore = configuration["runtime"]["ignore"]
    cooldown = configuration["runtime"]["cooldown"]

    commands = []
    single_process_args_template = "--topic {topic} --msg {topic} --rate {rate} --num-sub-threads {subs} {extra_args} {reliability} {durability} {keep_last}{communication}"

    for topic in matrix["topics"]:
        for rate in matrix["rates"]:
            for sub in matrix["subs"]:
                for reliability in matrix["reliability"]:
                    for durability in matrix["durability"]:
                        for keep_last in matrix["keep_last"]:
                            for extra_args in matrix.get("extra_args", [""]):
                                for rmw in matrix["rmw"]:
                                    for v in exclude:
                                        if v.get('topic', topic) == topic and \
                                            v.get('subs', sub) == sub and \
                                            v.get('reliability', reliability) == reliability and \
                                            v.get('durability', durability) == durability and \
                                            v.get('keep_last', keep_last) == keep_last and \
                                            v.get('rmw', rmw) == rmw and \
                                            v.get('rate', rate) == rate:
                                            continue

                                    communication = ""
                                    if rmw == "raw_cyclonedds":
                                        communication = " --communication CycloneDDS"
                                    command = (single_process_args_template.format(
                                        topic=topic,
                                        rate=rate,
                                        subs=sub,
                                        reliability=reliability,
                                        durability=durability,
                                        keep_last=keep_last,
                                        communication=communication,
                                        extra_args=extra_args
                                    ), rmw)
                                    commands.append(command)

    print(f"The estimated runtime for singleprocess is {datetime.timedelta(seconds=(max_runtime + cooldown) * len(commands))}.")

    def runner():
        print("SINGLEPROCESS_MODE")
        for (command, rmw) in commands:
            if rmw == "raw_cyclonedds":
                env["RMW_IMPLEMENTATION"] = "rmw_cyclonedds_cpp"
            else:
                env["RMW_IMPLEMENTATION"] = rmw

            fname = str(uuid.uuid4())
            command = re.sub('\s+', ' ', command).strip()  # remove duplicated spaces
            full_command = f"ros2 run performance_test perf_test {command} --max-runtime {max_runtime} --ignore {ignore} -o csv --csv-logfile {fname}.csv"

            print(full_command)

            s = subprocess.Popen(
                full_command.split(),
                env=env,
                cwd=output_dir
            )
            pid = s.pid

            try:
                s.communicate(timeout=2*max_runtime)
            except subprocess.TimeoutExpired:
                s.terminate()
                try:
                    s.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    s.kill()

                    try:
                        if platform.system() == "Windows" and s.poll() is None:
                            # On windows we might need some extreme measures
                            subprocess.Popen(f"TASKKILL /F /PID {pid} /T").communicate(timeout=5)
                    except subprocess.TimeoutExpired:
                        print("Hopelessness!! We have an unterminated process that even windows could not squash! Despair!!")
                        sys.exit(1)

            time.sleep(cooldown)

    return runner


def runner_for_multi_process(configuration, output_dir):
    env = os.environ.copy()
    matrix = configuration["matrix"]
    exclude = configuration.get("exclude")
    max_runtime = configuration["runtime"]["max"]
    ignore = configuration["runtime"]["ignore"]
    cooldown = configuration["runtime"]["cooldown"]

    commands = []
    sub_process_args_template = "--topic {topic} --msg {topic} --rate {rate} --num-pub-threads 0 --num-sub-threads {subs} {extra_args} {reliability} {durability} {keep_last}{communication}"
    pub_process_args_template = "--topic {topic} --msg {topic} --rate {rate} --num-pub-threads 1 --num-sub-threads 0 {extra_args} {reliability} {durability} {keep_last}{communication}"

    for topic in matrix["topics"]:
        for rate in matrix["rates"]:
            for sub in matrix["subs"]:
                for reliability in matrix["reliability"]:
                    for durability in matrix["durability"]:
                        for keep_last in matrix["keep_last"]:
                            for extra_args in matrix.get("extra_args", [""]):
                                for rmw in matrix["rmw"]:
                                    for v in exclude:
                                        if v.get('topic', topic) == topic and \
                                            v.get('subs', sub) == sub and \
                                            v.get('reliability', reliability) == reliability and \
                                            v.get('durability', durability) == durability and \
                                            v.get('keep_last', keep_last) == keep_last and \
                                            v.get('rmw', rmw) == rmw and \
                                            v.get('rate', rate) == rate:
                                            continue

                                    communication = ""
                                    if rmw == "raw_cyclonedds":
                                        communication = " --communication CycloneDDS"
                                    command = (sub_process_args_template.format(
                                        topic=topic,
                                        rate=rate,
                                        subs=sub,
                                        reliability=reliability,
                                        durability=durability,
                                        keep_last=keep_last,
                                        communication=communication,
                                        extra_args=extra_args
                                    ), pub_process_args_template.format(
                                        topic=topic,
                                        rate=rate,
                                        reliability=reliability,
                                        durability=durability,
                                        keep_last=keep_last,
                                        communication=communication,
                                        extra_args=extra_args
                                    ), rmw)
                                    commands.append(command)

    print(f"The estimated runtime for multiprocess is {datetime.timedelta(seconds=(max_runtime + cooldown) * len(commands))}.")

    def runner():
        print("MULTIPROCESS_MODE")
        for (sub_command, pub_command, rmw) in commands:
            if rmw == "raw_cyclonedds":
                env["RMW_IMPLEMENTATION"] = "rmw_cyclonedds_cpp"
            else:
                env["RMW_IMPLEMENTATION"] = rmw

            fname = str(uuid.uuid4())
            sub_command = re.sub('\s+', ' ', sub_command).strip()  # remove duplicated spaces
            pub_command = re.sub('\s+', ' ', pub_command).strip()  # remove duplicated spaces
            sub_full_command = f"ros2 run performance_test perf_test {sub_command} --max-runtime {max_runtime} --ignore {ignore} -o csv --csv-logfile {fname}.csv"
            pub_full_command = f"ros2 run performance_test perf_test {pub_command} --max-runtime {max_runtime} --ignore {ignore}"

            print(sub_full_command)

            s = subprocess.Popen(
                sub_full_command.split(),
                env=env,
                cwd=output_dir
            )
            s_pid = s.pid
            p = subprocess.Popen(
                pub_full_command.split(),
                env=env,
                cwd=output_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            p_pid = p.pid

            try:
                s.communicate(timeout=2*max_runtime)
                p.communicate(timeout=2*max_runtime)
            except subprocess.TimeoutExpired:
                try:
                    s.terminate()
                except:
                    pass
                try:
                    p.terminate()
                except:
                    pass

                try:
                    s.wait(timeout=5)
                    p.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    s.kill()
                    p.kill()

                    try:
                        if platform.system() == "Windows" and s.poll() is None:
                            # On windows we might need some extreme measures
                            subprocess.Popen(f"TASKKILL /F /PID {s_pid} /T").communicate(timeout=5)
                            subprocess.Popen(f"TASKKILL /F /PID {p_pid} /T").communicate(timeout=5)
                    except subprocess.TimeoutExpired:
                        print("Hopelessness!! We have an unterminated process that even windows could not squash! Despair!!")
                        sys.exit(1)

            time.sleep(cooldown)
    return runner


def time_and_runner_for_nodes_scaling(configuration, output_dir):
    sub_process_args_template = "--topic {topic} --msg {topic} --rate {rate} --num-pub-threads 0 --num-sub-threads 1 {reliability} {durability} {keep_last}{communication}"
    pub_process_args_template = "--topic {topic} --msg {topic} --rate {rate} --num-pub-threads 1 --num-sub-threads 0 {reliability} {durability} {keep_last}{communication}"

    max_runtime = configuration["runtime"]["max"]
    ignore = configuration["runtime"]["ignore"]
    cooldown = configuration["runtime"]["cooldown"]
    nodes_min = configuration["nodes"]["min"]
    nodes_max = configuration["nodes"]["max"]
    nodes_step = configuration["nodes"]["step"]
    prefix = configuration["prefix"]
    rmw = configuration["rmw"]

    tests = list(range(nodes_min, nodes_max, nodes_step))

    total_runtime = (max_runtime + 5 + ignore + cooldown) * len(tests)
    communication = ""
    if rmw == "raw_cyclonedds":
        communication = " --communication CycloneDDS"

    sub_command = sub_process_args_template.format(communication=communication, **configuration)
    pub_command = pub_process_args_template.format(communication=communication, **configuration)

    env = os.environ.copy()
    if rmw == "raw_cyclonedds":
        env["RMW_IMPLEMENTATION"] = "rmw_cyclonedds_cpp"
    else:
        env["RMW_IMPLEMENTATION"] = rmw

    def runner():
        print("SCALING MODE (NODES)")
        for num in tests:
            sub_full_commands = [
                f"ros2 run performance_test perf_test {sub_command} --max-runtime {max_runtime} --ignore {ignore} -o csv --csv-logfile {prefix}_{num}_{node}.csv"
                for node in range(num)
            ]
            pub_full_command = f"ros2 run performance_test perf_test {pub_command} --max-runtime {max_runtime+5}"

            print(sub_full_commands[0])

            s = [subprocess.Popen(
                    full_command.split(),
                    env=env,
                    cwd=output_dir
                )
                for full_command in sub_full_commands
            ]
            p = subprocess.Popen(
                pub_full_command.split(),
                env=env,
                cwd=output_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            p_pid = p.pid

            try:
                for sub in s:
                    sub.communicate(timeout=2*max_runtime)
                p.communicate(timeout=2*max_runtime)
            except subprocess.TimeoutExpired:
                for sub in s:
                    try:
                        sub.terminate()
                    except:
                        pass
                try:
                    p.terminate()
                except:
                    pass

                try:
                    for sub in s:
                        sub.wait(timeout=5)
                    p.wait(timeout=5)
                except subprocess.TimeoutExpired:

                    try:
                        if platform.system() == "Windows":
                            # On windows we might need some extreme measures
                            for sub in s:
                                subprocess.Popen(f"TASKKILL /F /PID {sub.pid} /T").communicate(timeout=5)
                            subprocess.Popen(f"TASKKILL /F /PID {p_pid} /T").communicate(timeout=5)
                        else:
                            for sub in s:
                                sub.kill()
                            p.kill()
                    except subprocess.TimeoutExpired:
                        print("Hopelessness!! We have an unterminated process that even windows could not squash! Despair!!")
                        sys.exit(1)

                # Scaling up further is not needed if we are already getting crashes, give up
                break

            time.sleep(cooldown)
    return total_runtime, runner


def time_and_runner_for_topics_scaling(configuration, output_dir):
    sub_process_args_template = "--msg {topic} --rate {rate} --num-pub-threads 0 --num-sub-threads 1 {reliability} {durability} {keep_last}{communication}"
    pub_process_args_template = "--msg {topic} --rate {rate} --num-pub-threads 1 --num-sub-threads 0 {reliability} {durability} {keep_last}{communication}"

    max_runtime = configuration["runtime"]["max"]
    ignore = configuration["runtime"]["ignore"]
    cooldown = configuration["runtime"]["cooldown"]
    nodes_min = configuration["nodes"]["min"]
    nodes_max = configuration["nodes"]["max"]
    nodes_step = configuration["nodes"]["step"]
    prefix = configuration["prefix"]
    rmw = configuration["rmw"]

    tests = list(range(nodes_min, nodes_max, nodes_step))

    total_runtime = (max_runtime + 5 + ignore + cooldown) * len(tests)
    communication = ""
    if rmw == "raw_cyclonedds":
        communication = " --communication CycloneDDS"

    sub_command = sub_process_args_template.format(communication=communication, **configuration)
    pub_command = pub_process_args_template.format(communication=communication, **configuration)

    env = os.environ.copy()
    if rmw == "raw_cyclonedds":
        env["RMW_IMPLEMENTATION"] = "rmw_cyclonedds_cpp"
    else:
        env["RMW_IMPLEMENTATION"] = rmw

    def runner():
        print("SCALING MODE (TOPICS)")
        for num in tests:
            sub_full_commands = [
                f"ros2 run performance_test perf_test {sub_command} --topic node{node} --max-runtime {max_runtime} --ignore {ignore} -o csv --csv-logfile {prefix}_{num}_{node}.csv"
                for node in range(num)
            ]
            pub_full_commands = [
                f"ros2 run performance_test perf_test {pub_command} --topic node{node} --max-runtime {max_runtime+5}"
                for node in range(num)
            ]

            print(sub_full_commands[0])

            s = [subprocess.Popen(
                    full_command.split(),
                    env=env,
                    cwd=output_dir
                )
                for full_command in sub_full_commands
            ]
            p = [subprocess.Popen(
                    full_command.split(),
                    env=env,
                    cwd=output_dir,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                for full_command in pub_full_commands
            ]

            try:
                for sub in s:
                    sub.communicate(timeout=2*max_runtime)
                for pub in p:
                    pub.communicate(timeout=2*max_runtime)
            except subprocess.TimeoutExpired:
                for sub in s:
                    try:
                        sub.terminate()
                    except:
                        pass
                for pub in p:
                    try:
                        pub.terminate()
                    except:
                        pass

                try:
                    for sub in s:
                        sub.wait(timeout=5)
                    for pub in p:
                        pub.wait(timeout=5)
                except subprocess.TimeoutExpired:

                    try:
                        if platform.system() == "Windows":
                            # On windows we might need some extreme measures
                            for sub in s:
                                subprocess.Popen(f"TASKKILL /F /PID {sub.pid} /T").communicate(timeout=5)
                            for pub in p:
                                subprocess.Popen(f"TASKKILL /F /PID {pub.pid} /T").communicate(timeout=5)
                        else:
                            for sub in s:
                                sub.kill()
                            for pub in s:
                                pub.kill()
                    except subprocess.TimeoutExpired:
                        print("Hopelessness!! We have an unterminated process that even windows could not squash! Despair!!")
                        sys.exit(1)

                # Scaling up further is not needed if we are already getting crashes, give up
                break

            time.sleep(cooldown)
    return total_runtime, runner


def runner_for_scaling(configuration, output_dir):
    subrunners = []
    seconds = 0
    for config in configuration:
        if config["type"] == "nodes":
            secs, runner = time_and_runner_for_nodes_scaling(config, output_dir)
            seconds += secs
            subrunners.append(runner)
        elif config["type"] == "topics":
            secs, runner = time_and_runner_for_topics_scaling(config, output_dir)
            seconds += secs
            subrunners.append(runner)
        else:
            raise Exception(f"Unknown scaling type {config['type']}, should be 'nodes' or 'topics'")

    print(f"The estimated runtime for scaling is {datetime.timedelta(seconds=seconds)}.")

    def runner():
        for subrunner in subrunners:
            subrunner()

    return runner


def test_suite_run(configuration, output_dir, clean):
    si_runner = None
    mp_runner = None
    sc_runner = None

    if "singleprocess" in configuration:
        dir = os.path.join(output_dir, "SingleProcess")
        os.makedirs(dir, exist_ok=True)

        if clean:
            for file in os.listdir(dir):
                if file.endswith(".csv"):
                    os.remove(os.path.join(dir, file))

        si_runner = runner_for_single_process(configuration["singleprocess"], dir)

    if "multiprocess" in configuration:
        dir = os.path.join(output_dir, "MultiProcess")
        os.makedirs(dir, exist_ok=True)

        if clean:
            for file in os.listdir(dir):
                if file.endswith(".csv"):
                    os.remove(os.path.join(dir, file))

        mp_runner = runner_for_multi_process(configuration["multiprocess"], dir)

    if "scaling" in configuration:
        dir = os.path.join(output_dir, "Scaling")
        os.makedirs(dir, exist_ok=True)

        if clean:
            for file in os.listdir(dir):
                if file.endswith(".csv"):
                    os.remove(os.path.join(dir, file))

        sc_runner = runner_for_scaling(configuration["scaling"], dir)

    if si_runner:
        si_runner()

    if mp_runner:
        mp_runner()

    if sc_runner:
        sc_runner()
