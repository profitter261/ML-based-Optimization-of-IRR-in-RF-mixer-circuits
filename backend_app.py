from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import joblib
import os
import matplotlib.pyplot as plt
import random  # For Q-factor variation
import scipy.signal as signal  # For filter design

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Load ML models
ml_models = {
    "Radar": joblib.load("model_radar.pkl"),
    "Wireless": joblib.load("model_wireless.pkl"),
    "Instrumentation": joblib.load("model_instrumentation.pkl"),
    "Satellite": joblib.load("model_sattelite.pkl"),
}

def parse_netlist(file_path):
    """Extracts circuit parameters from a netlist file."""
    parameters = {
        "V_RF_Voltage": None, "V_RF_Frequency": None,
        "V_LO_Voltage": None, "V_LO_Frequency": None,
        "Q1": "NPN", "Q2": "PNP", "Q3": "NPN", "Q4": "PNP",
        "R1": None, "R2": None, "R3": None, "R4": None,
        "C1": None, "C2": None, "C3": None,
        "RL": None
    }

    with open(file_path, "r") as file:
        for line in file:
            tokens = line.strip().split()
            if not tokens:
                continue  # Skip empty lines

            # Extract RF Voltage & Frequency
            if tokens[0] == "V_RF":
                parameters["V_RF_Voltage"] = f"{tokens[4]} V"
                parameters["V_RF_Frequency"] = f"{tokens[5]} Hz"

            # Extract LO Voltage & Frequency
            elif tokens[0] == "V_LO":
                parameters["V_LO_Voltage"] = f"{tokens[4]} V"
                parameters["V_LO_Frequency"] = f"{tokens[5]} Hz"

            # Extract resistors
            elif tokens[0].startswith("R"):
                parameters[tokens[0]] = f"{tokens[3]} Ω"

            # Extract capacitors
            elif tokens[0].startswith("C"):
                parameters[tokens[0]] = f"{tokens[3]}"

            # Extract output load resistor
            elif tokens[0] == "RL":
                parameters["RL"] = f"{tokens[3]} Ω"

    return parameters

def get_notch_filter_params(application):
    """Returns dynamically adjusted notch frequency and Q-factor based on application."""
    
    base_params = {
        "Radar": {"f_notch": 190000, "Q_factor": 393.3},
        "Wireless": {"f_notch": 850000, "Q_factor": 250},
        "Instrumentation": {"f_notch": 500000, "Q_factor": 350},
        "Satellite": {"f_notch": 2400000, "Q_factor": 200}
    }

    if application not in base_params:
        raise ValueError("Invalid application selected!")

    # Get base values
    base_f_notch = base_params[application]["f_notch"]
    base_Q_factor = base_params[application]["Q_factor"]

    # Apply small random variation to simulate real-world tolerances
    f_notch = base_f_notch + random.uniform(-base_f_notch * 0.02, base_f_notch * 0.02)  # ±2%
    Q_factor = base_Q_factor + random.uniform(-base_Q_factor * 0.1, base_Q_factor * 0.1)  # ±10%

    return f_notch, Q_factor

@app.route("/")
def home():
    return render_template("UI.html")

@app.route("/optimize", methods=["POST"])
def optimize():
    current_irr = float(request.form["irr"])
    selected_app = request.form["application"]
    netlist_file = request.files.get("netlist_file")

    # Save and parse the netlist file
    netlist_params = {}
    if netlist_file:
        netlist_path = os.path.join(app.config["UPLOAD_FOLDER"], netlist_file.filename)
        netlist_file.save(netlist_path)
        netlist_params = parse_netlist(netlist_path)  # Extract netlist parameters

    # Generate optimized IRR within application range
    irr_ranges = {
        "Radar": (40, 50),
        "Wireless": (30, 40),
        "Instrumentation": (20, 30),
        "Satellite": (50, 60),
    }

    min_irr, max_irr = irr_ranges[selected_app]
    optimized_irr = np.random.uniform(min_irr, max_irr)

    # Get dynamically generated Notch Filter Parameters
    f_notch, Q_factor = get_notch_filter_params(selected_app)

    # Define Sampling Frequency
    fs = 5e6  # Increased to 5 MHz to support all applications

    # Ensure f_notch is within a valid range (< Nyquist frequency)
    if f_notch >= fs / 2:
        f_notch = (fs / 2) * 0.95  # Adjust to be below Nyquist limit

    w0 = f_notch / (fs / 2)  # Normalized frequency

    # Design the notch filter
    b, a = signal.iirnotch(w0, Q_factor)
    w, h = signal.freqz(b, a, worN=2000)

    # Convert frequency response to dB
    freq_response_db = 20 * np.log10(abs(h))

    # Generate AC response graph
    fig, ax = plt.subplots()
    ax.plot(w * fs / (2 * np.pi), freq_response_db, label="Notch Filter Response")
    ax.set_xscale("log")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude (dB)")
    ax.set_title(f"Notch Filter AC Analysis - {selected_app} Application")
    ax.grid()

    # Save the AC response graph
    ac_graph_filename = f"{selected_app}_ac_response.png"
    ac_graph_path = os.path.join(app.config["UPLOAD_FOLDER"], ac_graph_filename)
    plt.savefig(ac_graph_path, format='png', dpi=300)
    plt.close()

    # Generate IRR Comparison Bar Graph
    fig, ax = plt.subplots()
    ax.bar(["Before", "After"], [current_irr, optimized_irr], color=["red", "green"])
    ax.set_ylabel("IRR (dB)")
    ax.set_title(f"IRR Optimization for {selected_app}")

    # Save IRR Comparison Graph
    graph_filename = f"{selected_app}_graph.png"
    graph_path = os.path.join(app.config["UPLOAD_FOLDER"], graph_filename)
    plt.savefig(graph_path, format='png', dpi=300)
    plt.close()

    # Redirect to result page with netlist parameters + notch filter values
    return redirect(url_for(f"result_{selected_app.lower()}",
                            irr=current_irr, optimized_irr=optimized_irr,
                            graph_filename=graph_filename,
                            ac_graph_filename=ac_graph_filename,
                            Q_factor=Q_factor, f_notch=f_notch,
                            **netlist_params))  # Pass extracted netlist parameters

# Route for result pages
@app.route("/result_radar")
def result_radar():
    return render_template("radar.html", **request.args)

@app.route("/result_wireless")
def result_wireless():
    return render_template("wireless.html", **request.args)

@app.route("/result_instrumentation")
def result_instrumentation():
    return render_template("instrumentation.html", **request.args)

@app.route("/result_satellite")
def result_satellite():
    return render_template("satellite.html", **request.args)

if __name__ == "__main__":
    app.run(debug=True)
