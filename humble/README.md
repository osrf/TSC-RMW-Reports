# 2021 ROS Middleware Evaluation Report

###  October 14, 2021

### Prepared by: Katherine Scott, Chris Lalancette, Audrow Nash

# Index

* [Introduction](#Introduction)
* [Executive Summary](#ExecutiveSummary)
* [Build Farm Performance Metrics](#BuildFarm)
* [REP-2004 Code Quality Metrics](#CodeQuality)
* [GitHub User Statistics](#GitHubStats)
* [User Survey Results](#Survey)
* [Appendix](APPENDIX.md)

# DDS provider template

On August 31, 2021, the providers of DDS implementations considered for the default DDS in ROS 2 Humble Hawksbill were provided with a set of questions to answer about their implementation.
The questionnaire is available [here](dds_provider_question_template.md).

## DDS provider responses

- [rmw_fasrtps_cpp](eProsima-response.md)

- [2021 Eclipse Cyclone DDS ROS Middleware Evaluation Report with iceoryx and Zenoh](eclipse-cyclonedds-report.md)

# <a id="Introduction"></a> Introduction

# <a id="ExecutiveSummary"></a> Executive Summary

# <a id="BuildFarm"></a> Build Farm Performance Metrics

# <a id="CodeQuality"></a> REP-2004 Code Quality Metrics

## Overview and Description

Code quality is an important metric for project health.
ROS 2 has defined various levels of package quality in [REP-2004](https://ros.org/reps/rep-2004.html).
Declaring a package to be in one of those quality levels means that it meets all of the requirements for that particular quality level.
The quality level of each of the middlewares and their RMW implementation is summarized below.
For more details, the reader is encouraged to look at the corresponding source repository for each middleware or RMW, where the quality level is declared in a file named QUALITY_DECLARATION.md or similar.

## Results

| Package/Quality Metric | [Cyclone DDS](https://github.com/eclipse-cyclonedds/cyclonedds/blob/96a0374bdbb12a7d535dbc81092c3d87f2490ecb/CYCLONEDDS_QUALITY_DECLARATION.md) | [rmw_cyclonedds](https://github.com/ros2/rmw_cyclonedds/blob/2aa2cf527d079265195b2dca91bb9c82481be0c1/rmw_cyclonedds_cpp/QUALITY_DECLARATION.md) | [Fast RTPS](https://github.com/eProsima/Fast-DDS/blob/4a27fbbbeb08ad83ffa10422eeaa201017382905/QUALITY.md) | [rmw_fastrtps](https://github.com/ros2/rmw_fastrtps/blob/daeeb8c7c57eec3df0a82aaf91a1b4e94aa889e3/rmw_fastrtps_cpp/QUALITY_DECLARATION.md) |
| ---------------------- | ---------- | -------------- | -------- | ------------ |
| Current Quality Level  |      2     |      4         |    1     |     2        |
| 1. Version Policy      | 1. follows semver but major 0 is stable<br>2. current version is stable<br>3. `dds_` or `DDS_` symbols are public API, others may change<br>4. no major releases in stable allowed<br>5. no major releases in stable allowed<br>6. no major releases in stable allowed | 1. follows semver<br>2. current version < 1.0.0<br>3. 3. public API is in the rmw headers<br>4. no major releases in stable allowed<br>5. no major releases in stable allowed<br>6. no major releases in stable allowed | 1. follows semver<br>2. current version is stable<br>3. API documentation [available](https://fast-dds.docs.eprosima.com/en/latest/fastdds/api_reference/api_reference.html)<br>4. no major releases in stable allowed<br>5. only minor releases break ABI<br>6. N/A | 1. follows semver<br>2. current version is stable<br>3. public API is in the headers<br>4. no major releases in stable allowed<br>5. no major releases in stable allowed<br>6. no major releases in stable allowed |
| 2. Change control      | 1. changes must be in PR<br>2. DCO required<br>3. one review for merge (except when no reviewers available)<br>4. CI required to pass<br>5. documentation required | 1. changes must be in PR<br>2. DCO required<br>3. at least one review required for merge<br>4. CI required to pass<br>5. documentation required | 1. changes must be in a PR<br>2. DCO required<br>3. at least one review required for merge<br>4. CI required to pass<br>5. documentation required | 1. changes must be in PR<br>2. DCO required<br>3. at least one review required for merge<br>4. CI required to pass<br>5. documentation required |
| 3. Documentation       | 1. no high-level/concept documentation<br>2. API docs are embedded in the code<br>3. Eclipse Public License 2.0/Eclipse Distribution License 1.0<br>4. copyright statement included with the code | 1. features are documented via rmw API<br>2. public API docs in rmw, other API docs embedded in code<br>3. Apache 2.0 license<br>4. copyright statement included with the code | 1. features are documented<br>2. API reference is hosted at [readthedocs](https://fast-dds.docs.eprosima.com/en/latest/fastdds/api_reference/api_reference.html)<br>3. Apache 2.0 license<br>4. copyright statement included with the code | 1. some features are documented<br>2. API docs are embedded in the code<br>3. Apache 2.0 license<br>4. copyright statement included with the code |
| 4. Testing             | 1. system tests cover features<br>2. tests cover all of the public API<br>3. line coverage should increase with changes<br>4. no performance tests<br>5. uses coverity for static analysis | 1. system tests cover features<br>2. system tests cover APIs<br>3. line coverage should keep or increase, but decreases are allowed if justified<br>4. No performance tests<br>5. uses standard ROS linters and tests | 1. simulation tests cover features<br>2. tests cover typical usage of public API<br>3. line coverage should keep or increase, but decreases are allowed if justified<br>4. automatic performance test on changes<br>5. uses linters, but only for new code | 1. system tests cover features<br>2. unit and system tests cover the API<br>3. line coverage should increase with changes, but decreases allowed with justification<br>4. no performance tests<br>5. uses standard ROS linters and tests |
| 5. Dependencies        | 1. no ROS deps<br>2. no ROS deps<br>3. OpenSSL external dep | 1. all direct deps have Quality Declaration except for rosidl_typesupport_introspection_c{pp}<br>2. no optional direct runtime ROS deps<br>3. Eclipse Cyclone DDS claims to be at QL 2 | 1. no ROS deps<br>2. no ROS deps<br>3. libasio, libtinyxml2, Fast CDR, foonathan_memory, and OpenSSL* external deps | 1. all direct runtime ROS deps declare quality level<br>2. no optional direct runtime ROS deps<br>3. Fast CDR/Fast RTPS claim to be at QL 1 |
| 6. Platform            | 1. supports all ROS 2 Tier 1 platforms | 1. supports all ROS 2 Tier 1 platforms | 1. supports all ROS 2 Tier 1 platforms | 1. supports all ROS 2 Tier 1 platforms |
| 7. Security            | 1. conforms to [REP-2006](https://ros.org/reps/rep-2006.html) | 1. conforms to [REP-2006](https://ros.org/reps/rep-2006.html) | 1. [Vulnerability disclosure policy](https://github.com/eProsima/policies/blob/main/VULNERABILITY.md) | 1. Conforms to [REP-2006](https://ros.org/reps/rep-2006.html) |


\* OpenSSL dependency for Fast RTPS is optional, but used in ROS 2.

## Discussion

# <a id="GitHubStats"></a> GitHub User Statistics

# <a id="Survey"></a> User Survey Results
