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


# <a id="ExecutiveSummary"></a> Executive Summary 


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

![Build Farm Memory
Consumption](./galactic/plots/BuildFarmRMWMemoryConsumption.png)


### 1.2.3: Subscriber CPU Utilization, Latency, and Lost Messages  By Message Type and RMW 
![Build Farm performance by message type](./galactic/plots/PerfTestVsMsgSize.png)


## 1.3 Build Farm Test Discussion

The results between two the RMW implementations were reasonably close, particularly in light of other RMW implementations visible on the build farm. In terms of CPU utilization and memory there the Cyclone RMW performed slightly better in terms of both memory and CPU performance. The memory advantage of Cyclone was not born out by plot in 1.2.3 where FastRTPS RMW seems to outperform for all message times. In terms of message latency and message both vendors appear to perform well up until approximately the 1mb message size. For messages greater than ~1Mb Cyclone RMW has better results with lower latency and the number of messages sent. 

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

![Open and closed pull requests and issues](./galactic/plots/BuildFarmRMWCPUConsumption.png )

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

rmw_cyclonedds_cpp is missing a quality declaration making it difficult to perform and apples to apples comparison between the two. Under most of the categories for the parts that are documented each implementation are comparable. Despite this there is an appreciable difference as CycloneDDS is currently declared as quality level 3, and FastRTPS is rated as quality level 2.







# Editing

You can use the [editor on GitHub](https://github.com/osrf/TSC-RMW-Reports/edit/main/README.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/osrf/TSC-RMW-Reports/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.
