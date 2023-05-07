import matplotlib.pyplot as plt
from random import random
from math import floor
import pandas as pd

# Read excel file using pandas
df = pd.read_excel('invest_reg.xlsx', sheet_name='Показатели', engine='openpyxl')

# Get the minimum and maximum investment activity values
min_val = df['Инвестиционная активность'].min()
max_val = df['Инвестиционная активность'].max()



def gradient(min_val, max_val, activity):
    """
    Convert investment activity values into a range from 0 to 1.
    Create a color gradient from yellow to red based on investment activity.
    """
    
    # Convert investment activity values into a range from 0 to 1.
    normalized_activity = (activity - min_val) / (max_val - min_val)
    
    # Create a color gradient from yellow to red based on investment activity.
    colors = plt.cm.Greens(normalized_activity)
    hex_colors = ['#%02x%02x%02x' % (int(color[0]*255), int(color[1]*255), int(color[2]*255)) for color in colors]

    return hex_colors


# def top_color_change():
#     color1 = floor(random() * 256)
#     color2 = floor(random() * 256)
#     color3 = floor(random() * 256)

#     rgb = 'rgb('+str(color1)+","+str(color2)+","+str(color3)+")"

#     return rgb