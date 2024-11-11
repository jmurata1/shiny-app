import matplotlib.pyplot as plt
import numpy as np
from shiny.express import ui, input, render
import pandas as pd
from shinywidgets import render_altair
import altair as alt

# Load your data (adjust path to your file location)
df = pd.read_csv('/Users/jaydenmurata/Shiny/final_cleaned_dataset.csv')

ui.input_selectize("var", "Select variable", choices=df.columns.tolist())

@render_altair
def hist():
    return (
        alt.Chart(df)
        .mark_bar()
        .encode(x=alt.X(f"{input.var()}:Q", bin=True), y="count()")
    )




# with ui.sidebar():
#     ui.input_slider("n", "N", 0, 100, 20)

# @render.plot(alt="A histogram")
# def histogram():
#     np.random.seed(19680801)
#     x = 100 + 15 * np.random.randn(437)
#     plt.hist(x, input.n(), density=True)
