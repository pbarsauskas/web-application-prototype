from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from models import DATABASE
matplotlib.use('TkAgg')
plt.style.use('seaborn-whitegrid')

def update_graph():
    df = pd.DataFrame(DATABASE.execute_sql('select input1 from dataentry').fetchall())
    fig = plt.figure()
    fig.suptitle('Graph', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)
    ax.plot(df)
    canvas = FigureCanvas(plt.gcf())
    output = BytesIO()
    canvas.print_png(output)
    return output.getvalue()