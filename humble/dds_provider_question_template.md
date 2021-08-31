# Default DDS provider template

## Introduction
Every year, the ROS 2 TSC is mandated to choose a default RMW provider for the next ROS 2 release.
In 2021, that selection will affect Humble Hawksbill, the release scheduled for May 2022.
The default RMW provider must be a Tier 1 provider as specified in REP-2000 (https://www.ros.org/reps/rep-2000.html), and must be open-source.
For Humble Hawksbill, the two RMW providers that meet this criteria are rmw_cyclonedds_cpp and rmw_fastrtps_cpp.

In order to make an informed decision, the TSC needs to be provided with a report that has details about each of the available choices.
The report is comprised of data directly from the RMW providers, plus common language that Open Robotics provides.
This template is the series of questions that each of the RMW providers should answer for that report.
Every question listed below was submitted either by TSC members, or from members of the community based on real world usage.

Remember that the TSC and end-users mostly care about how the DDS implementation works as part of the ROS 2 system, not standalone.
Each response should be measured in context of the entire ROS 2 stack, or should be measured for both the DDS implementation and the ROS 2 stack where there is a significant difference.

It is up to the DDS provider to answer the questions in the way that they feel is best.
That includes choosing the hardware platform, the operating system, the tuning parameters, individual metrics, etc.
Keep in mind that most of the TSC members are users of ROS 2 in robotics applications, so the choices that are made should reflect that.
Choosing only high-end, cloud-connected machines, or only microcontrollers, probably does not match the day-to-day experience of ROS 2 users.
Each choice that is made should be documented, and the rationale for each choice should be explained in the responses to the question.

Each response should be as detailed, accurate, and reproducible as possible.
That means that a detailed description of how any data was collected and analyzed should be included with each answer.
Graphs are very useful and encouraged for each answer where it makes sense.
Where relevant, graphs should show the data from the same test run using rmw_cyclonedds_cpp and rmw_fastrtps_cpp.

Data should be taken using the following ros2.repos file: https://github.com/osrf/TSC-RMW-Reports/blob/main/humble/ros2.repos.
When building these packages, they must be built in the default configuration as they will be delivered in ROS 2 Humble.

When the RMW providers are ready to deliver the report (see the Relevant Dates below), they should open a pull request to the TSC repository https://github.com/osrf/TSC-RMW-Reports, targeting https://github.com/osrf/TSC-RMW-Reports/blob/main/humble/README.md.
The format of the reports should be Markdown, as that is what will be rendered by GitHub into the final report.

## Relevant Dates

* August 31, 2021 - Template is delivered from Open Robotics to ADLINK/Apex.AI and eProsima
* September 20, 2021 - First draft of template responses from ADLINK/Apex.AI and eProsima due - this is to identify any problems early
* October 4, 2021 - Final responses to the template are returned to Open Robotics from ADLINK/Apex.AI and eProsima
* October 12, 2021 - Report is delivered from Open Robotics to the ROS 2 TSC
* October 21, 2021 - Discussion of the report at the monthly TSC meeting
* October 25, 2021 through November 12, 2021 - Voting open to TSC members for default RMW provider
* November 18, 2021 - Announcement of the default RMW provider at monthly TSC meeting
* Early December, 2021 - Based on the outcome of the default RMW provider vote, any required technical changes made to the ROS 2 codebase
* May 23, 2022 - Release of Humble Hawksbill

## Questions
The length of the response to all of the questions combined should be no more than 4000 words, with as many graphs as needed to support that.
If additional space is needed, feel free to provide a link to an external resource with more information.

### Performance
* Without configuration, what is the throughput and latency (in addition to any other relevant metrics) when transferring large topics (like ~4K camera images) at medium frequencies (~30Hz)?

* Without configuration, how does the implementation scale with the number of topics in the system?

* Without configuration, how does the implementation scale with the number of nodes in the system?

* Please provide benchmarks for inter-host, inter-process (with and without LoanedMessages), and intra-process (with and without LoanedMessages) throughput for both large and small message sizes, on both Linux and Windows.

* For a pub/sub pair in separate processes, what is the average round-trip time, throughput, and CPU/memory utilization? How does this scale with topic frequency and topic size?

### Services
* Several users have reported instances where services never appear, or they never get responses. What do you think the problems might be, and what are you doing to try and address these problems?
    * https://github.com/ros2/ros2/issues/1074
    * https://github.com/ros2/rmw_fastrtps/issues/392
    * https://github.com/ros2/rmw_fastrtps/pull/418
    * https://github.com/ros2/rmw_cyclonedds/issues/74
    * https://github.com/ros2/rmw_cyclonedds/issues/191

* How do services scale with the number of clients? And/or the amount of request traffic?

### WiFi
We’ve had a lot of reports from users of problems using ROS 2 over WiFi.
What do you think the causes of the problems are, and what are you doing to try to address these problems?

* Some example issues from users:
    * https://answers.ros.org/question/362065/bad-performance-of-ros2-via-wifi/
    * https://discourse.ros.org/t/ros2-default-behavior-wifi/13460/38
    * https://discourse.ros.org/t/bad-networks-dragging-down-localhost-communication/20611

* How well does the implementation work out-of-the-box over WiFi?

* How does the system behave when a robot leaves WiFi range and then reconnects?

* How long does it take to launch a large application like RViz2 over WiFi?

* What is a solution for default DDS discovery on lossy networks?

* How does performance scale with the number of robots present in a WiFi network?

### Features
* What is the roadmap and where is it documented?

* Can the middleware be configured to be memory-static at runtime?

* What support is there for microcontrollers?

* Are there tools available for integrating/bridging with other protocols (MQTT, etc)? What are they, and how do they work?

* How much adherence is there to the RTPS standard?

* How much support for the DDS-Security specification is provided in the DDS implementation?

* Does the package have explicit tooling and support for protocol dissection?

### Quality
* What is the currently declared REP-2004 (https://www.ros.org/reps/rep-2004.html) quality of the package implementing the RTPS/DDS protocols and the RMW?

* How else does the package measure quality? Please list specific procedures or tools that are used.

* Where is the development process documented?

* What kinds of tests are run? Smoke tests, unit tests, integration tests, load tests, coverage? What platforms are each of the tests run on?

* Has the DDS Security implementation been audited by a third-party?

## Free-form

In this section, you can add any additional information that you think is relevant to your RMW implementation.
For instance, if your implementation has unique features, you can explain them here.
These should be things technical in nature, not just marketing.
Please keep your responses limited to 2000 words with a reasonable number of graphs; we’ll truncate anything longer than that during editing of the report.
If you cannot fit all of your data into the limit, feel free to provide a link to an external resource which we’ll include in the report.
