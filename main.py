import os
import sqlite3

from flask import Flask, render_template
from math import ceil, floor

import plot_creator_reg as plot_reg
import plot_creator_uzb as plot_uzb
from map_color import df as map_df, gradient, max_val, min_val
from region_classification import classification


app = Flask(__name__, static_folder='static')



def get_db_connection():
    """
    Creates a connection to the SQLite database
    """
    conn = sqlite3.connect('uzb_regions.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_db_conn_news():
    """
    Creates a connection to the SQLite database
    """
    conn = sqlite3.connect('news.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_news_title():
    conn = get_db_conn_news()

    by_title_news = conn.execute("SELECT title FROM news").fetchall()

    news_title = by_title_news

    conn.close()

    return news_title


reg_colors = gradient(min_val, max_val, map_df['Инвестиционная активность'])
reg_classify = classification()


@app.route("/")
def home():
    """
    Handles requests to the root URL
    """
    graph_json_population = plot_reg.population_bar(13)
    graph_json_gdp = plot_uzb.gdp_graph()
    return render_template('index.html', image_path="images/background_u.jpg",
                            graphJSON_population=graph_json_population, 
                            graphJSON_GDP=graph_json_gdp, reg_colors=reg_colors,
                            min_val=floor(min_val), max_val=ceil(max_val),
                            reg_classify=reg_classify, news_title=get_news_title())


@app.route("/<region>")
def region(region):
    """
    Handles requests to URLs with a `region` parameter
    """
    conn = get_db_connection()
    by_id_region = conn.execute("SELECT * FROM uzb_regions WHERE id = '" + region + "'").fetchall()

    graph_json_population = plot_reg.population_bar(region)
    graph_json_gdp = plot_reg.gdp_graph(region)
    graph_json_temp = plot_reg.growth_temp(region)
    graph_json_dev = plot_reg.inv_dev(region)
    graph_json_ipc = plot_reg.inv_per_capita(region)
    graph_json_ish = plot_reg.inv_share()

    population = plot_reg.df['Численность постоянного населения (тысяч чел)'][int(region)]
    population = '{0:,}'.format(population).replace(',', ' ')

    gdp = plot_reg.df['Объем ВРП за 2022 год'][int(region)]
    gdp = round(gdp, 2)
    gdp = '{0:,}'.format(gdp).replace(',', ' ')

    conn.close()

    try:
        text = open(app.static_folder+"/texts/"+region+".txt", "r", encoding="utf8")
        text_r = text.read()
        text.close()
        text_r_arr = text_r.split('\n')
    except:
        text_r_arr = 'нет текста'

    image_path = "images/background_"+region+".jpg"

    return render_template('region.html', population=population, gdp=gdp, 
                           region=region, by_id_region=by_id_region, 
                           image_path=image_path, 
                           text_arr=text_r_arr, graphJSON_population=graph_json_population, 
                           graphJSON_GDP=graph_json_gdp, graphJSON_temp = graph_json_temp,
                           graphJSON_ish=graph_json_ish, graphJSON_dev = graph_json_dev,
                           graphJSON_ipc = graph_json_ipc,reg_colors=reg_colors,
                           min_val=floor(min_val), max_val=ceil(max_val)
                           , news_title=get_news_title())


@app.route("/regions")
def regions_show():
    regions = plot_reg.df['Регионы']
    return render_template('regions_list.html', regions=regions, news_title=get_news_title())

@app.route("/news")
def news():
    return render_template('news_list.html' , news_title=get_news_title())

@app.route("/news/<news_id>")
def show_news(news_id):
    conn = get_db_conn_news()

    by_id_news = conn.execute("SELECT * FROM news WHERE id = '" + news_id + "'").fetchall()

    conn.close()

    return render_template('news.html', title=by_id_news[0][1], text=by_id_news[0][2], news_title=get_news_title())



@app.errorhandler(Exception)
def error_handler(error):
    return render_template('error.html', error_code=error.code), error.code

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
