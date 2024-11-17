# shiny-app
A web application built using Python Shiny deployed on AWS EC2 to showcase house price prediction on selected features.  The app provides interactive visualizations and real-time price predictions for houses in California.

## URL: http://3.15.206.34

## Server Information
 EC2 Instance ID: i-08e7966db1d4837ec
 IP Address: 3.15.206.34

## Structure
 shiny-app/
 ├── app.py                   # Main application file
 ├── shinyvenv/               # Virtual environment
 ├── requirements.txt         # Python dependencies
 ├── shinykey.pem             # Key
 ├── all_data.csv             # Cleaned data
 ├── house_price_model.joblib # Gradient Boosting Regressor
 └── README.md                # Documentation

## Price Prediction in Shiny App
  Interactive sliders for adjusting house features:
    Living Area (sq ft)
    Years Since Built
    Gas Station Count (within 2 miles)
    Golf Course Count (within 2 miles)
    Average Bar Rating (within 0.5 miles)
    Household Income (by zipcode)
    Distance to Trader Joe's
    Best School Rating (within 1 mile)
    Distance to Coast

## Visualizations in Shiny App
    Interactive California map showing house locations
    Color-coded pricing visualization
    Feature distribution histograms
    Feature importance chart

## Configuration File
run_as ubuntu;

server {
  listen 80;

  location / {
    # Point to your virtual environment
    python /srv/shiny-server/shiny-app/shinyvenv;
    
    # Host the directory of Shiny Apps
    site_dir /srv/shiny-server/shiny-app;
    
    # Log all Shiny output to files in this directory
    log_dir /var/log/shiny-server;
    
    # When a user visits the base URL rather than a particular application,
    # an index of the applications available in this directory will be shown.
    directory_index on;
  }
}
