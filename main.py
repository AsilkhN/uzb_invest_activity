from flask import Flask, render_template
import plot_creator_reg as plcr
import plot_creator_uzb as plc_uzb
from map_color import gradient, min_val, max_val
from map_color import df as map_df
import sqlite3
import os
from math import ceil, floor

app = Flask(__name__, static_folder='static')

# Define a function that creates a connection to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('uzb_regions.db')
    conn.row_factory = sqlite3.Row
    return conn

reg_colors = gradient(min_val, max_val, map_df['Инвестиционная активность'])

# Define a view function that handles requests to the root URL `/`
@app.route("/")
def home():
    graphJSON_population = plcr.population_bar(13)
    graphJSON_GDP = plc_uzb.gdp_graph()
    return render_template('index.html', image_path = "images/background_.jpg",
                            graphJSON_population = graphJSON_population, 
                           graphJSON_GDP = graphJSON_GDP, reg_colors = reg_colors,
                           min_val = floor(min_val), max_val=ceil(max_val))

# Define a view function that handles requests to URLs with a `region` parameter
@app.route("/<region>")
def region(region):

    #Connecting to DB
    conn = get_db_connection()
    by_id_region = conn.execute("Select * from uzb_regions where id = '" + region + "'").fetchall()

    graphJSON_population = plcr.population_bar(region)
    graphJSON_GDP = plcr.gdp_graph(region)

    population = plcr.df['Численность постоянного населения (тысяч чел)'][int(region)]
    population = '{0:,}'.format(population).replace(',', ' ')

    gdp = plcr.df['Объем ВРП за 2022 год'][int(region)]
    gdp = round(gdp, 2)
    gdp = '{0:,}'.format(gdp).replace(',', ' ')
    conn.close()
    #Getting text about the region
    try:
        text = open(app.static_folder+"/texts/"+region+".txt", "r", encoding="utf8")
        text_r = text.read()
        text.close()
        text_r_arr = text_r.split('\n')
    except:
        text_r_arr = 'нет текста'

    return render_template('regions.html',population = population, gdp = gdp, region = region, by_id_region = by_id_region, image_path = "images/background_"+region+".jpg", text_arr = text_r_arr,graphJSON_population = graphJSON_population, graphJSON_GDP = graphJSON_GDP, reg_colors = reg_colors)

@app.route("/regions")
def regions_show():
    return "Здесь будет список регионов"

@app.route("/news")
def news():
    return "Здесь должны быть новости"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
