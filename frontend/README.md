# React + Vite + Flowbite

This is the frontend (Web UI) part of the project, built using React and Flowbite as UI Kit.
It provides a basic interface for the REST API.

## Features
- Visualizes the full list of running processes
  - allows the user to order by each column
  - allows the user to order by ascending or descending order
- Provides a search bar to filter the processes by name
- Provides a slider for selecting API query interval
- Visualizes a list of processes that can be classified as "anomalies", following the
  env variables that define the criteria for an anomaly. A process may appear in this list
  and then disappear, due to the fact that the assumption was made with the available set of
  data. Anomalies are seperated by their usage of CPU and Memory resources.

## Notes / Future improvements
- The endpoints are hardcoded for each table.
- The state of dark/light mode is not persistent and not regarding the system settings.
