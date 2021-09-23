# Fast DDS TSC RMW report 2021

* [Performance](#performance)
* [Services](#services)
* [WiFi](#wifi)
* [Features](#features)
* [Benchmarking](#benchmarking)

## Performance

The complete description of the benchmark executed on Fast DDS can be found on section [Benchmarking](#benchmarking).
The answers to these questions are taken from the result of this benchmark.

### Without configuration, what is the throughput and latency (in addition to any other relevant metrics) when transferring large topics (like ~4K camera images) at medium frequencies (~30Hz)?

We are assuming here an intra-process communication, since the inter-process one is addressed in a following question.

According to the benchmark, we found that with the default configuration and the given size and frequencies,
none of the implementations saturate the throughput, so we repeated the tests
increasing the data size and frequency to get the maximum throughput estimation.

According to the tests, both implementations have similar latencies, but Fast DDS achieves around double the throughput for high data rates.
There is also no significant difference on CPU usage between both implementations.

### Without configuration, how does the implementation scale with the number of topics in the system?

Both implementation have similar latency and throughput degradation with the increase of topics in the system.

### Without configuration, how does the implementation scale with the number of nodes in the system?

Regardless of the implementation, performance degrades mostly with the number of nodes subscribed to the same topic.
It is expected that the latency increases and that the throughput decreases with the number of subscribers.
Both implementations increase latency at similar rate with each added subscriber. However, throughput in Cyclone falls faster than in Fast DDS.

Both implementations keep the memory usage stable regardless of the number of subscribers.
And although CPU usage increases with the number of subscribers, they both keep similar values in all cases.


### Please provide benchmarks for inter-host, inter-process (with and without LoanedMessages), and intra-process (with and without LoanedMessages) throughput for both large and small message sizes, on both Linux and Windows.

For a complete description of the benchmark and the resulting conclusions, see section [Benchmarking](#benchmarking).

### For a pub/sub pair in separate processes, what is the average round-trip time, throughput, and CPU/memory utilization? How does this scale with topic frequency and topic size?

In order to get comparable results for inter - and intra-process communication, we are sticking here to the 4k, 30Hz traffic defined in the first question.
With the default configuration in inter-process communication, Fast DDS gets better latency and throughput than Cyclone.
Also CPU usage is lower with Fast DDS than Cyclone.
Both implementations keep the memory usage stable regardless of the number of subscribers or nodes.


## Services

We found there are two kinds of problems with services: requests that are lost during the service discovery phase and the scalability with the number of clients.

### Service discovery

Service discovery relies on the discovery of the request/reply topics.
However, both topics are discovered asynchronously, so it is possible that the request topic entities are matched while the response entities are not fully matched yet.
In this situation, if the client makes a request, the response will be lost.
We already proposed a possible solution to this in https://github.com/ros2/rmw_fastrtps/pull/418.
Summarizing, this solution proposes that the request publisher sends the GUID of its corresponding response subscriber,
and the server will hold a list of pending requests that will be answered only when the response subscriber has been discovered.
This solution requires RMW implementations to agree how the GUID is going to be sent, to avoid interoperability issues.

### Scalability with the number of subscribers

Services scaling poorly with the number of subscribers is a consequence of the design of the services themselves.
Since the response topic is unique, no matter which client made the request, services send the response to all clients, even if they are not interested on it.


## WiFi

### How does the system behave when a robot leaves WiFi range and then reconnects?

The result depends on whether the robot keeps the IP address or not. 
If the robot keeps its IP address, the robot will be able to reconnect to the other nodes. Otherwise, the nodes in the robot will need to be relaunched.

### How long does it take to launch a large application like RViz2 over WiFi?

You can find a complete analysis of the discovery performance of Fast DDS over WiFi [here](https://www.eprosima.com/index.php/resources-all/scalability/fast-rtps-discovery-mechanisms-analysis).

### What is a solution for default DDS discovery on lossy networks?

Problems with discovery over WiFi come mostly as a result of the multicast discovery traffic.

In order to minimize the multicast traffic, Fast DDS only uses multicast for the PDP by default, switching to unicast communication for EDP.

Additionally, Fast DDS provides solutions to avoid multicast discovery:

 * [Configuring initial peers](https://fast-dds.docs.eprosima.com/en/latest/fastdds/use_cases/wifi/initial_peers.html) so that the node can set unicast communication with them.
   This way, the use of multicast is not needed to discover these peers. If all the peers are known and configured beforehand, all multicast communication can be removed.
   
 * Using a [Discovery server](https://fast-dds.docs.eprosima.com/en/latest/fastdds/use_cases/wifi/discovery_server_use_case.html),
   a DomainParticipant with a well-know address that provides the rest of the participants the information required to connect among them using unicast connections.

### How does performance scale with the number of robots present in a WiFi network?

You can find a complete analysis of the discovery performance of Fast DDS over WiFi [here](https://www.eprosima.com/index.php/resources-all/scalability/fast-rtps-discovery-mechanisms-analysis).



## Features

### What is the roadmap and where is it documented?

You can find the roadmap [here](https://github.com/eProsima/Fast-DDS/blob/master/roadmap.md)

### Can the middleware be configured to be memory-static at runtime?

Yes, see [the documentation](https://fast-dds.docs.eprosima.com/en/latest/fastdds/use_cases/realtime/allocations.html#realtime-allocations)

### What support is there for microcontrollers?

[eProsima Micro XRCE-DDS](https://www.eprosima.com/index.php/products-all/eprosima-micro-xrce-dds):
an open source middleware product that implements the OMG (Object Management Group) wire protocol for eXtremely Resource Constrained Environments (DDS-XRCE).
eProsima Micro XRCE-DDS is the default middleware of micro-ROS.

### Are there tools available for integrating/bridging with other protocols (MQTT, etc)? What are they, and how do they work?

[eProsima Integration Service](https://www.eprosima.com/index.php/products-all/eprosima-integration-service):
an open source product that enables intercommunication of an arbitrary number of protocols that speak different languages.

### How much adherence is there to the RTPS standard?

RTPS version 2.2 is fully supported.

### How much support for the DDS-Security specification is provided in the DDS implementation?

DDS-security specification version 1.1 is fully supported, except only `file` schema is supported in the URI for certificates and private keys. `PKCS11` schema support is under development.

### Does the package have explicit tooling and support for protocol dissection?

The [eProsima Fast DDS Monitor](https://www.eprosima.com/index.php/products-all/eprosima-fast-dds-monitor) 
is an open source graphical desktop application aimed to monitor DDS environments deployed using eProsima Fast DDS.
The user can track the status of publication/subscription communications between DDS entities in real-time, and measure communication parameters such as latency, throughput, packet loss and others.


## Quality

### What is the currently declared REP-2004 quality of the package implementing the RTPS/DDS protocols and the RMW?

- eProsima Fast DDS has QL1. The Quality declaration document can be found [here](https://github.com/eProsima/Fast-DDS/blob/master/QUALITY.md)
- rmw_fastrtps has QL2.

### How else does the package measure quality? Please list specific procedures or tools that are used.

All changes to eProsima Fast DDS occur through pull requests that are required to pass all CI tests on Jenkins.
In case of failure, only maintainers can merge the pull request, and only when there is enough evidence that the failure is unrelated to the change.
Additionally, all pull requests must have a positive review from one other contributor that did not author the pull request.

Each feature in eProsima Fast DDS has corresponding tests which simulate typical usage, and they are located in the [test](https://github.com/eProsima/Fast-DDS/tree/master/test) directory.
New features are required to have tests before being added.

Test coverage is monitored as part of the pull request CI requirements.
All contributions to Fast DDS must not decrease current line coverage.

eProsima Fast DDS has a code style that is enforced using uncrustify.
Among the CI tests there are tests that ensures that every pull request is compliant with the code style.
The latest pull request results can be seen [here](http://jenkins.eprosima.com:8080/job/fastdds_github_uncrustify/lastBuild).

Performance tests are automatically run after merging to the master branch of the project.
If there has been any performance regression a notification is issued to maintainers that will study and decide how to proceed.

Valgrind memory checks are executed nightly on Jenkins. If any issue is found, a notification is issued to maintainers unless properly justified and accepted by maintainers.

Prior to any new release, an additional step of release testing is performed to check that communication works within the same machine, between machines and between platforms.
These tests are performed using several configurations to ensure every functionality works correctly. Interoperability with other vendors is also checked using the latest official ShapesDemo.


### Where is the development process documented?

The process can be found in [CONTRIBUTING](https://github.com/eProsima/policies/blob/main/CONTRIBUTING.md).

### What kinds of tests are run? Smoke tests, unit tests, integration tests, load tests, coverage? What platforms are each of the tests run on?

Unit tests, integration tests and coverage tests are run before accepting any pull request and on nightly jobs.
Performance tests are run after merging to the master branch.

All tests are run on linux, windows, MacOS and linux aarch64 platforms.

### Has the DDS Security implementation been audited by a third-party?

Each of the Fast DDS security plugins were implemented with a third party entities that reviewed the code.




## Benchmarking

### Testing framework

Tests have been executed on Raspberry-pi 4b+, linux laptops and windows laptops.

Tests on Ubuntu 20.04 and Windows10 laptops are still being processed and will be available by the final deadline date.

#### RPi specifications

| Board model | Architecture | CPUs | CPU max MHz | Kernel version | OS |
|-|-|-|-|-|-|
| Raspberry Pi 4 Model B Plus Rev 1.1 | aarch64 | 4 | 1500 | 5.4.0-1042-raspi | Ubuntu 20.04.1 LTS |

#### Linux laptop specifications

| Board model | Architecture | CPUs | CPU max MHz | Kernel version | OS |
|-|-|-|-|-|-|
| Intel(R) Core(TM) i7-7700HQ CPU @ 2.80GHz | x86_64 | 4 | 3800 | 5.4.0-73-generic | Ubuntu 20.04.2 LTS |

#### Windows laptop specifications

| Board model | Architecture | CPUs | CPU max MHz | OS |
|-|-|-|-|-|
| Intel(R) Core(TM) i7-4700MQ CPU @ 2.40GHz | x86_64 | 4 | 2400 | 5.4.0-73-generic | Windows 10 Enterprise  |

### Benchmark tools

For the test to be reproducible, they were performed using a fork of the [Apex performance test tool](https://gitlab.com/ApexAI/performance_test.git).
This fork has the necessary changes needed for the tools to build on Windows systems.
You can get the fork [here](https://gitlab.com/MiguelCompany/performance_test), checkout commit c230727.

We have prepared a set of scripts to help automatize the launch of the tests with different configurations. These scripts include:
 * Downloading the specified [ros2.repos file](https://github.com/osrf/TSC-RMW-Reports/blob/main/humble/ros2.repos).
 * Downloading the aforementioned fork of the Apex performance tool.
 * Compiling ROS2 and the performance tool
 * Launching the tests with the configuration specified on a json file

All tests were executed for 5 minutes.
During this time, Apex performance tool outputs measurements every second.
This means that every test has around 300 measured samples that are statistically analysed.

### Testing setup

#### Network setup

In order to avoid external noise in the results, the experiments have been conducted in an isolated environment:

 * Devices are connected to a LAN without internet access (they are not connected to any other network).
 * To easy the process of conducting the experiments, a "gateway" machine is connected to the testing LAN, as well as a normal LAN, so that the testing machines can be accessed from outside the testing LAN with 2 ssh connections (to the gateway machine, and from there to the testing device). This is very useful when conducting inter-host tests, since the gateway can act as an orchestrator.
 * The WiFi interfaces were down for the experiments that do not use it (i.e., except the inter-host with WiFi experiments).


#### Tested configurations

Several configurations have been tested. Note that the default configuration for eProsima Fast DDS is asynchronous publishing with no data-sharing.

**Reliability**

Both best-effort and reliable configurations are tested.

**History kind and durability**

Only volatile keep-last configuration was tested. With the kind of tests being performed, where there are no late-joiner subscribers, there is no significant difference on the results when using transient or keep-all. In order to reduce the amount of possible lost packages on reliable configurations, a depth of 100 was used.

**Loans**

Results with both loaned messages and without loaned messages were tested.

**Data sizes**

In order to characterize the performance with the size of the data samples, the following data types and sizes have been used:
 * 256 B
 * 4 KB
 * 2 MB

We consider these values as examples of small, medium and large data sizes.

**Delivery rates**

In order to characterize the performance with the delivery rate, the following rates have been used:
 * 30 Hz
 * 300 Hz
 * 1000 Hz
 
We consider these values as examples of low, medium and high publication frequencies.

**Number of subscribers**

In order to characterize the performance with the number of subscribers, tests with different number of subscribers have been used:
 * 1 subscriber
 * 3 subscribers
 * 10 subscribers

**Publishing mode**

Synchronous an asynchronous publication modes have been compared.
 
**Delivery mode**

Different available delivery modes have been compared:
 * Intra-process delivery.
 * Inter-process delivery using data-sharing.
 * Inter-process delivery without data-sharing.
 * Inter-host delivery over Ethernet.
 * Inter-host delivery over WiFi.

## Performance test result analysis

The amount of combinations resulting of the tested configurations is huge.
To keep conclusions comprehensible, only significant results are presented here.
You can find the complete result report [here](https://github.com/eProsima/benchmarking/tree/master/performance_results/tsc_rmw_report_2021).

