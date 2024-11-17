import matplotlib.pyplot as plt
import numpy as np
from shiny.express import ui, input, render
import pandas as pd
from shinywidgets import render_altair
import altair as alt
import joblib

# Define color palette
HOUSE_COLORS = {
    'primary': '#8B4513',     # Saddle brown - wood tones
    'background': '#FAF0E6',  # Linen - warm white
    'accent': '#CD853F',      # Peru - warm brown
    'text': '#3E2723',        # Dark brown - text color
    'gradient': ['#8B4513', '#A0522D', '#B8860B', '#CD853F', '#DEB887']
}

# California GeoJSON for map background
CALIFORNIA_GEOJSON = {
    "type": "Feature",
    "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [-124.4096, 41.9983], [-123.6237, 42.0024], [-123.1526, 42.0126],
            [-122.0073, 42.0075], [-121.2369, 41.9962], [-120.0037, 41.9947],
            [-119.9999, 39.0021], [-120.0006, 38.9999], [-117.9673, 37.5555],
            [-116.3694, 36.3594], [-115.4752, 35.7755], [-114.7368, 35.0075],
            [-114.7043, 34.8726], [-114.6342, 34.7107], [-114.6286, 33.9337],
            [-114.5682, 33.6978], [-114.4980, 33.4192], [-114.5270, 33.2806],
            [-114.7215, 32.7193], [-115.1913, 32.6929], [-117.3395, 32.5121],
            [-117.4817, 32.7834], [-118.0590, 33.7078], [-118.6290, 34.0233],
            [-119.3157, 34.3733], [-120.3689, 34.4749], [-120.7524, 34.6089],
            [-120.9528, 34.7363], [-121.2585, 34.9866], [-121.7746, 35.2157],
            [-122.3457, 35.9350], [-122.8868, 36.6906], [-123.2378, 37.2239],
            [-123.7420, 37.7783], [-123.8665, 38.2702], [-124.0479, 38.7587],
            [-124.3967, 39.7619], [-124.3611, 40.3827], [-124.4096, 41.9983]
        ]]
    }
}

# CSS styles
CSS_STYLES = f"""
    body {{
        font-family: 'Arial, sans-serif';
        background-color: {HOUSE_COLORS['background']};
        margin: 0;
        padding: 20px;
    }}
    .grid-container {{ display: grid; grid-template-columns: 300px 1fr; gap: 20px; }}
    .sidebar, .main-content, .card {{
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    .card {{ padding: 15px; margin-bottom: 20px; }}
    .map-container {{ height: 400px; width: 100%; border-radius: 8px; overflow: hidden; }}
    .prediction-box {{
        background-color: {HOUSE_COLORS['background']};
        padding: 15px;
        border-radius: 6px;
        margin-top: 20px;
        text-align: center;
        font-size: 1.2em;
        color: {HOUSE_COLORS['text']};
    }}
    .feature-description {{
        font-style: italic;
        color: {HOUSE_COLORS['text']};
        margin: 5px 0 15px 0;
    }}
    h3, h4 {{ color: {HOUSE_COLORS['primary']}; margin-bottom: 15px; }}
    hr {{ margin: 20px 0; border: none; border-top: 1px solid {HOUSE_COLORS['accent']}; }}
"""

# Feature configurations to keep interpretability
FEATURES_CONFIG = {
    "livingArea": {
        "description": "The total living area of the house in square feet.",
        "log_transform": True
    },
    "years_since_built": {
        "description": "The number of years since the house was built.",
        "log_transform": False
    },
    "GasStation_Count": {
        "description": "The number of gas stations within a two mile radius of the house.",
        "log_transform": False
    },
    "GolfCourse_Count": {
        "description": "The number of golf courses within a two mile radius of the house.",
        "log_transform": False
    },
    "average_bar_rating": {
        "description": "The average rating of bars within half a mile of the house.",
        "log_transform": False
    },
    "household_income": {
        "description": "The average household income of the house's zipcode.",
        "log_transform": True
    },
    "TraderJoes_distance": {
        "description": "The distance to the nearest Trader Joe's store in miles.",
        "log_transform": True
    },
    "best_school_rating": {
        "description": "The rating of the best school within a one mile.",
        "log_transform": False
    },
    "coast_distance": {
        "description": "The distance to the nearest coast in miles.",
        "log_transform": False
    }
}

