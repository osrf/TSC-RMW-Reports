#!/bin/bash
set -e
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd $SCRIPT_DIR

perf_tool collect --database roundtrip.json --clean "Ubuntu inter-host" Interhost ./ubuntu-cyclonedds-interhost-main/*.csv
perf_tool collect --database roundtrip.json "Ubuntu inter-host" Interhost ./ubuntu-fastrtps-interhost-main/*.csv

perf_tool plot cpu_usage -f "Ubuntu inter-host" --database roundtrip.json
perf_tool plot ram_usage -f "Ubuntu inter-host" --database roundtrip.json
perf_tool plot jitter -f "Ubuntu inter-host" --database roundtrip.json
perf_tool plot roundtrip -f "Ubuntu inter-host" --database roundtrip.json
perf_tool plot throughput -f "Ubuntu inter-host" --database roundtrip.json

perf_tool histcatplot cpu_usage -c topic Array2m -c host "Ubuntu inter-host" -c subs 1 -c mode Interhost -c zero_copy false -c transient false \
    --filename plots/interhost_array2m_cpu_usage.png --roundtrip --database roundtrip.json
perf_tool histcatplot ram_usage -c topic Array2m -c host "Ubuntu inter-host" -c subs 1 -c mode Interhost -c zero_copy false -c transient false \
    --filename plots/interhost_array2m_ram_usage.png --roundtrip --database roundtrip.json
perf_tool histcatplot latency_mean -c topic Array2m -c host "Ubuntu inter-host" -c subs 1 -c mode Interhost -c zero_copy false -c transient false \
    --filename plots/interhost_array2m_roundtrip.png --roundtrip --database roundtrip.json
perf_tool histcatplot jitter -c topic Array2m -c host "Ubuntu inter-host" -c subs 1 -c mode Interhost -c zero_copy false -c transient false \
    --filename plots/interhost_array2m_jitter.png --roundtrip --database roundtrip.json
perf_tool histcatplot throughput -c topic Array2m -c host "Ubuntu inter-host" -c subs 1 -c mode Interhost -c zero_copy false -c transient false \
    --filename plots/interhost_array2m_throughput.png --roundtrip --database roundtrip.json

perf_tool histcatplot cpu_usage -c topic Array16k -c host "Ubuntu inter-host" -c subs 1 -c mode Interhost -c zero_copy false -c transient false \
    --filename plots/interhost_array16k_cpu_usage.png --roundtrip --database roundtrip.json
perf_tool histcatplot ram_usage -c topic Array16k -c host "Ubuntu inter-host" -c subs 1 -c mode Interhost -c zero_copy false -c transient false \
    --filename plots/interhost_array16k_ram_usage.png --roundtrip --database roundtrip.json
perf_tool histcatplot latency_mean -c topic Array16k -c host "Ubuntu inter-host" -c subs 1 -c mode Interhost -c zero_copy false -c transient false \
    --filename plots/interhost_array16k_roundtrip.png --roundtrip --database roundtrip.json
perf_tool histcatplot jitter -c topic Array16k -c host "Ubuntu inter-host" -c subs 1 -c mode Interhost -c zero_copy false -c transient false \
    --filename plots/interhost_array16k_jitter.png --roundtrip --database roundtrip.json
perf_tool histcatplot throughput -c topic Array16k -c host "Ubuntu inter-host" -c subs 1 -c mode Interhost -c zero_copy false -c transient false \
    --filename plots/interhost_array16k_throughput.png --roundtrip --database roundtrip.json

perf_tool histcatplot cpu_usage -c topic PointCloud1m -c host "Ubuntu inter-host" -c subs 1 -c mode Interhost -c zero_copy false -c transient false \
    --filename plots/interhost_pointcloud1m_cpu_usage.png --roundtrip --database roundtrip.json
perf_tool histcatplot ram_usage -c topic PointCloud1m -c host "Ubuntu inter-host" -c subs 1 -c mode Interhost -c zero_copy false -c transient false \
    --filename plots/interhost_pointcloud1m_ram_usage.png --roundtrip --database roundtrip.json
perf_tool histcatplot latency_mean -c topic PointCloud1m -c host "Ubuntu inter-host" -c subs 1 -c mode Interhost -c zero_copy false -c transient false \
    --filename plots/interhost_pointcloud1m_roundtrip.png --roundtrip --database roundtrip.json
perf_tool histcatplot jitter -c topic PointCloud1m -c host "Ubuntu inter-host" -c subs 1 -c mode Interhost -c zero_copy false -c transient false \
    --filename plots/interhost_pointcloud1m_jitter.png --roundtrip --database roundtrip.json
perf_tool histcatplot throughput -c topic PointCloud1m -c host "Ubuntu inter-host" -c subs 1 -c mode Interhost -c zero_copy false -c transient false \
    --filename plots/interhost_pointcloud1m_throughput.png --roundtrip --database roundtrip.json

perf_tool histcatplot cpu_usage -c topic PointCloud4m -c host "Ubuntu inter-host" -c subs 1 -c mode Interhost -c zero_copy false -c transient false \
    --filename plots/interhost_pointcloud4m_cpu_usage.png --roundtrip --database roundtrip.json
perf_tool histcatplot ram_usage -c topic PointCloud4m -c host "Ubuntu inter-host" -c subs 1 -c mode Interhost -c zero_copy false -c transient false \
    --filename plots/interhost_pointcloud4m_ram_usage.png --roundtrip --database roundtrip.json
perf_tool histcatplot latency_mean -c topic PointCloud4m -c host "Ubuntu inter-host" -c subs 1 -c mode Interhost -c zero_copy false -c transient false \
    --filename plots/interhost_pointcloud4m_roundtrip.png --roundtrip --database roundtrip.json
perf_tool histcatplot jitter -c topic PointCloud4m -c host "Ubuntu inter-host" -c subs 1 -c mode Interhost -c zero_copy false -c transient false \
    --filename plots/interhost_pointcloud4m_jitter.png --roundtrip --database roundtrip.json
perf_tool histcatplot throughput -c topic PointCloud4m -c host "Ubuntu inter-host" -c subs 1 -c mode Interhost -c zero_copy false -c transient false \
    --filename plots/interhost_pointcloud4m_throughput.png --roundtrip --database roundtrip.json

perf_tool histcatplot cpu_usage -c topic Struct32k -c host "Ubuntu inter-host" -c subs 1 -c mode Interhost -c zero_copy false -c transient false \
    --filename plots/interhost_struct32k_cpu_usage.png --roundtrip --database roundtrip.json
perf_tool histcatplot ram_usage -c topic Struct32k -c host "Ubuntu inter-host" -c subs 1 -c mode Interhost -c zero_copy false -c transient false \
    --filename plots/interhost_struct32k_ram_usage.png --roundtrip --database roundtrip.json
perf_tool histcatplot latency_mean -c topic Struct32k -c host "Ubuntu inter-host" -c subs 1 -c mode Interhost -c zero_copy false -c transient false \
    --filename plots/interhost_struct32k_roundtrip.png --roundtrip --database roundtrip.json
perf_tool histcatplot jitter -c topic Struct32k -c host "Ubuntu inter-host" -c subs 1 -c mode Interhost -c zero_copy false -c transient false \
    --filename plots/interhost_struct32k_jitter.png --roundtrip --database roundtrip.json
perf_tool histcatplot throughput -c topic Struct32k -c host "Ubuntu inter-host" -c subs 1 -c mode Interhost -c zero_copy false -c transient false \
    --filename plots/interhost_struct32k_throughput.png --roundtrip --database roundtrip.json

perf_tool collect --clean Ubuntu Images ./ubuntu-images/*.csv --database images.json
perf_tool histcatplot cpu_usage -c mode Images -c host Ubuntu --database images.json -c reliable true -c transient false -c zero_copy true -c rate 30 \
    --onlycyclone --filename plots/imagetopics_zerocopy_cpu_usage.png
perf_tool histcatplot ram_usage -c mode Images -c host Ubuntu --database images.json -c reliable true -c transient false -c zero_copy true -c rate 30 \
    --onlycyclone --filename plots/imagetopics_zerocopy_ram_usage.png
perf_tool histcatplot latency_mean -c mode Images -c host Ubuntu --database images.json -c reliable true -c transient false -c zero_copy true -c rate 30 \
    --onlycyclone --filename plots/imagetopics_zerocopy_latency_mean.png
perf_tool histcatplot jitter -c mode Images -c host Ubuntu --database images.json -c reliable true -c transient false -c zero_copy true -c rate 30 \
    --onlycyclone --filename plots/imagetopics_zerocopy_jitter.png
perf_tool histcatplot throughput -c mode Images -c host Ubuntu --database images.json -c reliable true -c transient false -c zero_copy true -c rate 30 \
    --onlycyclone --filename plots/imagetopics_zerocopy_throughput.png

perf_tool histcatplot cpu_usage -c topic PointCloud4m -c rate 20 -c subs 1 -c mode MultiProcess -c zero_copy false -c reliable true -c transient false \
    --filename plots/imagetopic_cpu_usage.png
perf_tool histcatplot ram_usage -c topic PointCloud4m -c rate 20 -c subs 1 -c mode MultiProcess -c zero_copy false -c reliable true -c transient false \
    --filename plots/imagetopic_ram_usage.png
perf_tool histcatplot latency_mean -c topic PointCloud4m -c rate 20 -c subs 1 -c mode MultiProcess -c zero_copy false -c reliable true -c transient false \
    --filename plots/imagetopic_latency_mean.png
perf_tool histcatplot jitter -c topic PointCloud4m -c rate 20 -c subs 1 -c mode MultiProcess -c zero_copy false -c reliable true -c transient false --log \
    --filename plots/imagetopic_jitter.png
perf_tool histcatplot throughput -c topic PointCloud4m -c rate 20 -c subs 1 -c mode MultiProcess -c zero_copy false -c reliable true -c transient false \
    --filename plots/imagetopic_throughput.png

perf_tool collect --clean Ubuntu SingleProcess ./ubuntu-singleprocess/*.csv
perf_tool collect Ubuntu MultiProcess ./ubuntu-multiprocess/*.csv
perf_tool collect Windows SingleProcess ./windows-singleprocess/*.csv
perf_tool collect Windows MultiProcess ./windows-multiprocess/*.csv
perf_tool collect "macOS M1" SingleProcess ./macos-m1-singleprocess/*.csv
perf_tool collect "macOS M1" MultiProcess ./macos-m1-multiprocess/*.csv
perf_tool collect RPi4B SingleProcess ./rpi4b-singleprocess/*.csv
perf_tool collect RPi4B MultiProcess ./rpi4b-multiprocess/*.csv

perf_tool plot cpu_usage -f "macOS M1" --rate-limited
perf_tool plot cpu_usage -f Windows --rate-limited
perf_tool plot cpu_usage -f RPi4B --rate-limited
perf_tool plot cpu_usage -f Ubuntu --rate-limited
perf_tool plot cpu_usage --rate-limited

perf_tool plot rel_cpu_usage -f "macOS M1" --rate-unlimited
perf_tool plot rel_cpu_usage -f Windows --rate-unlimited
perf_tool plot rel_cpu_usage -f RPi4B --rate-unlimited
perf_tool plot rel_cpu_usage -f Ubuntu --rate-unlimited
perf_tool plot rel_cpu_usage --rate-unlimited

perf_tool plot ram_usage -f "macOS M1"
perf_tool plot ram_usage -f Windows
perf_tool plot ram_usage -f RPi4B
perf_tool plot ram_usage -f Ubuntu
perf_tool plot ram_usage

perf_tool plot latency_mean -f "macOS M1"
perf_tool plot latency_mean -f Windows
perf_tool plot latency_mean -f RPi4B
perf_tool plot latency_mean -f Ubuntu
perf_tool plot latency_mean

perf_tool plot jitter -f "macOS M1"
perf_tool plot jitter -f Windows
perf_tool plot jitter -f RPi4B
perf_tool plot jitter -f Ubuntu
perf_tool plot jitter

perf_tool plot throughput -f "macOS M1" --rate-unlimited
perf_tool plot throughput -f Windows --rate-unlimited
perf_tool plot throughput -f RPi4B --rate-unlimited
perf_tool plot throughput -f Ubuntu --rate-unlimited
perf_tool plot throughput --rate-unlimited

perf_tool scaleplot ./ubuntu-nodes-scaling cpu_usage 1 50 2
perf_tool scaleplot ./ubuntu-nodes-scaling ram_usage 1 50 2
perf_tool scaleplot ./ubuntu-nodes-scaling latency_mean 1 50 2
perf_tool scaleplot ./ubuntu-nodes-scaling jitter 1 50 2
perf_tool scaleplot ./ubuntu-topics-scaling cpu_usage 1 50 2 --topics
perf_tool scaleplot ./ubuntu-topics-scaling ram_usage 1 50 2 --topics
perf_tool scaleplot ./ubuntu-topics-scaling latency_mean 1 50 2 --topics
perf_tool scaleplot ./ubuntu-topics-scaling jitter 1 50 2 --topics

perf_tool collect --clean --database zerocopy.json Ubuntu ZeroCopy ubuntu-multiprocess/*.csv
perf_tool collect --database zerocopy.json Ubuntu ZeroCopy ubuntu-zerocopy/*.csv

perf_tool plot cpu_usage -f Ubuntu --rate-limited --database zerocopy.json --zero-copy
perf_tool plot rel_cpu_usage -f Ubuntu --rate-limited --database zerocopy.json --zero-copy
perf_tool plot ram_usage -f Ubuntu --rate-limited --database zerocopy.json --zero-copy
perf_tool plot latency_mean -f Ubuntu --rate-limited --database zerocopy.json --zero-copy
perf_tool plot jitter -f Ubuntu --rate-limited --database zerocopy.json --zero-copy

perf_tool tabulate -f Ubuntu -o tables/ubuntu-limited.csv --rate-limited
perf_tool tabulate -f Ubuntu -o tables/ubuntu-unlimited.csv --rate-unlimited
perf_tool tabulate -f Windows -o tables/windows-limited.csv --rate-limited
perf_tool tabulate -f Windows -o tables/windows-unlimited.csv --rate-unlimited
perf_tool tabulate -f "macOS M1" -o tables/macosm1-limited.csv --rate-limited
perf_tool tabulate -f "macOS M1" -o tables/macosm1-unlimited.csv --rate-unlimited
perf_tool tabulate -f RPi4B -o tables/rpi4b-limited.csv --rate-limited
perf_tool tabulate -f RPi4B -o tables/rpi4b-unlimited.csv --rate-unlimited

