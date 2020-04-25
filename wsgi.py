from flask import Flask, render_template

application = Flask(__name__)

@application.route("/")
def home():
    return render_template("home.html")

@application.route('/about/')
def about():
    return render_template("about.html")

@application.route('/plot/')
def plot():
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure
    from bokeh.embed import components
    from bokeh.resources import CDN

    start = datetime.datetime(2020, 1, 1)
    end = datetime.datetime(2020, 4, 22)
    name = "TSLA"
    df = data.DataReader(name=name, data_source="yahoo", start=start, end=end)
    hours_12 = 12 * 60 * 60 * 1000
    # x axis is in millisecond, box to be 12 hrs.

    z = []
    for x, y in zip(df.Open, df.Close):
        if x > y:
            z.append("#00FFFF")
        else:
            z.append("#FF7F50")
    df["Status"] = z

    f = figure(x_axis_type='datetime', width=1000, height=300, sizing_mode="scale_width")
    f.grid.grid_line_alpha = 0.3
    f.title.text = "Candlestick Chart"
    f.title.align = "center"
    f.title.text_color = "Gray"
    f.title.text_font = "times"
    f.title.text_font_style = "bold"
    f.xaxis.minor_tick_line_color = None
    f.yaxis.minor_tick_line_color = None
    f.xaxis.axis_label = "Date"
    f.xaxis.axis_label_text_font_style = "italic"
    f.yaxis.axis_label = "Price"
    f.yaxis.axis_label_text_font_style = "italic"

    f.segment(df.index, df.High, df.index, df.Low, line_color="black")
    f.rect(df.index, (df.Open + df.Close) / 2, hours_12, abs(df.Open - df.Close), fill_color=df.Status,
           line_color="black")
    # gets overlayed, change the order as a layer

    script1, div1 = components(f)
    cdn_js = CDN.js_files[0]
    print(script1)
    return render_template("plot.html", script1=script1, div1=div1, cdn_js=cdn_js)

if __name__ == "__main__":
    application.run(debug=True)
