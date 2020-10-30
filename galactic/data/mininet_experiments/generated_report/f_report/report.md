# Comparing RMW Implementations Across Bandwidths and Packet Losses

Comparison is between the rmw implementations rmw_fastrtps_cpp sync, rmw_fastrtps_cpp async, and rmw_cyclonedds_cpp sync, and is
varied across bandwidth limits (1000, 300, and 54) and message type/rate
combinations (Array1k@30 and PointCloud512k@30).

Data was collected using the `run_experiments.py` script, and uses [mininet](http://mininet.org/)
to simulate adverse network conditions, potentially varying the bandwidth limit, packet loss,
and/or packet delay for each process.

Each experimental run consists of two processes, one containing a publisher and the other
containing a subscription.
Experiments are run for 15 seconds, and various statistics are collected, but for this
comparison only "number of messages sent/received per second" are considered.

## Comparisons with Bandwidth Limited to 54Mbps

### Comparison Publishing Array1k@30

The specific details for this experiment are as follows:

- 1 Publisher
- 1 Subscription
- Separate Processes
- Single Machine
- Number of Runs Averaged: 10
- RMW Implementation: rmw_fastrtps_cpp sync/rmw_fastrtps_cpp async/rmw_cyclonedds_cpp sync
- Message Type: Array1k
- Message Rate: 30
- Reliability QoS: reliable
- Durability QoS: volatile
- History Kind QoS: keep_last
- History Depth QoS: 10
- Bandwidth Limit (Mbps): 54
- Packet Loss Percentage: 0/10/20/30/40
- Packet Delay (ms): 0

#### rmw_cyclonedds_cpp sync

<table>
  <tr>
    <td>Packet Loss: 0%</td>
    <td>Packet Loss: 10%</td>
    <td>Packet Loss: 20%</td>
    <td>Packet Loss: 30%</td>
    <td>Packet Loss: 40%</td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_0loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_10loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_20loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_30loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_40loss_0delay/average_sent_received.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_0loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_10loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_20loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_30loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_40loss_0delay/average_latency.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_0loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_10loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_20loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_30loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_40loss_0delay/resource.svg"></td>
  </tr>
</table>

#### rmw_fastrtps_cpp async

<table>
  <tr>
    <td>Packet Loss: 0%</td>
    <td>Packet Loss: 10%</td>
    <td>Packet Loss: 20%</td>
    <td>Packet Loss: 30%</td>
    <td>Packet Loss: 40%</td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_54bw_0loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_54bw_10loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_54bw_20loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_54bw_30loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_54bw_40loss_0delay/average_sent_received.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_54bw_0loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_54bw_10loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_54bw_20loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_54bw_30loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_54bw_40loss_0delay/average_latency.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_54bw_0loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_54bw_10loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_54bw_20loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_54bw_30loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_54bw_40loss_0delay/resource.svg"></td>
  </tr>
</table>

#### rmw_fastrtps_cpp sync

<table>
  <tr>
    <td>Packet Loss: 0%</td>
    <td>Packet Loss: 10%</td>
    <td>Packet Loss: 20%</td>
    <td>Packet Loss: 30%</td>
    <td>Packet Loss: 40%</td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_0loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_10loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_20loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_30loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_40loss_0delay/average_sent_received.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_0loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_10loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_20loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_30loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_40loss_0delay/average_latency.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_0loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_10loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_20loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_30loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_54bw_40loss_0delay/resource.svg"></td>
  </tr>
</table>

### Comparison Publishing PointCloud512k@30

The specific details for this experiment are as follows:

- 1 Publisher
- 1 Subscription
- Separate Processes
- Single Machine
- Number of Runs Averaged: 10
- RMW Implementation: rmw_fastrtps_cpp sync/rmw_fastrtps_cpp async/rmw_cyclonedds_cpp sync
- Message Type: PointCloud512k
- Message Rate: 30
- Reliability QoS: reliable
- Durability QoS: volatile
- History Kind QoS: keep_last
- History Depth QoS: 10
- Bandwidth Limit (Mbps): 54
- Packet Loss Percentage: 0/10/20/30/40
- Packet Delay (ms): 0

#### rmw_cyclonedds_cpp sync

<table>
  <tr>
    <td>Packet Loss: 0%</td>
    <td>Packet Loss: 10%</td>
    <td>Packet Loss: 20%</td>
    <td>Packet Loss: 30%</td>
    <td>Packet Loss: 40%</td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_0loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_10loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_20loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_30loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_40loss_0delay/average_sent_received.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_0loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_10loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_20loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_30loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_40loss_0delay/average_latency.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_0loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_10loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_20loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_30loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_40loss_0delay/resource.svg"></td>
  </tr>
</table>

#### rmw_fastrtps_cpp async

<table>
  <tr>
    <td>Packet Loss: 0%</td>
    <td>Packet Loss: 10%</td>
    <td>Packet Loss: 20%</td>
    <td>Packet Loss: 30%</td>
    <td>Packet Loss: 40%</td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_0loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_10loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_20loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_30loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_40loss_0delay/average_sent_received.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_0loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_10loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_20loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_30loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_40loss_0delay/average_latency.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_0loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_10loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_20loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_30loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_40loss_0delay/resource.svg"></td>
  </tr>
</table>

#### rmw_fastrtps_cpp sync

<table>
  <tr>
    <td>Packet Loss: 0%</td>
    <td>Packet Loss: 10%</td>
    <td>Packet Loss: 20%</td>
    <td>Packet Loss: 30%</td>
    <td>Packet Loss: 40%</td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_0loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_10loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_20loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_30loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_40loss_0delay/average_sent_received.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_0loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_10loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_20loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_30loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_40loss_0delay/average_latency.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_0loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_10loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_20loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_30loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_54bw_40loss_0delay/resource.svg"></td>
  </tr>
</table>

## Comparisons with Bandwidth Limited to 300Mbps

### Comparison Publishing Array1k@30

The specific details for this experiment are as follows:

- 1 Publisher
- 1 Subscription
- Separate Processes
- Single Machine
- Number of Runs Averaged: 10
- RMW Implementation: rmw_fastrtps_cpp sync/rmw_fastrtps_cpp async/rmw_cyclonedds_cpp sync
- Message Type: Array1k
- Message Rate: 30
- Reliability QoS: reliable
- Durability QoS: volatile
- History Kind QoS: keep_last
- History Depth QoS: 10
- Bandwidth Limit (Mbps): 300
- Packet Loss Percentage: 0/10/20/30/40
- Packet Delay (ms): 0

#### rmw_cyclonedds_cpp sync

<table>
  <tr>
    <td>Packet Loss: 0%</td>
    <td>Packet Loss: 10%</td>
    <td>Packet Loss: 20%</td>
    <td>Packet Loss: 30%</td>
    <td>Packet Loss: 40%</td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_0loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_10loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_20loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_30loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_40loss_0delay/average_sent_received.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_0loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_10loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_20loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_30loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_40loss_0delay/average_latency.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_0loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_10loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_20loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_30loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_40loss_0delay/resource.svg"></td>
  </tr>
</table>

#### rmw_fastrtps_cpp async

<table>
  <tr>
    <td>Packet Loss: 0%</td>
    <td>Packet Loss: 10%</td>
    <td>Packet Loss: 20%</td>
    <td>Packet Loss: 30%</td>
    <td>Packet Loss: 40%</td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_300bw_0loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_300bw_10loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_300bw_20loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_300bw_30loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_300bw_40loss_0delay/average_sent_received.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_300bw_0loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_300bw_10loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_300bw_20loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_300bw_30loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_300bw_40loss_0delay/average_latency.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_300bw_0loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_300bw_10loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_300bw_20loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_300bw_30loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_300bw_40loss_0delay/resource.svg"></td>
  </tr>
</table>

#### rmw_fastrtps_cpp sync

<table>
  <tr>
    <td>Packet Loss: 0%</td>
    <td>Packet Loss: 10%</td>
    <td>Packet Loss: 20%</td>
    <td>Packet Loss: 30%</td>
    <td>Packet Loss: 40%</td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_0loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_10loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_20loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_30loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_40loss_0delay/average_sent_received.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_0loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_10loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_20loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_30loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_40loss_0delay/average_latency.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_0loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_10loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_20loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_30loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_300bw_40loss_0delay/resource.svg"></td>
  </tr>
</table>

### Comparison Publishing PointCloud512k@30

The specific details for this experiment are as follows:

- 1 Publisher
- 1 Subscription
- Separate Processes
- Single Machine
- Number of Runs Averaged: 10
- RMW Implementation: rmw_fastrtps_cpp sync/rmw_fastrtps_cpp async/rmw_cyclonedds_cpp sync
- Message Type: PointCloud512k
- Message Rate: 30
- Reliability QoS: reliable
- Durability QoS: volatile
- History Kind QoS: keep_last
- History Depth QoS: 10
- Bandwidth Limit (Mbps): 300
- Packet Loss Percentage: 0/10/20/30/40
- Packet Delay (ms): 0

#### rmw_cyclonedds_cpp sync

<table>
  <tr>
    <td>Packet Loss: 0%</td>
    <td>Packet Loss: 10%</td>
    <td>Packet Loss: 20%</td>
    <td>Packet Loss: 30%</td>
    <td>Packet Loss: 40%</td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_0loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_10loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_20loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_30loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_40loss_0delay/average_sent_received.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_0loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_10loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_20loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_30loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_40loss_0delay/average_latency.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_0loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_10loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_20loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_30loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_40loss_0delay/resource.svg"></td>
  </tr>
</table>

#### rmw_fastrtps_cpp async

<table>
  <tr>
    <td>Packet Loss: 0%</td>
    <td>Packet Loss: 10%</td>
    <td>Packet Loss: 20%</td>
    <td>Packet Loss: 30%</td>
    <td>Packet Loss: 40%</td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_0loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_10loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_20loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_30loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_40loss_0delay/average_sent_received.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_0loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_10loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_20loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_30loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_40loss_0delay/average_latency.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_0loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_10loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_20loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_30loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_40loss_0delay/resource.svg"></td>
  </tr>
</table>

#### rmw_fastrtps_cpp sync

<table>
  <tr>
    <td>Packet Loss: 0%</td>
    <td>Packet Loss: 10%</td>
    <td>Packet Loss: 20%</td>
    <td>Packet Loss: 30%</td>
    <td>Packet Loss: 40%</td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_0loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_10loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_20loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_30loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_40loss_0delay/average_sent_received.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_0loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_10loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_20loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_30loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_40loss_0delay/average_latency.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_0loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_10loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_20loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_30loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_300bw_40loss_0delay/resource.svg"></td>
  </tr>
</table>

## Comparisons with Bandwidth Limited to 1000Mbps

### Comparison Publishing Array1k@30

The specific details for this experiment are as follows:

- 1 Publisher
- 1 Subscription
- Separate Processes
- Single Machine
- Number of Runs Averaged: 10
- RMW Implementation: rmw_fastrtps_cpp sync/rmw_fastrtps_cpp async/rmw_cyclonedds_cpp sync
- Message Type: Array1k
- Message Rate: 30
- Reliability QoS: reliable
- Durability QoS: volatile
- History Kind QoS: keep_last
- History Depth QoS: 10
- Bandwidth Limit (Mbps): 1000
- Packet Loss Percentage: 0/10/20/30/40
- Packet Delay (ms): 0

#### rmw_cyclonedds_cpp sync

<table>
  <tr>
    <td>Packet Loss: 0%</td>
    <td>Packet Loss: 10%</td>
    <td>Packet Loss: 20%</td>
    <td>Packet Loss: 30%</td>
    <td>Packet Loss: 40%</td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_0loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_10loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_20loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_30loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_40loss_0delay/average_sent_received.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_0loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_10loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_20loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_30loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_40loss_0delay/average_latency.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_0loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_10loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_20loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_30loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_40loss_0delay/resource.svg"></td>
  </tr>
</table>

#### rmw_fastrtps_cpp async

<table>
  <tr>
    <td>Packet Loss: 0%</td>
    <td>Packet Loss: 10%</td>
    <td>Packet Loss: 20%</td>
    <td>Packet Loss: 30%</td>
    <td>Packet Loss: 40%</td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_1000bw_0loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_1000bw_10loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_1000bw_20loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_1000bw_30loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_1000bw_40loss_0delay/average_sent_received.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_1000bw_0loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_1000bw_10loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_1000bw_20loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_1000bw_30loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_1000bw_40loss_0delay/average_latency.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_1000bw_0loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_1000bw_10loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_1000bw_20loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_1000bw_30loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_Array1k@30_reliable_volatile_keep_last@10_1000bw_40loss_0delay/resource.svg"></td>
  </tr>
</table>

#### rmw_fastrtps_cpp sync

<table>
  <tr>
    <td>Packet Loss: 0%</td>
    <td>Packet Loss: 10%</td>
    <td>Packet Loss: 20%</td>
    <td>Packet Loss: 30%</td>
    <td>Packet Loss: 40%</td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_0loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_10loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_20loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_30loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_40loss_0delay/average_sent_received.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_0loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_10loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_20loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_30loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_40loss_0delay/average_latency.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_0loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_10loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_20loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_30loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_Array1k@30_reliable_volatile_keep_last@10_1000bw_40loss_0delay/resource.svg"></td>
  </tr>
</table>

### Comparison Publishing PointCloud512k@30

The specific details for this experiment are as follows:

- 1 Publisher
- 1 Subscription
- Separate Processes
- Single Machine
- Number of Runs Averaged: 10
- RMW Implementation: rmw_fastrtps_cpp sync/rmw_fastrtps_cpp async/rmw_cyclonedds_cpp sync
- Message Type: PointCloud512k
- Message Rate: 30
- Reliability QoS: reliable
- Durability QoS: volatile
- History Kind QoS: keep_last
- History Depth QoS: 10
- Bandwidth Limit (Mbps): 1000
- Packet Loss Percentage: 0/10/20/30/40
- Packet Delay (ms): 0

#### rmw_cyclonedds_cpp sync

<table>
  <tr>
    <td>Packet Loss: 0%</td>
    <td>Packet Loss: 10%</td>
    <td>Packet Loss: 20%</td>
    <td>Packet Loss: 30%</td>
    <td>Packet Loss: 40%</td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_0loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_10loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_20loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_30loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_40loss_0delay/average_sent_received.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_0loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_10loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_20loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_30loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_40loss_0delay/average_latency.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_0loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_10loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_20loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_30loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_cyclonedds_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_40loss_0delay/resource.svg"></td>
  </tr>
</table>

#### rmw_fastrtps_cpp async

<table>
  <tr>
    <td>Packet Loss: 0%</td>
    <td>Packet Loss: 10%</td>
    <td>Packet Loss: 20%</td>
    <td>Packet Loss: 30%</td>
    <td>Packet Loss: 40%</td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_0loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_10loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_20loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_30loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_40loss_0delay/average_sent_received.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_0loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_10loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_20loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_30loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_40loss_0delay/average_latency.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_0loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_10loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_20loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_30loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_async_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_40loss_0delay/resource.svg"></td>
  </tr>
</table>

#### rmw_fastrtps_cpp sync

<table>
  <tr>
    <td>Packet Loss: 0%</td>
    <td>Packet Loss: 10%</td>
    <td>Packet Loss: 20%</td>
    <td>Packet Loss: 30%</td>
    <td>Packet Loss: 40%</td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_0loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_10loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_20loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_30loss_0delay/average_sent_received.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_40loss_0delay/average_sent_received.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_0loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_10loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_20loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_30loss_0delay/average_latency.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_40loss_0delay/average_latency.svg"></td>
  </tr>
  <tr>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_0loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_10loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_20loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_30loss_0delay/resource.svg"></td>
    <td valign="top"><img src="rmw_fastrtps_cpp_sync_PointCloud512k@30_reliable_volatile_keep_last@10_1000bw_40loss_0delay/resource.svg"></td>
  </tr>
</table>

