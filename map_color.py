import numpy as np
import matplotlib.pyplot as plt

import pandas as pd

df = pd.read_excel('invest_reg.xlsx', sheet_name='Показатели', engine='openpyxl')

# Получение минимального и максимального значения инвестиционной активности
min_val = df['Инвестиционная активность'].min()
max_val = df['Инвестиционная активность'].max()



def gradient(min_val, max_val, activity):
    # Преобразование значений инвестиционной активности в диапазон от 0 до 1
    normalized_activity = (activity - min_val) / (max_val - min_val)
    
    # Создание градиента цветов от желтого к красному
    colors = plt.cm.Greens(normalized_activity)
    hex_colors = ['#%02x%02x%02x' % (int(color[0]*255), int(color[1]*255), int(color[2]*255)) for color in colors]
    
    return hex_colors

