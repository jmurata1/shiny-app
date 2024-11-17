# California House Price Prediction App

A web application built using Python Shiny deployed on AWS EC2 to showcase house price prediction on selected features. The app provides interactive visualizations and real-time price predictions for houses in California.

## Server
- **URL:** http://3.15.206.34
- **EC2 Instance ID:** i-08e7966db1d4837ec
- **IP Address:** 3.15.206.34

## Project Structure
```
shiny-app/
├── app.py              # Main application file
├── shinyvenv/          # Virtual environment
├── requirements.txt    # Python dependencies
├── shinykey.pem       # AWS key file
├── all_data.csv       # Cleaned dataset
├── house_price_model.joblib  # Trained model
└── README.md          # Documentation
```

## Features

### Price Prediction Parameters
- **Living Area:** Total living area of the property in sq ft
- **Years Since Built:** Number of years since the property was built
- **Gas Station Count:** Count of gas stations within a 2-mile radius
- **Golf Course Count:** Count of golf courses within a 2-mile radius
- **Average Bar Rating:** Average rating of bars in a 0.5-mile radius
- **Household Income:** Median household income for the property's zipcode
- **Trader Joe's Distance:** Distance to the nearest Trader Joe's
- **Best School Rating:** Highest rating of an elementary school within 1-mile radius
- **Coast Distance:** Distance to the nearest coastline

### Visualizations
- Live rice prediciton
- Interactive California map showing house locations
- Color-coded pricing visualization
- Feature distribution histograms
- Feature importance chart

## Installation

### Prerequisites
```bash
sudo apt update && sudo apt install -y git python3 python3-pip python3-venv
```

### Clone Repository
```bash
git clone https://github.com/jmurata1/shiny-app.git
cd shiny-app
```

### Virtual Environment Setup
```bash
python3 -m venv shinyvenv
source shinyvenv/bin/activate
pip install -r requirements.txt
sudo ln -s /home/ubuntu/shiny-app /srv/shiny-server/shiny-app
```

## Configuration

Create a configuration file at `/etc/shiny-server/shiny-server.conf`:

```nginx
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
```