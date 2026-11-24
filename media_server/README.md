
# Raspberry Pi Media Server

A lightweight Flask-based media server developed to
support educational video delivery and network performance
experiments.

## Features

- Video delivery at 480p, 720p, and 1080p
- Automated startup time measurement
- Buffering detection and duration tracking
- 60-second playback observation
- JSON-based communication between browser and server
- Automated CSV data logging

## Technologies

Python, Flask, JavaScript, HTML, Raspberry Pi, and Linux.

## Purpose

The server provides a platform for controlled streaming
experiments and future validation of the statistical models.

Bandwidth conditions are selected manually in the interface.
Actual bandwidth restrictions must be applied separately.

## Run Locally

Install Flask:

`pip install flask`

Start the server:

`python app.py`

Open `http://localhost:5000` in a browser.

Video files must be provided separately in the paths
specified in app.py.
