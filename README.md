# Design Dashboard

This repository contains the web application that analyses the urban layout design from qua-kit platform. 

### Functionality
The web application can read the urban layout in .geojson format and conduct the following analysis
- Degree of Mixed-use
- Population Density(residential)
- Energy Consumption(annual)
- Gross Plot Ratio

### Technology 
This application is built with Flask framework. The other library I used include：
- shapely.py: to perform geometrical calculation
- d3.js: for front-end graph visualization

### How to run application?
go to the folder and run with 
`python3 app.py`
