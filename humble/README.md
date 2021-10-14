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
* [DDS Provider Responses](#DDSProviderResponses)
* [Appendix](APPENDIX.md)

# <a id="Introduction"></a> Introduction

This report is intended to serve as a guide for the selection of the default ROS middleware (RMW) implementation for the ROS 2 Humble Hawksbill release.
It provides information about the qualifying Tier 1 RMW implementations through objective application performance from the ROS 2 buildfarm, community engagement data, and through response to a questionnaire given to each of the RMW providers.
The report is intended to be purely informational and non-prescriptive; meaning it does not make a recommendation for the default middleware.
The default ROS 2 Humble middleware implementation will be selected by the ROS 2 Technical Steering Committee (TSC) after evaluation by both the ROS 2 Middleware Working Group and the TSC.

In order to be considered for this report, RMW implementations needed to meet a minimum bar:

1. It is considered a Tier 1 implementation in [REP-2000](https://www.ros.org/reps/rep-2000.html)
1. Both the RMW implementation and and the middleware it depends on are open-source projects under a permissive license
1. It is based on a middleware that uses RTPS or is a DDS implementation

Two RMW implementations currently meet this minimum bar: `rmw_cyclonedds_cpp` based on Eclipse Cyclone DDS and `rmw_fastrtps_cpp` based on Fast RTPS.
From here on out, Cyclone DDS will be used synonymously with `rmw_cyclonedds_cpp` and Fast RTPS will be used synonymously with `rmw_fastrtps_cpp` unless otherwise specified.
Note that Fast RTPS is now known as Fast DDS, but for historical reasons this report will continue to refer to it as Fast RTPS.
This report evaluates these two DDS implementations along with their RMW implementations for ROS 2.

The application performance and community engagement is measured objectively by Open Robotics along 4 axes:

* [Build Farm Performance Metrics](#BuildFarm) - this dataset covers basic RMW performance in terms of memory, CPU utilization, and lost messages using a simplified network under optimal conditions
* [REP-2004 Code Quality Data](#CodeQuality) - this simple table represents the [REP-2004](https://www.ros.org/reps/rep-2004.html) code quality standards as implemented for both the RMWs and DDS implementations
* [GitHub User Statistics](#GitHubStats) - this section looks at GitHub community engagement data over the preceding six months for both the RMWs and DDS implementations
* [User Survey Results](#Survey) - this section presents the results of a survey of the ROS 2 community asking about the overall end-user experience

In the [DDS Provider Reponses](#DDSProviderResponse) section, each of the RMW providers were asked a series of questions that are current concerns of the ROS 2 TSC.
The questionnaire that was provided is available [here](dds_provider_question_template.md).
The responses from the providers are necessarily biased, and because the hardware and software used for each providers response is different, no direct comparison is possible.
However, the manner in which the providers responded to the questionnaire should give some insights into how they are thinking about the problems that ROS 2 users are facing.

# <a id="ExecutiveSummary"></a> Executive Summary

This section will attempt to summarize the most important parts from each of the sections in this report.

In [Section 1](#-1-build-farm-performance-metrics), the plots in [1.2.1](#121-cpu-utilization-in-a-spinning-node-by-rmw) and [1.2.2](#122-memory-utilization-in-a-spinning-node-by-rmw) show nearly identical performance between Cyclone DDS and Fast RTPS with synchronous publishing.
However, comparing the results to the [2020 report](../galactic/README.md), it is clear that both implementations now use more CPU and more memory than before.

Also in [Section 1](#-1-build-farm-performance-metrics), plots in [1.2.3](#123-subscriber-cpu-utilization-latency-and-lost-messages-by-message-type-and-rmw) show Fast RTPS with synchronous publishing to be the best implementation, having the same shape to the curve as message size increases, but with a better score in each case.
Note, these plots show only a single run of the performance tests each, as they come from a single night of the nightly performance jobs.
They also show clear trade-offs between synchronous and asynchronous publishing modes.

In [Section 2](#-2-rep-2004-code-quality-metrics), adherence to [REP-2004](https://www.ros.org/reps/rep-2004.html) is compared.
The implementations are quite similar, despite some inconsistencies in the reporting due to differences in self reporting.
Under most of the categories for the parts that are documented each implementation are comparable.
Despite this there is a difference as Cyclone DDS is currently declared as quality level 2 and Fast RTPS is declared as quality level 1.

In [Section 3](#-3-github-user-statistics), data from GitHub about the two vendor's repositories is compared, and we see similar results.
Issues are handled in a timely fashion for the most part, and those that are not could be special cases.
It is difficult to draw a meaningful conclusion from the data available.

In [Section 4](#-4-user-survey-results) the user survey results are presented,
and there is a slight advantage for Cyclone DDS as highlighted in the plots for
section [4.2.2] and [4.2.3](#625-survey-question-drill-down-2). Generally
speaking, more users recommend that the TSC adopt Cyclone as the default, and
users who have tried both implementations prefer Cyclone DDS over Fast
RTPS. However, FastDDS has a slightly higher mean net promoter score (both RMWs
have a high median net promoter score). Keep in mind that this survey relies on
self reporting which could bias the results

In [Section 5](#-5-dds-provider-responses), the responses to the DDS provider survey are presented.
There are potential sources of bias which may affect this result due to the fact that it relies on self reporting.
The editors mention several points they found interesting while reading the reports.

# <a id="BuildFarm"></a> 1. Build Farm Performance Metrics

## 1.1 Overview and Description

The first dataset collected for evaluating RMW performance comes by way of the [ROS build farm](http://build.ros2.org). The ROS build farm hosts a collection of small integration tests that verify that a given RMW implementation performs acceptably when connected to either a single ROS node or a single ROS publisher sending messages to a single ROS subscriber.
Within the build farm there are also interoperability tests that examine the transport of messages between pairs of RMW/DDS implementations; however these tests are outside of the scope of this report.
For this section of the report we looked at the performance of two different testing regimes:

1. A single, spinning, ROS node backed by an DDS/RMW pair and instrumented to collect general performance data like mean and median CPU and memory consumption.
1. A ROS publisher and subscriber pair sending messages of varying sizes and instrumented to collect both host load statistics and network performance statistics.

All metrics for this portion of the report were collected using a custom [performance metrics tool](https://github.com/ahcorde/buildfarm_perf_tests/tree/master/test).
The Python Jupyter notebooks for pre-processing the data and plotting data can be found respectively [BuildFarmDataProcessing.ipynb](https://github.com/osrf/TSC-RMW-Reports/blob/main/humble/notebooks/BuildFarmDataProcessing.ipynb) and [BuildFarmPlots.ipynb](https://github.com/osrf/TSC-RMW-Reports/blob/main/humble/notebooks/BuildFarmPlots.ipynb).
The raw and post-processed data can be found in the [build_farm subdirectory](https://github.com/osrf/TSC-RMW-Reports/tree/main/humble/notebooks/data/build_farm).

## 1.2 Build Farm Test Results

The first set of data collected involved running a single, perpetually spinning ROS node a short time and collecting the peak, mean, and median, CPU and memory utilization statistics.
The figures below summarize the results for the Cyclone DDS RMW in synchronous configuration and Fast RTPS RMW in both the synchronous and asynchronous configuration.
Full plots of all the RMW variants and configurations are available in [Appendix A](APPENDIX.md#appendix_a).
The data for these plots was collected on August 31, 2021, and can be [downloaded using this link](http://build.ros2.org/job/Rci__nightly-performance_ubuntu_focal_amd64/387/artifact/ws/test_results/buildfarm_perf_tests/*.csv/*zip*/buildfarm_perf_tests.zip).
Summarized csv files can be found in the [data directory for the build farm test results](https://github.com/osrf/TSC-RMW-Reports/tree/main/humble/notebooks/data/build_farm).
Figure 1.2.1 provides the CPU performance while Figure 1.2.2 provides the memory performance including virtual, resident, and physical memory allocation.

A second bevy of tests were run using a single publisher and a single subscriber communicating across a host machine while varying both the underlying RMW as well as the message size.
The publisher and subscriber were instrumented to collect both system performance metrics and transmission metrics.
We have selected a few illustrative examples from the set to share including subscriber CPU versus message size, messages received versus message size, and message latency versus message size in figure 1.2.3.

### 1.2.1 CPU Utilization in a Spinning Node By RMW

This plot shows the CPU usage of a single, empty spinning node.
The node being empty means that it has no publishers, subscribers, services, actions, or timers attached.
Thus, this is a test of just the overhead of a node. The 95% CPU measurement indicates the 95% percentile (i.e. peak) CPU utilization of the node.

![Build Farm CPU Consumption](./notebooks/plots/BuildFarmRMWCPUConsumption.png )

### 1.2.2 Memory Utilization in a Spinning Node By RMW

This plot shows the memory usage of a single, empty spinning node.
The node being empty means that it has no publishers, subscribers, services, actions, or timers attached.
Thus, this is a test of just the overhead of a node.
The 95% memory measurement indicates the 95% percentile (i.e. peak) memory utilization of the node.

![Build Farm Memory Consumption](./notebooks/plots/BuildFarmRMWMemoryConsumption.png)

### 1.2.3 Subscriber CPU Utilization, Latency, and Lost Messages By Message Type and RMW

In this plot, 1000 messages of the specified size were sent between a publisher and subscriber on the same machine.
For each message size, the plots show how many messages out of 1000 were received by the publisher, the average latency to receive each of the messages, and the average CPU utilization to receive the messages.
For this plot, Quality of Service options of best-effort, keep last, and a depth of 10 were used.

![Build Farm performance by message type](./notebooks/plots/PerfTestVsMsgSize.png)

## 1.3 Build Farm Test Discussion

In the empty spinning node case, both RMW implementations are reasonably close in terms of CPU usage and memory consumption.
However, comparing the results to the [2020 report](../galactic/README.md), it is clear that both implementations now use more CPU and more memory than before.

In terms of messages received both RMW implementations appear to perform well up until the 1MB message size.
After that point, we see a divergence in the implementations.
Cyclone DDS starts dropping messages at the 2MB size, and continues to drop more messages as the size increases.
Fast RTPS async drops a small number of messages at the 1MB and 2MB size, but starts dropping a large number of messages after that.
Fast RTPS sync mode receives all messages up until 4MB size, and starts dropping messages after that.
It should be noted that compared to the [2020 report](../galactic/README.md), both implementations now deal with 2MB sizes better than before, with Fast RTPS showing a larger improvement.

For the message received latency, both RMW implementations are approximately the same up until the PointCloud512k message size.
Starting at the 1MB message size, the latency with Cyclone DDS approximately doubles for each step up in size.
Starting at the 1MB message size, the latency with Fast RTPS async goes up slowly until the 4MB size, where it spikes dramatically.
Fast RTPS sync has the best results here, with latency slowly increasing until the final test.
Compared to the [2020 report](../galactic/README.md), Cyclone DDS sync and Fast RTPS async are approximately the same, with Fast RTPS sync showing a noticeable improvement.

Finally, for CPU usage all of the RMW implementations are about the same until the 60k message size.
After that, the Cyclone DDS CPU usage goes up quickly with the amount of data being sent, spiking at the 2MB size and then lowering from there.
The Fast RTPS async CPU usage spikes at 2MB, and then starts going down a lot more dramatically.
In both of those cases, that is likely happening because more messages are being dropped after 2MB.
The Fast RTPS sync CPU usage goes up at the PointCloud512k size, drops dramatically for the 1MB, 2MB, and 4MB sizes, and then spikes again for the 8MB size.
This is an unexpected result, since CPU usage should increase as the data size goes up.
This may be a measurement error or other problem in that particular test.
Compared to the [2020 report](../galactic/README.md), Cyclone DDS sync and Fast RTPS async are approximately the same, with Fast RTPS sync showing a very different performance curve.

# <a id="CodeQuality"></a> 2. REP-2004 Code Quality Metrics

## 2.1 Overview and Description

Code quality is an important metric for project health.
ROS 2 has defined various levels of package quality in [REP-2004](https://ros.org/reps/rep-2004.html).
Declaring a package to be in one of those quality levels means that it meets all of the requirements for that particular quality level.
The quality level of each of the middlewares and their RMW implementation is summarized below.
For more details, the reader is encouraged to look at the corresponding source repository for each middleware or RMW, where the quality level is declared in a file named QUALITY_DECLARATION.md or similar.

## 2.2 Results

| Package/Quality Metric | [Cyclone DDS](https://github.com/eclipse-cyclonedds/cyclonedds/blob/96a0374bdbb12a7d535dbc81092c3d87f2490ecb/CYCLONEDDS_QUALITY_DECLARATION.md) | [rmw_cyclonedds_cpp](https://github.com/ros2/rmw_cyclonedds/blob/2aa2cf527d079265195b2dca91bb9c82481be0c1/rmw_cyclonedds_cpp/QUALITY_DECLARATION.md) | [Fast RTPS](https://github.com/eProsima/Fast-DDS/blob/4a27fbbbeb08ad83ffa10422eeaa201017382905/QUALITY.md) | [rmw_fastrtps_cpp](https://github.com/ros2/rmw_fastrtps/blob/daeeb8c7c57eec3df0a82aaf91a1b4e94aa889e3/rmw_fastrtps_cpp/QUALITY_DECLARATION.md) |
| ---------------------- | -------------- | -------------- | -------------- | -------------- |
| Current Quality Level  |        2       |       4        |        1       |        2       |
| 1. Version Policy      | 1. follows semver but major 0 is stable<br>2. current version is stable<br>3. `dds_` or `DDS_` symbols are public API, others may change<br>4. no major releases in stable allowed<br>5. no major releases in stable allowed<br>6. patch releases allowed, minor allowed after assessing ABI stability, major releases allowed if accompanied by `rmw_cyclonedds_cpp` update | 1. follows semver<br>2. current version < 1.0.0<br>3. public API is in the rmw headers<br>4. no major releases in stable allowed<br>5. no major releases in stable allowed<br>6. no major releases in stable allowed | 1. follows semver<br>2. current version is stable<br>3. API documentation [available](https://fast-dds.docs.eprosima.com/en/latest/fastdds/api_reference/api_reference.html)<br>4. no major releases in stable allowed<br>5. only minor releases break ABI<br>6. N/A | 1. follows semver<br>2. current version is stable<br>3. public API is in the headers<br>4. no major releases in stable allowed<br>5. no major releases in stable allowed<br>6. no major releases in stable allowed |
| 2. Change control      | 1. changes must be in PR<br>2. DCO required<br>3. one review for merge (except when no reviewers available)<br>4. CI required to pass<br>5. documentation required | 1. changes must be in PR<br>2. DCO required<br>3. at least one review required for merge<br>4. CI required to pass<br>5. documentation required | 1. changes must be in a PR<br>2. DCO required<br>3. at least one review required for merge<br>4. CI required to pass<br>5. documentation required | 1. changes must be in PR<br>2. DCO required<br>3. at least one review required for merge<br>4. CI required to pass<br>5. documentation required |
| 3. Documentation       | 1. concept documentation refers to DDS spec<br>2. API docs are embedded in the code<br>3. Eclipse Public License 2.0/Eclipse Distribution License 1.0<br>4. copyright statement included with the code | 1. features are documented via rmw API<br>2. public API docs in rmw, other API docs embedded in code<br>3. Apache 2.0 license<br>4. copyright statement included with the code | 1. features are documented<br>2. API reference is hosted at [readthedocs](https://fast-dds.docs.eprosima.com/en/latest/fastdds/api_reference/api_reference.html)<br>3. Apache 2.0 license<br>4. copyright statement included with the code | 1. some features are documented<br>2. API docs are embedded in the code<br>3. Apache 2.0 license<br>4. copyright statement included with the code |
| 4. Testing             | 1. system tests cover features<br>2. tests cover all of the public API<br>3. line coverage should increase with changes<br>4. manual and nightly performance tests<br>5. uses coverity for static analysis | 1. system tests cover features<br>2. system tests cover APIs<br>3. line coverage should keep or increase, but decreases are allowed if justified<br>4. No performance tests<br>5. uses standard ROS linters and tests | 1. simulation tests cover features<br>2. tests cover typical usage of public API<br>3. line coverage should keep or increase, but decreases are allowed if justified<br>4. automatic performance test on changes<br>5. uses linters, but only for new code | 1. system tests cover features<br>2. unit and system tests cover the API<br>3. line coverage should increase with changes, but decreases allowed with justification<br>4. no performance tests<br>5. uses standard ROS linters and tests |
| 5. Dependencies        | 1. no ROS deps<br>2. no ROS deps<br>3. OpenSSL* external dep | 1. all direct deps have Quality Declaration except for rosidl_typesupport_introspection_c{pp}<br>2. no optional direct runtime ROS deps<br>3. Eclipse Cyclone DDS claims to be at QL 2 | 1. no ROS deps<br>2. no ROS deps<br>3. libasio, libtinyxml2, Fast CDR, foonathan_memory, and OpenSSL* external deps | 1. all direct runtime ROS deps declare quality level<br>2. no optional direct runtime ROS deps<br>3. Fast CDR/Fast RTPS claim to be at QL 1 |
| 6. Platform            | 1. supports all ROS 2 Tier 1 platforms | 1. supports all ROS 2 Tier 1 platforms | 1. supports all ROS 2 Tier 1 platforms | 1. supports all ROS 2 Tier 1 platforms |
| 7. Security            | 1. conforms to [REP-2006](https://ros.org/reps/rep-2006.html) | 1. conforms to [REP-2006](https://ros.org/reps/rep-2006.html) | 1. [Vulnerability disclosure policy](https://github.com/eProsima/policies/blob/main/VULNERABILITY.md) | 1. Conforms to [REP-2006](https://ros.org/reps/rep-2006.html) |


\* OpenSSL dependency for Cyclone DDS and Fast RTPS is optional, but used in ROS 2.

## 2.3 Discussion

Compared to last year, Cyclone DDS now has a Quality Level defined for `rmw_cyclonedds_cpp`.

The packages implementing the DDS/RTPS protocol (`Cyclone DDS` and `Fast RTPS`) are comparable in most respects.
The key differences seem to be:

* Cyclone DDS relies on the OMG DDS standard for documenting the features, while Fast RTPS has dedicated documentation
* Cyclone DDS does not have automated performance tests, while Fast RTPS does
* Cyclone DDS conforms to REP-2006 for security vulnerability reporting, while Fast RTPS has its own, largely equivalent, security process

The packages implementing the interface to ROS 2 (`rmw_cyclonedds_cpp` and `rmw_fastrtps_cpp`) are generally comparable.
Here are some of the key differences:

* `rmw_cyclonedds_cpp` has a major version number < 1, while `rmw_fastrtps_cpp` has a major version number > 1
* `rmw_cyclonedds_cpp` features are documented via the `rmw` API, while `rmw_fastrtps_cpp` relies on the README, the `rmw` docs, and the `Fast RTPS` docs
* `rmw_cyclonedds_cpp` is missing a Quality Declaration for the `rosidl_typesupport_introspection_c{pp}` dependency, while `rmw_fastrtps_cpp` has a Quality Declaration for all dependencies

As a reminder, all of the quality levels for the various packages are self-declared.

# <a id="GitHubStats"></a> 3. GitHub User Statistics

## 3.1 Overview and Statistics

Responsiveness to issues and pull requests in a GitHub repository is a good proxy measurement for how quickly a given provider responds to their customers and
users.
The number of pull requests, and how quickly they are closed, can also give us an indication to how much development is taking place on a given code base and how quickly issues are being resolved.
To examine the responsiveness and development velocity of both RMW providers we used the GitHub API to collect commit, pull request, and issue data for the 180 days before the report was drafted on October 11, 2021.
The process of collecting this data was divided into two parts, data collection which can be found in [this notebook](./notebooks/GetGitRMWDDSMetrics.ipynb), and data analysis which can be [found here](./notebooks/PlotGithubStats.ipynb).

## 3.2 GitHub Engagement Results

### 3.2.1 Open and Closed Pull Requests in the Previous Six Months

The following plot gives the open and closed issues and pull requests broken down by both DDS implementation and RMW implementation.

![Open and closed pull requests and issues](./notebooks/plots/PullRequestsAndIssues.png )

### 3.2.2 Cumulative Time to Close Pull Requests and Issues

These cumulative histograms give the percentage of issues and pull requests closed within a certain time frame over the 180 day sample period.

![Time to close pull requests and issues](./notebooks/plots/IssueAndPRTurnAround.png)

## 3.3 GitHub Metrics Discussion

Generally, for the six month period sampled, both providers are doing a great job responding to both issues and pull requests.
Both the main Cyclone DDS repository and the RMW implementation are slightly faster to close issues and pull requests than the Fast RTPS equivalents.
Fast RTPS has about 1.5 times as many pull requests and issues as Cyclone DDS.
This may be down to a number of factors, including the development practices, the number of ROS users, addressing bugs and feature requests, etc.

# <a id="Survey"></a> 4. User Survey Results


## 4.1 Overview


This section of the report is a  user survey on ROS users' feelings about their selected RMW implementation conducted between October 6th and 13th 2021. The survey was posted to ROS Discourse and provided ROS 2 users with a chance to rate the performance of their RMW as well as give a narrative description of their experience. In total there were 88 responses with 47 users reporting that they use Cyclone DDS  and 41 users reporting they use Fast RTPS. Nearly all of the respondents were ROS 2 users with approximately 85% of them presently working with ROS 2 Foxy or Galactic.

In the following section we summarize the data and where possible provide the descriptive statistics for both RMWs as well for the ROS community. Section 4.2 gives a summary of the results and section 4.3 includes excerpts of narratives submitted by ROS 2 users.

## 4.2 Overall Survey Results

For our 2021 ROS 2 User Survey we asked participants to self report the both the version of ROS they used and their preferred DDS implementation. These data are summarized in plot 4.2.1.

### 4.2.1 ROS Distro and Preferred DDS Vendor
![ROS 2 Distro used by the Respondents broken down by preferred DDS implementation](./notebooks/plots/ROS2Version.png)

More than half of all respondents are currently using ROS 2 Foxy Fitzroy, the current LTS ROS 2 Release, with another 40% using either ROS 2 Galactic or ROS 2 Rolling Ridley. A small minority continue to use ROS 2 Dashing, or Eloquent or do not use ROS 2. These results  were fairly consistent across DDS vendors.

This year's survey was extremely direct and asked respondents which DDS vendor they would recommend to the ROS 2 TSC as the Humble default. Each respondent was asked to select their preferred vendor and also to submit their confidence in that selection on scale from one to ten (1 -- low confidence, 10 -- high confidence). These results are summarized in figure 4.2.2.


### 4.2.2 Vendor Recommendation and Confidence Score
![Preferred DDS Implementation and Confidence in that Decision](./notebooks/plots/ROS2Choice.png)

Based on the user feedback there was a slight preference for Cyclone DDS (47 responses vs. 41 responses) with the Cyclone users also being slightly more confident in their choice. 

In our survey we asked each community member if they had tried both DDS vendors before making their recommendation to the TSC. These data are captured in figure 4.2.3. 

### 4.2.3 Percentage of Users Who Tried both Tier One DDS Vendors
![Percentage of Respondents who Tried both DDS Implementations and the Outcome](./notebooks/plots/SwitchChoice.png)

Slightly less than two thirds of those responding to the survey had tried both Tier 1 DDS vendors. Of those who tried both vendors the majority of them decided to use Cyclone DDS as their default DDS implementation. 

Our survey also tried to gauge the net promoter score of each Tier 1 DDS implementation. A [net promoter score](https://en.wikipedia.org/wiki/Net_promoter_score) is a market research metric that asks a user, "On a scale of one to ten, how likely are you to recommend this product to a friend." A histogram of net promoter scores for each Tier 1 DDS Vendor is provided in figure 4.2.4.

### 4.2.4 Histogram of Net Promoter Scores
![Net Promoter Score Histogram](./notebooks/plots/DDSNPS.png)

The histograms of both Tier 1 DDS Vendors are fairly similar, with the majority of users scoring their DDS implementation highly. Both vendors have a median score of 9, but Fast RTPS has a slightly higher mean score of 8.93 compared to Cyclone DDS's score 8.53. 


## Section 4.3 Narrative Responses from ROS 2 Users

	
### 4.3.1 How Do Users Evaluate DDS Vendors

In our survey we asked participants to discuss how they evaluated the Tier 1 DDS vendors, below are some of their responses. 

Some users were concerned with the communities behind the development (this sentiment was echoed in a number of responses. 

```
At this stage, CycloneDDS and FastDDS are similar enough from a technical and
performance standpoint that my evaluation has shifted more towards a qualitative
evaluation of the organizations/developers behind the implementation,
particularly with respect to how eager and responsive the developers are to
accommodating the needs and requests of the community. I should note that we
still internally use RTI Connext as our "mission critical/battle hardened" DDS
vendor of choice for the most important components of our stack (these being
pure DDS and not ROS2-based), having almost eight years of experience and
success with their product.
```

Other survey participants used their CI systems to evaluate performance. Here is one such example:


```
[We] simply monitoring the pass/fail rates and test flakyness of [our] CI over
the matrix of RMW vendors. Feel free to review the historic trend on our nigh At
this stage, CycloneDDS and FastDDS are similar enough from a technical and
performance stantly job matrix.
```


Many users simply tried both vendors, like this user.

```
[We] monitored performance of dds implementations and made several PR
contributions to both of them. Compared DDS implementations in different use
cases (multi process shared memory, multiple network interfaces, etc)
```



	

### 4.3.2 Cyclone DDS Users 

Our survey asked Cyclone users what they thought about Cyclone DDS and why they think it should be the default. One user claimed the out of the box experience wasn't great. 

```
I have 100% confidence in Cyclone as a middleware. I have encountered a few
instances of customers complaining about inconsistent message delivery from
their laptops. Every single time this has been the case, those customers have
been running fast instead of Cyclone (since it is the default), and it is always
fixed immediately when changing to Cyclone.
```

Other users claimed that they have had success in production with Cyclone, like this user. 

```
We have been using this DDS implementation at scale (100 AMR over unreliable
wifi) for over a year with next to no issue. In comparison, we have used
FastRTPS in the past with a lot of issues.
```

Multiple users preferred using Cyclone because of its feature set and its open-source model. 

```
I like that it is open-source (like ROS) and that the developers are accessible,
responsive, and very interested to learn about and accommodate your
application. I also think the integration of Iceoryx will be game-changing for
how we write ROS code.
```


### 4.3.3 Fast RTPS Users 

Our survey also asked Fast RTPS users what they liked about Fast RTPS and why they thought it should be the default. Many users claimed that the code quality was much better, like the user below.

```
Fastdds is a production level DDS implementation. Performance is good, but what
strikes the most is the quality of its code. It's maintained through a serious
review process, it's easy to look and add features. The code does not contain
hacks or subtleties. There are a lot of documentation and examples."_
```

Other users claimed that the Fast RTPS development road map made software development easier:

```
One of our requirements is to ensure data persistency and right now only Fast
DDS have this feature implemented. Cyclone DDS was not an option for the
moment. Their roadmap published last year said that it would be available soon
and I would have liked to test it and do some benchmarking, but I don't think it
has been released yet.
```

Finally, some Fast RTPS users just thought the performance was just better. 


```
It [Fast RTPS] turns out to be both more stable and faster in our benchmarks.
```


### 4.3.4 What Caused Users to Switch to Cyclone DDS

For ROS users who switched to Cyclone DDS from Fast RTPS we asked them what motivated that change. The survey asked, "Before you go, is there anything you would like to tell the ROS 2 TSC about your experience with **Fast RTPS**? Did you switch DDS vendors? If so, why?"


For some users the switch was motivated by unpatched bugs.

```
We switched from fastdds to cyclonedds as after an official foxy release in the beginning of the year, there was a serious bug in released fastdds version related to a memory transport in a discovery daemon (if I remember correctly)

```

Several users reported issues with crashing services that were fixed by switching to Cyclone.

```
Crashing services; RMW or DDS layer exceptions being thrown; generally unreliable and requiring significant DDS configuration file customization to get reasonable behavior for mobile robot systems. Several tickets filed in Nav2 which were trivially solved for users by switching the Cyclone 
```

Other users thought the performance differences were negligible but the developer experience with Cyclone was much better. 

```
Experience with the actual products has been about the same. Experience with the personnel at FastDDS has been awful. 
```

Other users had difficulties  with installation and concerns about the complexity of using FastDDS. 

```
I experienced less problems during the installation and troubleshooting with Cyclone DDS than Fast RTPS. Moreover, Cyclone DDS is more lightweight in our target platforms.
```


### 4.3.4 What Caused Users to Switch to Fast RTPS


For ROS users who switched from Cyclone DDS from Fast RTPS we asked them what motivated that change. The survey asked,  "Before you go, is there anything you would like to tell the ROS 2 TSC about your experience with **Cyclone DDS**  Did you switch DDS vendors? If so, why?"



For some users the switch was motivated by performance issues.

```
In most cases Cyclone DDS was working well, but we had some strange behaviors, stability 
issues (apparently losing some packets) and found out its performance not as good as FastDDS.
```


Other users thought the performance between the two vendors were similar but had concerns about code quality.

```
I tested and evaluated Cyclone DDS in detail. Despite its performance being
better than Fastdds in some metrics, I wouldn't base a product on it. The code
is quite messy and basically maintained and developed by a single person. It
still lacks many features wrt fastdds and it looks like support for new features
always results in increasing exponentially the complexity of the
code. Cyclonedds is definitely very promising, but it shouldnt be a default
implementation until it goes through a deep cleanup and refactor to be easier to
debug and more scalable. The amount of documentation is also very small and this
makes it extremely hard to try and use some of its features.
```

For other users the choice was based on the availability of certain features. 


```
I am interested in contributing ROS2 APIs that enable productive connectivity to
5G networks. I switched to Fast RTPS because they were the only ones who
implemented support for 5G network connectivity API called "unique network
flows" that are part of Galactic.

```

Some users thought that the documentation and support for Fast RTPS was much better. 

```
We tried to switch to cyclone when we run into some issues with our
containerization, however, there were other problems with Cyclone as
well. Furthermore, we got more quick support from FastDDS, which also pointed us
out to their documentation which was quite extensive.

```



# <a id="DDSProviderResponses"></a> 5. DDS provider responses

## 5.1 Overview

As previously mentioned, each of the candidate DDS providers was given a [questionnaire](dds_provider_question_template.md) to respond to.
The questions provided all came from TSC members, and represent a subset of the concerns facing the ROS 2 community.
The responses from each of the providers is below:

* [2021 Eclipse Cyclone DDS ROS Middleware Evaluation Report with iceoryx and Zenoh](eclipse-cyclonedds-report.md)

* [Fast RTPS TSC RMW report 2021](eProsima-response.md)

## 5.2 Discussion

The two reports were taken with different hardware by different people at different times.
*Additionally, the Fast RTPS response is using [this ros2.repos](./ros.repos) file from August 31, 2021, while the Cyclone DDS response is using Galactic Patch Release 1.*
All of these factors mean that the two reports are not directly comparable in any meaningful sense.
The reader is encouraged to look at the way in which the providers answered the concerns coming from the community.
This can give insight into how, and how much, a provider is thinking about any particular issue.

Since the two reports are vastly different, a detailed comparison will not be provided here.
Here are some interesting points the editors noticed while reading the reports:

* Looking at the provider responses, Cyclone DDS answered all of the questions.  Fast RTPS answered all of the questions except for the one that says "How well does the implementation work out-of-the-box over WiFi?".

* For the performance scaling tests, the Cyclone DDS plots show up to 50 subscribers, while the Fast DDS ones only show up to 10 subscribers.

* In terms of memory usage, both of the reports agree that Fast RTPS has higher memory usage in the usual cases.  According to the eProsima report, this is because Fast RTPS support more configurations and options.

* Service scalability is hampered because neither has Content Filtering, but that is on the roadmap for both.

* For the WiFi answers, both providers mentioned that additional configuration is needed in order to make WiFi work better.  In the Fast RTPS case, this is by either providing a list of Initial Peer node (through XML configuration), or by setting up a Discovery Server.  In the Cyclone DDS case, this is by deploying Zenoh to deal with WiFi communications in a different way.
