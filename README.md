# procmon.py - Process Monitoring Application

## Overview
 
This application is built using FastAPI. It consists of the FastAPI application
and a background task that polls the system for process information and keeps a
history of the processes and their stats. The application provides REST API for
fetching the collected data and for analyzing it to detect anomalies.

## Configuration

The application is configured using a .env file. It contains the limits for the
anomaly detection algorithm. The values are:
- `PROCESS_REFRESH_INTERVAL` - Interval in seconds for polling the processes.
- `ANOMALY_THRESHOLD` - Threshold for the rolling z-score to classify a usage as anomaly.
- `ROLLING_WINDOW_SIZE` - Size of the rolling window for the z-score calculation.
- `ROLLING_WINDOW_LIMIT` - Limit for the rolling window size. Calculation starts after
    this limit is reached. Used to prevent false positives when there is not enough data.

## Dockerfile
The Dockerfile is set up to run the application as a monolith. Currently, FastAPI is
serving the frontend. This might not be optimal and is not ready for production. It is
plainly for ease of demonstration. The container will provide a working application.

**NB:** The docker container spawns no processes, other than the CMD command. This is expected
behavior. The application is more interesting to run on a host machine, where it can
visualize hundreds of processes.


## Notes / Future improvements
- The anomaly detection algorithm variables are not optimal.
- The anomaly detection algorithm might be improved by using a more sophisticated algorithm.
- The anomaly routes can be improved with more filtering and ordering options.
- Add more testing, testing the routes proved difficult, due to the settings object.