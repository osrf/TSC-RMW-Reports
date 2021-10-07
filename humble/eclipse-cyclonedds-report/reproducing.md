# Reproducing the data included in this report


## Setup

All data included in this report were generated with the Apex.AI [performance_test tool](https://gitlab.com/ApexAI/performance_test). To run the testsuite make sure to have:

 1. A valid ROS 2 installation. We used ROS 2 Galactic Patch Release 1.
 2. Compiled `performance_test` with `--cmake-args -DCMAKE_BUILD_TYPE=Release`
 3. To use the automated runner/analysis tool you will need Python 3.6 or higher

To install the automated runner/analysis tool:

```bash
$ pip install ./perf_tool --user
```

Now you can run the tests with one of the configurations included under "configurations/".

```bash
$ perf_tool run configurations/conf-main.json
```

This will call `performance_test` with a host of different arguments one after the other and generate CSV logfiles that can be used in analysis. The shared main testsuite for every platform is defined in [`conf-main.json`](configurations/conf-main.json) and includes singleprocess, multiprocess and scaling tests. They should be run with no config files for the RMW. Then there is [`conf-zerocopy.json`](configurations/conf-zerocopy.json) which runs Cyclone DDS with iceoryx. For this you will need a minimal config containing just the switch to allow shared memory mode and make sure to start the icoryx roudi daemon. Lastly there is [`conf-images.json`](configurations/conf-images.json) which showcases a selection of large datatypes at 30Hz.

## Analysis

The `perf_tool` can collect data from CSV logs, tabulate them and turn them into plots. Look in the file [`recollect.sh`](rawdata/recollect.sh) for how all the plots that are included in this report were generated. The per-test PDFs were generated with the performance plotter included in performance_test.
