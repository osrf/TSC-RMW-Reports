# 2020 ROS Middleware Evaluation Report DRAFT

###  October 21st, 2020

### Prepared by: Katherine Scott, William Woodall, Chris Lalancette, Dirk Thomas

# Index

0. [Introduction](#Introduction)
1. [Executive Summary](#ExecutiveSummary)
2. [Build Farm Performance Metrics](#BuildFarm)
3. [Mininet Simulation Results](#Mininet)
4. [REP-2004 Code Quality Metrics Table](#CodeQuality)
5. [GitHub User Statistics](#GithubStats)
6. [User Survey Results](#Survey)
7. [Discussion](#Discussion)
8. [Appendix A: Additional Build Farm Plots](#AppendixB)
9. [Appendix B: Additional Mininet Results](#AppendixA)


# Introduction <a id="Introduction"></a>

This report is intended to serve as a guide for the selection of the default ROS middleware (RMW) implementation for the ROS 2 Galactic Galapagos release. This report is intended to provide information about the Tier 1 RMW/DDS implementations along two broad axes of evaluation: application performance and community engagement. This report is intended to be purely informational and non-prescriptive; meaning this report does not make a recommendation for the default middleware.  Instead, it is an attempt to present objective data about the default RMW candidates in a neutral and factual manner. The final default ROS 2 Galactic middleware implementation will be selected by the ROS 2 Technical Steering Committee (TSC) after evaluation by both the ROS 2 Middleware Working Group and the TSC.

This report evaluates two Data Distribution Service (DDS) implementations along with their RMW implementations for ROS 2 Foxy, namely Cyclone RMW and FastRTPS RMW. These two Tier 1 ROS 2 RMW implementations along with the underlying DDS implementations are evaluated along two broad rubrics: application performance, as in the overall computational performance of the RMW, and community engagement, or how the RMW’s users perceived the utility of the RMW for their application. These two broad categories of evaluation are supported by the analysis of five recently collected datasets. The datasets collected and how they were analyzed are summarized below:

1. Build Farm Performance Data -- this dataset covers basic RMW performance in terms of memory, cpu utilization, and interoperability between RMWs using a simplified network under optimal conditions
2. Mininet Performance Data -- this data set is an initial attempt to evaluate RMW performance under simulated real-world conditions. It attempts to understand what conditions cause each RMW to fail.
3. REP-2004 Code Quality Data -- this simple table presents the REP-2004 code quality standards as implemented for both the RMW and underlying DDS implementation.
4. GitHub Engagement Data -- this section looks at GitHub community engagement data over the preceding six months for both the RMWs and DDS implementation.
5. User Survey Data -- this section presents the results of a survey of the ROS 2 community asking them about the overall end-user experience.

In collecting these datasets we made our best effort to use the most recent version of each RMW; but in many cases, particularly with outside parties, there was some variation in the implementation under test. As such, it is important to understand that these data do not represent a single snap-shot in time of each RMW implementation; instead they represent a more holistic evaluation of performance over the preceding six months. It is also important to note that many of these values may shift in the future based on implementation updates. Moreover, fixating on or overweighting a single metric in the evaluation of the RMW implementations could lead to poor outcomes, as the underlying tests are imperfect representations of the real world. This is to say that the data collected for this report are merely an imperfect sample of a moving target. Finally, please keep in mind that this report is geared towards selecting the default ROS 2 RMW. As shown by the data, most ROS users are perfectly content to change the default RMW if it addresses their use case. The core use-case for the ROS 2 RMW is as the starting point for new ROS adopters; and as such a preference should be given to the needs of this group of individuals.

Where possible we will provide the underlying data and source code for both experimentation and analysis. This process is intended to be repeated for each subsequent ROS 2 release and our hope is that it can become more automated and also serve as a community resource for selecting the best RMW for each user’s specific needs.


# Executive Summary <a id="ExecutiveSummary"></a>


# 1. Build Farm Performance Data

## 1.1 Overview and Description

The first dataset collected for evaluating RMW performance comes by way of the ROS build farm. The ROS build farm hosts a collection of small integration tests that verify that a given RMW Implementation performs acceptably when connected to either a single ROS node or a single ROS publisher sending messages to a single ROS subscriber. Within the build farm there are also interoperability tests that examine the transport of messages between pairs of RMW/DDS implementations; however these tests are outside of the scope of this report. For this section of the report we looked at the performance of three different testing regimes:

1. A single, spinning, ROS node backed by an DDS/RMW pair and instrumented to collect general performance data like mean and median CPU and memory consumption.
2. A publisher subscriber pair where the publisher and subscriber each use a different RMW implementation. These tests are  instrumented to collect basic load statistics like CPU and memory utilization. These tests are included in Appendix A.
3. A ROS publisher and subscriber pair sending messages of varying sizes and instrumented to collect both host load statistics and network performance statistics.

All metrics for this portion of the report were collected using a custom
performance metrics tool that can be found in this pull request. The Python
Jupyter notebooks for pre-processing the data and plotting data can be found
respectively
[BuildFarmDataProcessing.ipynb](https://github.com/osrf/TSC-RMW-Reports/blob/main/galactic/BuildFarmDataProcessing.ipynb)
and
[BuildFarmPlots.ipynb](https://github.com/osrf/TSC-RMW-Reports/blob/main/galactic/BuildFarmPlots.ipynb). The
post processed data can be found in the [buildfarm subdirectory](https://github.com/osrf/TSC-RMW-Reports/tree/main/galactic/data/build_farm).

## 1.2 Build Farm Test Results


The first set of data collected involved running a single, perpetually spinning ROS node a short time and collecting the peak, mean, and median, CPU and memory utilization statistics. The figures below summarize the results for both the Cyclone RMW and FastRTPS RMW in the asynchronous configuration. Full plots of all the RMW variants and configurations are available in Appendix A. The data for these plots was collected on October 14th 2020 as indicated by this build farm log. The full data set can be downloaded using this link. Summarized csv files of the data will be provided in the final report.  Figure 1.2.1 provides the CPU performance while Figure 1.2.2 provides the memory performance including virtual, resident, and physical memory allocation. Links to the source code for this test along with the analysis are available in the appendix.

A second bevy of tests were run using a single publisher and a single subscriber
communicating across a host machine while varying both the underlying RMW as
well as the message size. The publisher and subscriber were instrumented to
collect both system performance metrics and transmission metrics. We have
selected a few illustrative examples from the set to share including subscriber
CPU versus message size, messages received versus message size, and message
latency versus message size in figures 1.2.3, 1.2.4, and 1.2.5 respectively.


### 1.2.1 CPU Utilization in a Spinning Node By RMW

![Build Farm CPU Consumption](./galactic/plots/BuildFarmRMWCPUConsumption.png )

### 1.2.2 Memory Utilization in a Spinning Node By RMW

![Build Farm Memory Consumption](./galactic/plots/BuildFarmRMWMemoryConsumption.png)

### 1.2.3: Subscriber CPU Utilization, Latency, and Lost Messages By Message Type and RMW

![Build Farm performance by message type](./galactic/plots/PerfTestVsMsgSize.png)

## 1.3 Build Farm Test Discussion

The results between two the RMW implementations were reasonably close, particularly in light of other RMW implementations visible on the build farm. In terms of CPU utilization and memory there the Cyclone RMW performed slightly better in terms of both memory and CPU performance. The memory advantage of Cyclone was not born out by plot in 1.2.3 where FastRTPS RMW seems to outperform for all message times. In terms of message latency and message both vendors appear to perform well up until approximately the 1mb message size. For messages greater than \~1Mb Cyclone RMW has better results with lower latency and the number of messages sent.


# 2. Mininet Experiments

In this section, we present some details of experiments made using [mininet](http://mininet.org/) to simulate degraded network conditions.

The priority of this section and these experiments is to highlight interesting differences in either the rmw implementations or settings that can be changed within those implementations.

See Appendix B for the complete report.

## 2.1 Synchronous Versus Asynchronous Publishing

There is a significant difference in both performance and behavior when using asynchronous publishing versus synchronous publishing.
Also, there is currently an asymmetry in the default behavior of `rmw_fastrtps_cpp` and `rmw_cyclonedds_cpp` on this point.

### 2.1.1 Overview

Briefly, the different modes dictate how publishing data is handled when the user calls something like `publish(msg)`.
In asynchronous publishing, the publish call puts the message on a queue and some significant part of sending it to remote subscriptions is done in a separate thread, allowing the publish call to return quickly and generally spend a more consistent amount of time in the publish call, especially when publishing large data where serialization, sending to the network, and other tasks could take a significant amount of time.
In synchronous publishing, the publish call does much more of the work to send the message to the network within the publish call, which is often more efficient and lower latency, but can cause issues with throughput when publishing large data and can cause the publish call to block longer than might be expected.

### 2.1.2 Current Situation

Currently `rmw_fastrpts_cpp` uses asynchronous publishing by default, but it also supports synchronous publishing as well.
Currently `rmw_cyclonedds_cpp` uses synchronous publishing, and does not support asynchronous publishing, this was reported in [this](https://github.com/ros2/rmw_cyclonedds/issues/89) issue.

A proposal was made to change `rmw_fastrtps_cpp` to use synchronous publishing by default, but it was rejected by request of the ROS 2 core maintainers (see [this](https://github.com/ros2/rmw_fastrtps/pull/343#pullrequestreview-346228522) pull request).
It is possible to change `rmw_fastrtps_cpp` to use synchronous publishing using non-portable environment variables and a custom XML configuration file, which is what is used in these experiments to generate the `rmw_fastrtps_cpp sync` results, versus the `rmw_fastrtps_cpp async` results which use the default settings.

### 2.1.3 The Possible Options

This change in behavior was blocked, in part, to avoid breaking behavioral changes between ROS distributions, i.e. one version is using async by default, and the next is using sync by default.
However, with the TSC approval, we could allow `rmw_fastrtps_cpp` to default to synchronous publishing, which would be a break in default behavior, but would bring it in line with how publishing works with `rmw_cyclonedds_cpp`.

Deciding to switch the default to `rmw_cyclonedds_cpp` is implicitly making this change in default behavior, from `rmw_fasrtps_cpp` with asynchronous publishing to `rmw_cyclonedds_cpp` with synchronous publishing.

Therefore there are three related possible outcomes from this process:

- Do nothing, keep `rmw_fastrtps_cpp` as the default, keep asynchronous publishing as the default.
- Switch to `rmw_cyclonedds_cpp` as the default, implicitly changing the publishing behavior to synchronous in the process.
- Stick with `rmw_fastrtps_cpp`, but change the default publishing mode to synchronous.

### 2.1.4 Improvements to ROS 2

Ideally we would have a portable way in the ROS 2 API for users to choose which publishing mode they want.
We should add this, but it still does not address the issue of which settings to use by default, and whether or not to breaking existing behavior by changing `rmw_fastrtps_cpp` to synchronous publishing by default.

### 2.1.5 Performance and Behavior Differences

In this subsection, we will motivate why this setting matters so much and should be considered when comparing the "out-of-the-box" behavior of `rmw_fastrtps_cpp` and `rmw_cyclonedds_cpp`, and why we should be careful when considering switching the default setting for users.

#### 2.1.5.1 Impact on Performance

Asynchronous publishing can have a positive impact on throughput when publishing large data where fragmentation is involved.

This report doesn't have very good data supporting this point, but one of the purposes of this feature is to provide better performance when publishing large messages or streaming video, see Fast-DDS's documentation as an example:

[https://fast-dds.docs.eprosima.com/en/v1.8.1/advanced.html#sending-large-data](https://fast-dds.docs.eprosima.com/en/v1.8.1/advanced.html#sending-large-data)

Also this graph from the build farm's performance dataset show how CPU utilization falls off for very large messages, even though messages received is lower than synchronous in this example:

![Build Farm performance by message type](./galactic/plots/PerfTestVsMsgSize.png)

It is likely that customization of a flow controller is also required to get the optimal large data performance when used with asynchronous publishing.

Aside from the potential benefits of asynchronous publishing in certain situations, it is clear that comparing synchronous publishing in `rmw_cyclonedds_cpp` with asynchronous publishing in `rmw_fastrtps_cpp` is not a fair comparison.
The "Messages Recv" part of the graph above demonstrates this as the sync mode for the two implementations are the same curve shape and close, whereas the asynchronous mode diverges from the other two.

#### 2.1.5.2 Impact on Publish Behavior

In a situation where the bandwidth required for publishing exceeds the available bandwidth, in this case limited artificially by mininet, you can observe a difference in publish blocking behavior.

To illustrate this difference consider this experiment case:

- a single publisher publishing a "PointCloud512k" at 30Hz to a single subscription in a separate process,
- using the QoS:
  - reliable,
  - volatile, and
  - keep last with a history depth of 10, and
- using mininet to limit the bandwidth to 54Mbps.

This case is interesting because the required bandwidth exceeds the limit imposed by mininet, i.e. the message is roughly 512 kilobytes being published at 30Hz, so a rough calculation is that it would require 122Mbps to transmit all of the data (not including the overhead of transport or resent data).

In this scenario, a backlog of messages is produced and the history cache is full in the first few seconds of publishing.

To understand this point, it is also important understand how the "Messages Sent" is calculated by the publishing process.
Each time a message is published, a time stamp is recorded, the remaining time until the next publish period is calculated and the publishing thread sleeps until that time has elapsed before publishing again.
So if publishing takes a long time it can begin to impact the effective publish rate.

Consider these two series of plots comparing `rmw_fastrtps_cpp sync` and `rmw_cyclonedds_cpp sync` with varying packet loss:

<table>
  <tr>
    <td></td>
    <td>rmw_cyclonedds_cpp sync</td>
    <td>rmw_fastrtps_cpp sync</td>
  </tr>
  <tr>
    <td>Packet Loss: 0%</td>
    <td>
      <img src="galactic/data/mininet_experiments/generated_report/rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_0loss_0delay/average_sent_received.svg">
    </td>
    <td>
      <img src="galactic/data/mininet_experiments/generated_report/rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_0loss_0delay/average_sent_received.svg">
    </td>
  </tr>
  <tr>
    <td>Packet Loss: 10%</td>
    <td>
      <img src="galactic/data/mininet_experiments/generated_report/rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_10loss_0delay/average_sent_received.svg">
    </td>
    <td>
      <img src="galactic/data/mininet_experiments/generated_report/rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_10loss_0delay/average_sent_received.svg">
    </td>
  </tr>
  <tr>
    <td>Packet Loss: 20%</td>
    <td>
      <img src="galactic/data/mininet_experiments/generated_report/rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_20loss_0delay/average_sent_received.svg">
    </td>
    <td>
      <img src="galactic/data/mininet_experiments/generated_report/rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_20loss_0delay/average_sent_received.svg">
    </td>
  </tr>
  <tr>
    <td>Packet Loss: 30%</td>
    <td>
      <img src="galactic/data/mininet_experiments/generated_report/rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_30loss_0delay/average_sent_received.svg">
    </td>
    <td>
      <img src="galactic/data/mininet_experiments/generated_report/rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_30loss_0delay/average_sent_received.svg">
    </td>
  </tr>
  <tr>
    <td>Packet Loss: 40%</td>
    <td>
      <img src="galactic/data/mininet_experiments/generated_report/rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_40loss_0delay/average_sent_received.svg">
    </td>
    <td>
      <img src="galactic/data/mininet_experiments/generated_report/rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_40loss_0delay/average_sent_received.svg">
    </td>
  </tr>
</table>

As you can see, the publishing rate does not meet the target of 30 per second, but are fairly consistent between the two implementations.

An oddity is that as the packet loss increases, the effective publishing rate increases as well, approaching the desired rate of 30.

Note that these plots show both individual runs (with reduced alpha) and averages of those 10 runs (solid lines).
The dotted lines are averages rates for the entire run.

Now consider these two series of plots between `rmw_fastrtps_cpp async` and `rmw_fastrtps_cpp sync`:

<table>
  <tr>
    <td></td>
    <td>rmw_fastrtps_cpp async</td>
    <td>rmw_fastrtps_cpp sync</td>
  </tr>
  <tr>
    <td>Packet Loss: 0%</td>
    <td>
      <img src="galactic/data/mininet_experiments/generated_report/rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_0loss_0delay/average_sent_received.svg">
    </td>
    <td>
      <img src="galactic/data/mininet_experiments/generated_report/rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_0loss_0delay/average_sent_received.svg">
    </td>
  </tr>
  <tr>
    <td>Packet Loss: 10%</td>
    <td>
      <img src="galactic/data/mininet_experiments/generated_report/rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_10loss_0delay/average_sent_received.svg">
    </td>
    <td>
      <img src="galactic/data/mininet_experiments/generated_report/rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_10loss_0delay/average_sent_received.svg">
    </td>
  </tr>
  <tr>
    <td>Packet Loss: 20%</td>
    <td>
      <img src="galactic/data/mininet_experiments/generated_report/rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_20loss_0delay/average_sent_received.svg">
    </td>
    <td>
      <img src="galactic/data/mininet_experiments/generated_report/rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_20loss_0delay/average_sent_received.svg">
    </td>
  </tr>
  <tr>
    <td>Packet Loss: 30%</td>
    <td>
      <img src="galactic/data/mininet_experiments/generated_report/rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_30loss_0delay/average_sent_received.svg">
    </td>
    <td>
      <img src="galactic/data/mininet_experiments/generated_report/rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_30loss_0delay/average_sent_received.svg">
    </td>
  </tr>
  <tr>
    <td>Packet Loss: 40%</td>
    <td>
      <img src="galactic/data/mininet_experiments/generated_report/rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_40loss_0delay/average_sent_received.svg">
    </td>
    <td>
      <img src="galactic/data/mininet_experiments/generated_report/rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_40loss_0delay/average_sent_received.svg">
    </td>
  </tr>
</table>

Notice in the async case that the publish rate almost achieves the desired 30Hz, whereas the publish rate for sync is clamped to the capacity of the network almost immediately.
The publish rate for async is quite noisy, which is something we could investigate further, but the average is quite close the desired goal.

This can be a very serious issue if the user's code is designed under the assumption that publishing is always relatively quick, which is a likely assumption for ROS 1 users (ROS 1 behaved most similarly to asynchronous publishing in ROS 2) or for users thinking that "keep last" will just replace messages in the history cache if there's a backlog.
We can document this behavior, but the impact is quite subtle and could lead to hard to diagnose problems in user's applications.

This example was intended to demonstrate why it is important to be cautious when changing this behavior for all users.

## 2.2

### 2.2.1 Experiments with Lost Packets or Latency at 54Mbs Bandwidth

![Build Farm performance by message type](./galactic/plots/PoorPerformersBW54.png)

### 2.2.2 Experiments with Lost Packets or Latency at 300Mbs Bandwidth

![Build Farm performance by message type](./galactic/plots/PoorPerformersBW300.png)

### 2.2.3 Experiments with Lost Packets or Latency at 1000Mbs Bandwidth

![Build Farm performance by message type](./galactic/plots/PoorPerformersBW1000.png)

# 3. Github Engagement Statistics

## 3.1 Overview and Statistics

Responsiveness to issues and pull requests in a Github repository is a good
proxy measurement for how quickly a given vendor responds to their customer and
users. The number of pull requests, and how quickly they are closed also give an
indication to how much development is taking place on a given code base and how
quickly issues are being resolved. To examine the responsiveness and development
velocity of both RMW vendors we used the github API to collect commit, pull
request, and issue data for the 180 days before the report was drafted on
10/17/2020. The process of collecting this data was divided into two part, data
collection which can be found in [this
notebook](./galactic/GetGitRMWDDSMetrics.ipynb), and data analysis which can be [found here](./galactic/PlotGithubStats.ipynb).

## 3.2 Github Engagement Results

### 3.2.1 Open and Closed Pull Requests in the Previous Six Months

![Open and closed pull requests and issues](./galactic/plots/PullRequestsAndIssues.png )

### 3.2.2 Cumulative Time to Close Pull Requests and Issues

![Time to close pull requests and issues](./galactic/plots/IssueAndPRTurnAround.png)

# 3.3 Github Metrics Discussion

Generally, for the six month period sampled, both vendors are doing a great job responding to both issues and pull requests. In terms of RMW layers the vendors have only small differences, with Fast being slightly faster closing issues and tickets for their RMW layer. Fast DDS also appears to be under heavier development with almost three times the number of pull requests during the previous six months. It is unclear if this is caused by an increased number of ROS users, increased feature deployment, or addressing bugs and issues.

# 4. Code Quality Metrics

## 4.1 Overview and Description

Code quality is an important metric for project health.  ROS 2 has defined various levels of package quality in [REP-2004](https://ros.org/reps/rep-2004.html).  Declaring a package to be in one of those quality levels means that it meets all of the requirements for that particular quality level.  The quality level of each of the middlewares and their RMW implementation is summarized below.  For more details, the reader is encouraged to look at the corresponding source repository for each middleware or RMW, where the quality level is declared in a file named QUALITY_DECLARATION.md or similar.

## 4.2 Results

| Package/Quality Metric | [cyclonedds](https://github.com/ros2/rmw_cyclonedds/blob/3fa62f4f8fa9b3cc624879e9c085ad19aa9c1977/CYCLONEDDS_QUALITY_DECLARATION.md) | cyclonedds RMW | [FastRTPS](https://github.com/eProsima/Fast-DDS/blob/08100416cd82950cafd37ce8b34c3a0cc02b3ba2/QUALITY.md) | [FastRTPS RMW](https://github.com/ros2/rmw_fastrtps/blob/4e0fce977c993f840b013c444d603842fb39ad64/rmw_fastrtps_cpp/QUALITY_DECLARATION.md) |
| ---------------------- | ---------- | -------------- | -------- | ------------ |
| Current Quality Level  |      3     |      N/A       |    2     |     2            |
| 1. Version Policy      | 1. follows semver by major 0 is stable<br>2. current version is stable<br>3. `dds_` or `DDS_` symbols are public API, others may change<br>4. no major releases in stable allowed<br>5. no major releases in stable allowed<br>6. no major releases in stable allowed | N/A | 1. follows semver<br>2. current version is stable<br>3. API documentation [available](https://fast-dds.docs.eprosima.com/en/latest/fastdds/api_reference/api_reference.html)<br>4. no major releases in stable allowed<br>5. only minor releases break ABI<br>6. N/A | 1. follows semver<br>2. current version is stable<br>3. public API is in the headers<br>4. no major releases in stable allowed<br>5. no major releases in stable allowed<br>6. no major releases in stable allowed |
| 2. Change control      | 1. changes must be in PR<br>2. DCO required<br>3. one review for merge (except when no reviewers available<br>4. CI required to pass<br>5. documentation required | N/A | 1. changes must be in a PR<br>2. DCO required<br>3. at least one review required for merge<br>4. CI required to pass<br>5. documentation required | 1. changes must be in PR<br>2. DCO required<br>3. at least one review required for merge<br>4. CI required to pass<br>5. documentation required |
| 3. Documentation       | 1. no high-level/concept documentation<br>2. API docs are embedded in the code<br>3. Eclipse Public License 2.0/Eclipse Distribution License 1.0<br>4. copyright statement included with the code | N/A | 1. all features are documented<br>2. API reference is hosted at [readthedocs](https://fast-dds.docs.eprosima.com/en/latest/fastdds/api_reference/api_reference.html)<br>3. Apache 2.0 license<br>4. copyright statement included with the code | 1. all features are documented<br>2. API docs are embedded in the code<br>3. Apache 2.0 license<br>4. copyright statement included with the code |
| 4. Testing             | 1. system tests cover features<br>2. tests cover all of the public API<br>3. line coverage should increase with changes<br>4. no performance tests<br>5. uses coverity for static analysis | N/A | 1. simulation tests cover features<br>2. tests cover typical usage of public API<br>3. best-effort line coverage increase with changes<br>4. automatic performance test on changes<br>5. uses linters, but only for new code | 1. system tests cover features<br>2. tests cover all of the API<br>3. line coverage should increase with changes<br>4. no performance tests<br>5. uses standard ROS linters and tests |
| 5. Dependencies        | 1. no ROS dependencies<br>2. no ROS dependencies<br>3. OpenSSL external dependency | N/A | 1. no ROS dependencies<br>2. no ROS dependencies<br>3. libasio, libtinyxml2, fast-cdr, foonathan_memory, and OpenSSL* external dependencies | 1. all direct runtime ROS deps at some level<br>2. no optional direct runtime ROS deps<br>3. fastcdr/fastrtps claim to be at QL 2 |
| 6. Platform            | 1. supports all ROS 2 Tier 1 platforms | N/A | 1. supports all ROS 2 Tier 1 platforms | 1. supports all ROS 2 Tier 1 platforms |
| 7. Security            | 1. conforms to [REP-2006](https://ros.org/reps/rep-2006.html) | N/A | 1. [Vulnerability disclosure policy](https://github.com/eProsima/policies/blob/main/VULNERABILITY.md) | 1. Conforms to [REP-2006](https://ros.org/reps/rep-2006.html) |


\* OpenSSL dependency for Fast-RTPS is optional, but used in ROS 2.

## 4.3 Discussion

rmw_cyclonedds_cpp is missing a quality declaration making it difficult to perform an apples to apples comparison between the two. Under most of the categories for the parts that are documented each implementation are comparable. Despite this there is an appreciable difference as CycloneDDS is currently declared as quality level 3, and FastRTPS is rated as quality level 2.

# Section 5: Community

## 5.1 Overview and Description

The final component of this document is a user survey on ROS user’s feelings about their selected RMW implementation conducted between September 17th and October 16th 2020. The survey was posted to ROS Discourse and provided ROS 2 users with a chance to rate the performance of their RMW as well as give a narrative description of their experience. In conjunction with this evaluation data we also asked participants to provide basic demographic data and perform a self assessment of their skills. In total there 96 responses with 31 users reporting that they use Cyclone RMW and 60 users reporting they use FastRTPS RMW. All of the respondents were ROS 2 users with nearly three quarters of them presently working with ROS 2 Foxy. The users sampled come from a wide variety of backgrounds, industries and work on a variety of different projects.

In the following section we summarize the data and where possible provide the descriptive statistics for both RMWs as well for the ROS community. Section 5.1.1 summarizes the questions given to participants that are referenced by the plots in 5.2. There is summary of the results in 5.3 with a selection of user narrative responses included in section 5.4

## 5.1.1 Survey Question Summary

Survey participants were asked a total of nineteen questions related to their
RMW experience, which each of the questions listed below along with a question
number to reference them in the graphs in section 5.2. Survey participants were
allowed to respond with one of the following: "Strongly Agree", "Agree",
"Neutral", "Disagree", "Strongly Disagree", and "Not Applicable". For plotting
the results the written scores were translated to numerical values with,
"Strongly Agree" being given a score of 5, and "Strongly Disagree" being given a
score of 1. Users who selected "Not Applicable" were not included in the final
results.


- Q1: My current RMW worked out of the box for my application.
- Q2: I understand how RMWs work.
- Q3: I am capable of changing my RMW easily.
- Q4: I would/have considered changing my RMW implementation.
- Q5: Open Robotics provides sufficient information for me to make a sound RMW selection.
- Q6: My current RMW implementation provides sufficient support.
- Q7: My current RMW implementation provides sufficient  documentation.
- Q8: My current RMW implementation provides sufficient debugging tools.
- Q9: My current RMW implementation provides sufficient features for my application.
- Q10: My current RMW implementation provides sufficient performance for my application.
- Q11: I am considering or have considered changing my current RMW implementation due to technical challenges.
- Q12: DDS/RMWs have improved the overall ROS experience.
- Q13: I would advocate for my current RMW to be the default ROS 2.
- Q14: I would recommend my current RMW to a friend.
- Q15: My RMW interoperates well with other systems.
- Q16: Based on the out-of-the-box experience I would recommend ROS2 Foxy to a friend.
- Q17: ROS should continue to use DDS as the default RMW implementation.
- Q18: I consider my current RMW implementation robust, reliable, and ready for production.

## 5.2 RMW User Survey Results

### 5.2.1 Survey Participant Demographic Information

![Survey Demographic Information by RMW](./galactic/plots/SurveyCohorts.png)

### 5.2.2 Survey Participant Skill Self Assesment

![Survey participant skill self assesment](./galactic/plots/SurveySkillReport.png)


### 5.2.3 Survey Response Data by RMW

![Survey Question Response Data](./galactic/plots/SurveyResponses.png)


### 5.2.4 Survey Question Drill Down 1

![Survey Drill Down 1](./galactic/plots/SurveyDrillDown1.png)


### 5.2.5 Survey Question Drill Down 2

![Survey Drill Down 1](./galactic/plots/SurveyDrillDown2.png)


## 5.3 Survey Discussion

We feel that we were able to collect a large and representative sample of the ROS community for this survey with a sufficient number of users for each RMW included in the final report. The respondents to the survey represent a wide swath of ROS 2 users with the preponderance of responses coming from ROS 2 Foxy Fitzroy users. These respondents reported a wide range of skill levels and varying degrees of competency in debugging, networking, and ROS development skills. What is remarkable about the responses is how uniform they were on most questions relating to their selected RMW vendor. The difference between most of the responses varies by no more than 5% for most of the questions.

Questions one, two, and three are leader questions that help us understand the ROS 2 community’s understanding of ROS middleware. By and large ROS 2 users, using both RMWs, say that they understand how RMWs work, how to change them, and that their current RMW worked out of the box for them. However, Cyclone RMW users are slightly more likely to understand RMWs. Question four asks if a given user has changed their RMW, and unsurprisingly Cyclone RMW users are much more likely to have considered changing their RMW. Question five, “Does Open Robotics provide sufficient information to make a sound RMW selection” received on average a neutral response indicating we could do more to support the community. For questions six, seven, and eight, most users, from both RMWs, feel they have sufficient support, documentation, and debugging tools. Question nine asks if the selected RMW has sufficient features, and Cyclone RMW users believe it performs slightly better in this category.

Question ten shows that Cyclone RMW users believe that they have sufficient performance for their application, but the difference is small, only 6%.
Question eleven, “I am considering changing or have changed my RMW due to technical challenges” is interesting because the responses are nearly uniform between the two RMWs. In question twelve we find that ROS users generally agree that DDS RMWs have improved the overall ROS experience. Question thirteen asks respondents if they would recommend their RMW as the default, to which Cyclone RMW users have a more positive response. Similarly, question fourteen asks is the user would recommend their RMW to a friend, and a slightly higher percentage of Cyclone RMW users would do so. This question is very similar to the “net promoter score” used by product managers to understand customer attitudes towards a product.  Most of the remaining questions are fairly similar results except for question eighteen, “I consider my current RMW implementation robust, reliable, and ready for production.” Question eighteen had a slightly higher positive response rate from Cyclone RMW users.

All in all, Cyclone RMW rated more favorably among its users, but only very slightly so.

## 5.4 Survey Narrative Responses

We provided a space in the user survey for respondents to communicate their feelings about their preferred middleware to the TSC, While not a formal evaluation, the experience of individuals is worth considering given our limited testing capabilities. The full list of responses will be provided to the TSC if requested. We have included a few of these excerpts in this document to capture the spirit of all the responses.


### 5.4.1 Cyclone User Responses

```
“CycloneDDS has been more consistent with outputting the expected
performance. The test we ran show that in many different scenarios CycloneDDS is
able to work without a hitch, while Fast DDS's performance outperforms
CycloneDDS in some scenarios it completely fails in others (100+ nodes in a
distributed setup over VPN).”

	                                      -- A ROS 2 Foxy user
```


```
“Right now, I would advocate for Cyclone DDS, with FastDDS still being a
relatively close second. I think FastDDS works for most users in most use-cases,
particularly users who may not be working in commercial/industrial environments,
such as university labs or personal projects, but I have had both performance
and reliability issues with it relating to discovery, implementation of DDS
features, sending of large-data, and more, which Cyclone fully resolved for
me. License-wise, they are both agreeable options.”

	                                      -- A ROS 2 Foxy user
```



``` markdown
“CycloneDDS is the best. Only CycloneDDS can remote use rviz2 over Wi-Fi to
 control the AMR doing navigation with Navigation2.”

	                                      -- A ROS 2 Foxy user
```



```
“I would definitely advocate for a default RMW (and even further for only a
single supported RMW). As for which one, I don't have a strong opinion, but I
would be biased to cyclonedds simply because they seem extremely willing to
engage with the community and to be responsive to its needs.”

	                                      -- A ROS 2 Foxy user
```
