# network-bandwidth-video-streaming
Statistical analysis of network bandwidth and video streaming performance using regression modeling, Python, and a Raspberry Pi-based media server.

# Network Bandwidth and Video Streaming Performance

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=flat&logo=raspberrypi&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black)
![Statistics](https://img.shields.io/badge/Statistical%20Modeling-276749)
![LaTeX](https://img.shields.io/badge/LaTeX-008080?style=flat&logo=latex&logoColor=white)

## Project Overview

How does limited network bandwidth affect video streaming performance, and how accurately can we model that relationship?

I explored this question through my senior research in Computer Science and Applied Mathematics, combining statistical modeling, network performance analysis, and the development of a Raspberry Pi-based media server.

The motivation behind this project was to better understand the challenges of delivering educational video content in environments with limited network connectivity.

## Research Highlights

- Analyzed **186 video streaming observations** across three video resolutions.
- Evaluated **three regression models** to predict video startup time.
- Achieved approximately **36% lower in-sample RMSE** using the Log-Log model compared with the linear baseline.
- Developed a Raspberry Pi-based media server supporting 480p, 720p, and 1080p video delivery.
- Examined buffering behavior using descriptive statistics and probability.

## Research Methodology

The project consists of two components: statistical analysis and system development.

### Statistical Analysis

Using an existing synthetic video streaming dataset, I investigated the relationship between available network bandwidth, video resolution, startup time, and buffering behavior.

The analysis involved:

- Data preparation and exploratory data analysis
- Pearson correlation analysis
- Regression coefficient estimation
- Model fitting and comparison
- Residual analysis
- Buffering occurrence and frequency analysis

### System Development

I developed a lightweight media server using Python and Flask on a Raspberry Pi to support educational video delivery over a local network.

The system supports multiple video resolutions and provides a platform for future controlled network experiments.

Network testing was performed using iperf3 and Linux networking tools.

## Regression Models

Three regression models were developed and evaluated:

| Model | RMSE (s) | R² | Adjusted R² |
|---|---:|---:|---:|
| Multiple Linear | 1.9143 | 0.5258 | 0.5180 |
| Quadratic | 1.6073 | 0.6657 | 0.6583 |
| **Log-Log** | **1.2236** | **0.8063** | **0.8031** |

All reported metrics are in-sample. Log-Log model predictions were evaluated on the original startup-time scale for comparison.

## Model Visualizations

### Regression Model Comparison

| Multiple Linear Regression | Log-Log Regression |
|:---:|:---:|
| ![Linear Regression](figures/linear_regression.png) | ![Log-Log Regression](figures/log_log_regression.png) |

### Quadratic Regression

![Quadratic Regression](figures/quadratic_regression.png)

### Residual Analysis

![Residual Analysis](figures/residual_analysis.png)

The residual plots compare observed and predicted startup
times across bandwidth levels. The Log-Log model shows
fewer noticeable residual patterns and achieves the
lowest in-sample RMSE among the three models.


## Key Findings

The Log-Log model provided the best overall fit among the three models evaluated.

The results showed that startup time generally decreases as bandwidth increases, with greater reductions at lower bandwidth levels.

Residual analysis also supported the selection of the Log-Log model, as its residuals showed fewer noticeable patterns.

These findings highlight the importance of considering nonlinear relationships when modeling network and streaming performance.

## Technical Skills

| Area | Tools and Methods |
|---|---|
| Programming | Python, JavaScript |
| Data Science | Regression, Exploratory Data Analysis |
| Mathematics | Statistics, Probability, Least Squares |
| Backend Development | Flask |
| Networking | TCP/IP, iperf3, Linux |
| Hardware | Raspberry Pi |
| Research Documentation | LaTeX, Overleaf |

## Research Materials

- Research Paper
- Research Poster
- Statistical Analysis Scripts
- Regression Curves
- Residual Plots
- Media Server Source Code

## Future Work

The next step is to validate the statistical findings using experimentally collected data from the Raspberry Pi media server under controlled bandwidth conditions.

I am also interested in exploring adaptive video delivery strategies that improve streaming performance in bandwidth-constrained environments.

## Author

**Cornelius Mulyokela**

Computer Science and Applied Mathematics (Data Science)

Senior Research Project | 2026
