from distutils.command.config import config
from shutil import copy2
from turtle import width
import plotly
import plotly.express as px
import json
from plotly.subplots import make_subplots
import plotly.graph_objects as go

class plot_graph():
    def __init__(self, data):
        self.data= data

    def plot_data(self):
        fig = make_subplots(rows= 1, cols= 2)
        fig.add_trace(go.Scatter(x=self.data[0], y=self.data[1]), row=1, col=1)
        fig.add_trace(go.Scatter(x=self.data[0], y=self.data[2]), row=1, col=2) 
        fig.update_xaxes(title_text = 'Time', row=1, col=1)
        fig.update_xaxes(title_text = 'Time', row=1, col=2)
        fig.update_yaxes(title_text = 'CO2', range = [0, 1500],row=1, col=1)
        fig.update_yaxes(title_text = 'Humidity', range = [0, 100], row=1, col=2)
        fig.update_layout(height=420, width= 900)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return graphJSON

