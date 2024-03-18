import base64
from io import BytesIO
from flask import Flask, render_template
from matplotlib.figure import Figure
from get_stue_dht11 import get_stue_data

app = Flask(__name__)

def stue_temp():
    timestamps, temp, hum = get_stue_data(20)

    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()

    fig.subplots_adjust(bottom=0.3)
    ax.tick_params(axis='x', which='both', rotation=65, labelsize=8)
    ax.set_facecolor("#DBF4A7") #indre ramme
    ax.plot(timestamps, temp, linestyle = "solid", c="#004E66", linewidth="2", marker="o", mec="#2374AB", mfc="#BFD7EA")
    ax.set_xlabel("Timestamps", fontsize=8)
    ax.set_ylabel("Temperature °C", fontsize=10)
    fig.patch.set_facecolor("#EBEBFF") #ydre ramme
    ax.tick_params(axis="x", colors="#000", labelsize=7) #timestamp tal
    ax.tick_params(axis="y", colors="#000", labelsize=7) #temp tal
    ax.spines["left"].set_color("#000") # y axis kant
    ax.spines["right"].set_color("#000") # y axis kant
    ax.spines["top"].set_color("#000") # y axis kant
    ax.spines["bottom"].set_color("#000") # y axis kant
    ax.grid(color='#DC1829', linestyle='--', linewidth=0.2)

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def stue_hum():
    timestamps, temp, hum = get_stue_data(20)
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    
    fig.subplots_adjust(bottom=0.3)
    ax.tick_params(axis='x', which='both', rotation=65, labelsize=8)
    ax.set_facecolor("#DBF4A7") #indre ramme
    ax.plot(timestamps, hum, linestyle = "solid", c="#BA1F33", linewidth="2", marker="o", mec="#2374AB", mfc="#BFD7EA")
    ax.set_xlabel("Timestamps", fontsize=8)
    ax.set_ylabel("Humidity %", fontsize=10)
    fig.patch.set_facecolor("#EBEBFF") #ydre ramme
    ax.tick_params(axis="x", colors="#000", labelsize=7) #timestamp farve tal
    ax.tick_params(axis="y", colors="#000", labelsize=7) #timestamp farve tal
    ax.spines["left"].set_color("#000") # y axis kant
    ax.spines["right"].set_color("#000") # y axis kant
    ax.spines["top"].set_color("#000") # y axis kant
    ax.spines["bottom"].set_color("#000") # y axis kant
    ax.grid(color='#DC1829', linestyle='--', linewidth=0.2)
    
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/room_1')
def room_1():
    stue_temperature = stue_temp()
    stue_humidity = stue_hum()
    print('Temperatur og fugtighed')
    return render_template('room_1.html', stue_temperature = stue_temperature, stue_humidity = stue_humidity)

@app.route('/room_2')
def room_2():
    return render_template('room_2.html')

@app.route('/room_3')
def room_3():
    return render_template('room_3.html')

@app.route('/room_4')
def room_4():
    return render_template('room_4.html')

if __name__ == '__main__':
    app.run(debug=True)
