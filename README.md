# shiny-app
A web application built using Python Shiny deployed on AWS EC2 to showcase house price prediction on selected features.  The app provides interactive visualizations and real-time price predictions for houses in California.

## URL: http://3.15.206.34

## Server Information
 EC2 Instance ID: i-08e7966db1d4837ec
 IP Address: 3.15.206.34

## Structure
shiny-app/
├── app.py              # Main application file
├── shinyvenv/          # Virtual environment
├── requirements.txt    # Python dependencies
├── shinykey.pem       # AWS key file
├── all_data.csv       # Cleaned dataset
├── house_price_model.joblib  # Trained model
└── README.md          # Documentation

## Price Prediction in Shiny App
  Interactive sliders for adjusting house features:
    - **livingArea**: Total living area of the property in sq ft.
    - **years_since_built**: Number of years since the property was built.
    - **GasStation_Count**: Count of gas stations within a 2-mile radius.
    - **GolfCourse_Count**: Count of golf courses within a 2-mile radius.
    - **average_bar_rating**: Average rating of bars in a 0.5-mile radius.
    - **household_income**: Median household income for the property's zipcode.
    - **TraderJoes_distance**: Distance to the nearest Trader Joe's.
    - **best_school_rating**: Highest rating of an elementary school within 1-mile radius.
    - **coast_distance**: Distance to the nearest coastline.

## Visualizations in Shiny App
    - Interactive California map showing house locations
    - Color-coded pricing visualization
    - Feature distribution histograms
    - Feature importance chart

## Shiny App Setup
    sudo apt install git
    sudo apt install python3
    sudo apt install python3-pip
    sudo apt install python3-venv
    git clone https://github.com/jmurata1/shiny-app.git

## Python Virtual Environment
    python3 -m venv shinyvenv
    source shinyvenv/bin/activate
    pip install -r Requirements.txt
    sudo ln -s /home/ubuntu/shiny-app /srv/shiny-server/shiny-app

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
