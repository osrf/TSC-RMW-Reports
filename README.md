# 2020 ROS Middleware Evaluation Report DRAFT

###  October 21st, 2020

### Prepared by: Katherine Scott, William Woodall, Chris Lalancette, Dirk Thomas

# Index

1. Introduction
2. [Executive Summary](#ExecutiveSummary)
3. Build Farm Performance Metrics
4. Mininet Simulation Results
5. REP-2004 Table
6. GitHub User Statistics
7. User Survey Results
8. Appendix A: Additional Build Farm Plots
9. Appendix B: Additional Mininet Results


# Introduction

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

### 1.2.2 Memory Utilization in a Spinning Node By RMW 

![Build Farm Memory
Consumption](./galactic/plots/BuildFarmRMWMemoryConsumption.png)

![Build Farm Memory
Consumption--try 2](/galactic/plots/BuildFarmRMWMemoryConsumption.png)


## 1.3 Build Farm Test Discussion

The results between two the RMW implementations were reasonably close, particularly in light of other RMW implementations visible on the build farm. In terms of CPU utilization and memory there the Cyclone RMW performed slightly better in terms of both memory and CPU performance. The memory advantage of Cyclone was not born out by plot in 1.2.3 where FastRTPS RMW seems to outperform for all message times. In terms of message latency and message both vendors appear to perform well up until approximately the 1mb message size. For messages greater than ~1Mb Cyclone RMW has better results with lower latency and the number of messages sent. 









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
