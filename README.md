# TCP Congestion Control Algorithms in Python

This repository implements three key **TCP congestion control algorithms** in Python:

1. **TCP AIMD (Additive Increase, Multiplicative Decrease)**
2. **TCP Cubic**
3. **TCP Vegas**

These algorithms are fundamental to how TCP manages congestion in networks, impacting performance, throughput, and fairness.

## Algorithms

### 1. **TCP AIMD (Additive Increase, Multiplicative Decrease)**
AIMD is the classical congestion control algorithm used in TCP Reno. It increases the congestion window (`cwnd`) linearly (additive increase) during normal conditions and reduces it by half (multiplicative decrease) upon detecting packet loss.

### 2. **TCP Cubic**
TCP Cubic is designed to improve performance in high-bandwidth, high-latency networks. It uses a cubic function for increasing the congestion window, which allows for more aggressive growth and faster recovery after packet loss compared to AIMD.

### 3. **TCP Vegas**
TCP Vegas adjusts the congestion window based on **RTT (Round-Trip Time)**, instead of relying solely on packet loss. It tries to detect congestion before it happens by comparing expected and actual RTT values, making it more proactive and efficient under low congestion conditions.
