def confgen():
    return {
        "singleprocess": {
            "runtime": {
                "max": 30,
                "ignore": 5,
                "cooldown": 5
            },
            "matrix": {
                "topics": [
                    "Array16k",
                    "Array2m",
                    "Struct32k",
                    "Struct16",
                    "PointCloud1m",
                    "PointCloud4m",
                    "PointCloud8m"
                ],
                "rates": [0, 20, 100, 500],
                "subs": [1, 3, 10],
                "reliability": ["--reliable"],
                "durability": [""],
                "keep_last": ["--keep-last --history-depth 100"],
                "rmw": ["rmw_cyclonedds_cpp", "rmw_fastrtps_cpp"]
            },
            "exclude": [
                {"topic": "Array2m", "subs": 10},
                {"topic": "PointCloud4m", "subs": 10},
                {
                    "topic": "PointCloud4m",
                    "rate": 500,
                    "reliability": "--reliable",
                    "durability": "--transient",
                    "subs": 1,
                },
                {"topic": "PointCloud1m", "rate": 500, "subs": 3},
                {"topic": "PointCloud4m", "rate": 500, "subs": 3},
                {"topic": "PointCloud8m", "rate": 500, "subs": 3},
                {"topic": "PointCloud1m", "rate": 0, "subs": 3},
                {"topic": "PointCloud1m", "rate": 500, "subs": 10},
                {"topic": "PointCloud4m", "rate": 500, "subs": 10},
                {"topic": "PointCloud8m", "rate": 500, "subs": 10},
                {"topic": "PointCloud1m", "rate": 0, "subs": 10},
                {"topic": "PointCloud4m", "rate": 0},
                {"topic": "PointCloud8m", "rate": 0},
                {
                    "topic": "Array2m",
                    "rate": "500",
                    "subs": "3",
                    "reliability": "--reliable",
                },
                {"topic": "Struct32k", "subs": 10, "rate": 500},
            ],
        },
        "multiprocess": {
            "runtime": {
                "max": 30,
                "ignore": 5,
                "cooldown": 5
            },
            "matrix": {
                "topics": [
                    "Array16k",
                    "Array2m",
                    "Struct32k",
                    "Struct16",
                    "PointCloud1m",
                    "PointCloud4m",
                ],
                "rates": [0, 20, 100, 500],
                "subs": [1, 3, 10],
                "reliability": ["--reliable"],
                "durability": [""],
                "keep_last": ["--keep-last --history-depth 100"],
                "rmw": ["rmw_cyclonedds_cpp", "rmw_fastrtps_cpp"],
                "extra_args": ["", "--zero-copy"]
            },
            "exclude": [
                {"topic": "Array2m", "subs": 10},
                {"topic": "PointCloud4m", "subs": 10},
                {
                    "topic": "PointCloud4m",
                    "rate": 500,
                    "reliability": "--reliable",
                    "durability": "--transient",
                    "subs": 1,
                },
                {"topic": "PointCloud1m", "rate": 500, "subs": 3},
                {"topic": "PointCloud4m", "rate": 500, "subs": 3},
                {"topic": "PointCloud8m", "rate": 500, "subs": 3},
                {"topic": "PointCloud1m", "rate": 0, "subs": 3},
                {"topic": "PointCloud1m", "rate": 500, "subs": 10},
                {"topic": "PointCloud4m", "rate": 500, "subs": 10},
                {"topic": "PointCloud8m", "rate": 500, "subs": 10},
                {"topic": "PointCloud1m", "rate": 0, "subs": 10},
                {"topic": "PointCloud4m", "rate": 0},
                {"topic": "PointCloud8m", "rate": 0},
                {
                    "topic": "Array2m",
                    "rate": "500",
                    "subs": "3",
                    "reliability": "--reliable",
                },
                {"topic": "Struct32k", "subs": 10, "rate": 500},
            ],
        },
        "scaling": [
            {
                "prefix": "cyclone_nodes_",
                "runtime": {
                    "max": 40,
                    "ignore": 5,
                    "cooldown": 15
                },
                "topic": "Struct16",
                "type": "nodes",
                "nodes": {"min": 1, "max": 61, "step": 3},
                "rate": 500,
                "reliability": "",
                "durability": "",
                "keep_last": "--keep-last --history-depth 100",
                "rmw": "rmw_cyclonedds_cpp"
            },
            {
                "prefix": "fast_nodes_",
                "runtime": {
                    "max": 40,
                    "ignore": 5,
                    "cooldown": 15
                },
                "topic": "Struct16",
                "type": "nodes",
                "nodes": {"min": 1, "max": 61, "step": 3},
                "rate": 500,
                "reliability": "",
                "durability": "",
                "keep_last": "--keep-last --history-depth 100",
                "rmw": "rmw_fastrtps_cpp"
            },
            {
                "prefix": "cyclone_topics_",
                "runtime": {
                    "max": 40,
                    "ignore": 5,
                    "cooldown": 15
                },
                "topic": "Struct16",
                "type": "topics",
                "nodes": {"min": 1, "max": 61, "step": 3},
                "rate": 500,
                "reliability": "",
                "durability": "",
                "keep_last": "--keep-last --history-depth 100",
                "rmw": "rmw_cyclonedds_cpp"
            },
            {
                "prefix": "fast_topics_",
                "runtime": {
                    "max": 40,
                    "ignore": 5,
                    "cooldown": 15
                },
                "topic": "Struct16",
                "type": "topics",
                "nodes": {"min": 1, "max": 61, "step": 3},
                "rate": 500,
                "reliability": "",
                "durability": "",
                "keep_last": "--keep-last --history-depth 100",
                "rmw": "rmw_fastrtps_cpp"
            }
        ],
    }
