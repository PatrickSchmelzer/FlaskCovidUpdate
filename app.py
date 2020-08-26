import flask
import covidData
import datetime
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates

app = flask.Flask(__name__)

@app.route("/")
def home():
    return flask.render_template("home.html", covidData=covidData.getCovidData(), inhabitants=covidData.getInhabitants())

@app.route("/plot/<country>")
def plot(country):
    casesPerDay, date, url = covidData.getDataPerCountry(country)
    fig=Figure()
    ax=fig.add_subplot(111)
    numdays = len(date)
    base = datetime.datetime.today() - datetime.timedelta(numdays)
    date_list = [base + datetime.timedelta(days=x) for x in range(0, numdays)]
    locator = mdates.MonthLocator()  # every month
    fmt = mdates.DateFormatter('%b')
    ax.plot_date(date_list, casesPerDay, '-')
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(fmt)
    ax.set_xlabel("Month")
    ax.set_ylabel("New Covid Cases")
    ax.grid()
    fig.suptitle(f"New Covid Cases in {country}", fontsize=16)
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    png_output = io.BytesIO()
    canvas.print_png(png_output)
    response=flask.make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response