def create_map_chart(data):
    """Create the interactive map visualization."""
    # Sample a subset of houses for better visualization
    map_data = data.sample(n=min(1000, len(data)))
    
    # Create California background
    background = alt.Chart(
        alt.Data(values=[CALIFORNIA_GEOJSON])
    ).mark_geoshape(
        fill='#f0f0f0',
        stroke='white',
        strokeWidth=1
    ).project(type='mercator')
    
    # Create selection parameter
    selection = alt.selection_point(
        name='select',
        on='mouseover',
        nearest=True,
        fields=['latitude', 'longitude']
    )
    
    # Create the main points layer
    points = alt.Chart(map_data).mark_circle(
        opacity=0.6
    ).encode(
        longitude='longitude:Q',
        latitude='latitude:Q',
        size=alt.Size(
            'livingArea:Q',
            scale=alt.Scale(domain=[map_data['livingArea'].min(), map_data['livingArea'].max()],
                          range=[50, 400]),
            title='Living Area (sq ft)'
        ),
        color=alt.Color(
            'price:Q',
            scale=alt.Scale(domain=[map_data['price'].min(), map_data['price'].max()],
                          range=HOUSE_COLORS['gradient']),
            title='Price ($)'
        ),
        tooltip=[
            alt.Tooltip('price:Q', title='Price', format='$,.0f'),
            alt.Tooltip('livingArea:Q', title='Living Area', format=',.0f'),
            alt.Tooltip('years_since_built:Q', title='Age (years)'),
            alt.Tooltip('best_school_rating:Q', title='School Rating'),
            alt.Tooltip('household_income:Q', title='Household Income', format='$,.0f'),
            alt.Tooltip('TraderJoes_distance:Q', title="Distance to Trader Joe's", format='.1f'),
            alt.Tooltip('GolfCourse_Count:Q', title='Golf Courses Nearby'),
            alt.Tooltip('average_bar_rating:Q', title='Avg Bar Rating', format='.1f')
        ]
    )
    
    # Create highlight layer
    highlight = points.mark_circle(
        size=400,
        opacity=0.3,
        stroke='white',
        strokeWidth=2
    ).encode(
        size=alt.value(400)
    ).transform_filter(
        selection
    )
    
    return (
        background + points + highlight
    ).properties(
        width=800,
        height=400,
        title=alt.TitleParams(
            text='Interactive House Location Map',
            subtitle='Larger points represent larger living area and darker points represents higher price. Hover over points for more details.'
        )
    ).configure_view(
        strokeWidth=0
    ).add_params(
        selection
    )

def create_altair_chart(data, x_field, chart_type='histogram'):
    """Create a reusable Altair chart."""
    if chart_type == 'histogram':
        return alt.Chart(data).mark_bar(
            color=HOUSE_COLORS['primary'],
            opacity=0.7
        ).encode(
            x=alt.X(f"{x_field}:Q", bin=True, title=x_field),
            y=alt.Y('count()', title="Frequency"),
        ).properties(height=300)
    return None

def make_prediction(model, input_data):
    """Make prediction with appropriate transformations."""
    input_df = pd.DataFrame([input_data])
    
    # Apply log transformations where needed
    for feature, config in FEATURES_CONFIG.items():
        if config['log_transform'] and feature in input_df.columns:
            input_df[feature] = np.log1p(input_df[feature])
    
    return model.predict(input_df)[0]

# Load data and model
df = pd.read_csv("all_data.csv")
best_model = joblib.load("house_price_model.joblib")

# UI Setup
ui.tags.head(ui.tags.style(CSS_STYLES))

with ui.div(class_="grid-container"):
    # Sidebar
    with ui.div(class_="sidebar"):
        ui.h3("House Price Predictor")
        ui.hr()
        ui.h4("Feature Distribution")
        ui.input_selectize("var", "Select variable to visualize", choices=list(FEATURES_CONFIG.keys()))
        
        @render.text
        def feature_description():
            return FEATURES_CONFIG[input.var()]["description"]
        
        ui.hr()
        ui.h4("Input Features")
        
        # Create sliders for each feature
        for feature in FEATURES_CONFIG.keys():
            min_val = float(df[feature].min())
            max_val = float(df[feature].max())
            step = max((max_val - min_val) / 100, 0.1)
            
            ui.input_slider(
                f"pred_{feature}",
                f"Select {feature}",
                min=min_val,
                max=max_val,
                value=(min_val + max_val) / 2,
                step=step
            )
    
    # Main content
    with ui.div(class_="main-content"):
        # Distribution Card
        with ui.div(class_="card"):
            ui.h4("Feature Distribution")
            @render_altair
            def hist():
                selected_var = input.var()
                return create_altair_chart(df.sample(n=5000, random_state=50), selected_var)
        
        # Prediction Card
        with ui.div(class_="card"):
            ui.h4("Prediction")
            @render.text
            def prediction():
                try:
                    input_values = {
                        feature: float(getattr(input, f"pred_{feature}")())
                        for feature in FEATURES_CONFIG.keys()
                    }
                    predicted_price = make_prediction(best_model, input_values)
                    return f"Predicted House Price: ${predicted_price:,.2f}"
                except Exception as e:
                    return f"Error making prediction: {str(e)}"
        
        # Map Card
        if 'latitude' in df.columns and 'longitude' in df.columns:
            with ui.div(class_="card"):
                ui.h4("House Locations")
                @render_altair
                def map_plot():
                    return create_map_chart(df)
        
        # Feature Importance Card
        with ui.div(class_="card"):
            ui.h4("Feature Importance")
            @render_altair
            def feature_importance():
                importances = best_model.named_steps['gradientboostingregressor'].feature_importances_
                importance_df = pd.DataFrame({
                    'feature': list(FEATURES_CONFIG.keys()),
                    'importance': importances
                })
                
                return alt.Chart(importance_df).mark_bar().encode(
                    x=alt.X('importance:Q', title='Importance Score'),
                    y=alt.Y('feature:N', sort='-x', title='Feature'),
                    color=alt.Color(
                        'importance:Q',
                        scale=alt.Scale(domain=[importance_df['importance'].min(), importance_df['importance'].max()],
                                      range=HOUSE_COLORS['gradient']),
                        legend=None
                    ),
                    tooltip=['feature', alt.Tooltip('importance:Q', format='.3f')]
                ).properties(height=300)
