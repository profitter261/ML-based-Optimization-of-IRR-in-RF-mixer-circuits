# ML-based-Optimization-of-IRR-in-RF-mixer-circuits

The project is a web-based platform built using Flask that enables users to optimize the Image Rejection Ratio (IRR) of a Gilbert Cell Mixer using pre-executed Jupyter Notebooks.

## Key Features:
1) User Input: Upload IRR dataset and choose one of four application scenarios.

2) Notebook Execution: Based on user selection, the corresponding notebook is automatically run.

3) Output Extraction: The system extracts IRR (before and after), optimized Q-factor, and notch frequency from the notebook’s output JSON file.

4) Visualization: A bar chart displays IRR improvement, and optimized parameters are shown clearly on the interface.

5) Modular Setup: Each application has its own dedicated notebook and logic, making the system scalable and easy to maintain.

This project bridges hardware simulation with a user-friendly web interface, delivering accurate, fast, and visually interpretable IRR optimization.

## Project Overview
This project demonstrates the **optimization of Image Rejection Ratio (IRR)** for a **Gilbert Cell Mixer** using AI/ML-assisted passive notch filter design. The IRR was optimized for four different applications: **Instrumentation, Radar, Satellite, and Wireless communication systems**. By processing HB analysis outputs from LTspice, the system significantly enhances the IRR and visualizes improvements.

---

## Tools & Requirements

### Simulators and Software
- **LTSpice** – For AC & HB analysis of Gilbert Cell Mixer and passive filters.
- **MATLAB** – For dataset generation and optimization computation.
- **Python** – For automation, visualization, and ML-based filter tuning.
- **GitHub** – For version control and documentation.

### Libraries
- `NumPy`, `Pandas` – Data handling
- `Matplotlib` – Visualization
- `Scikit-learn` – ML models for optimization
- `SciPy` – Signal processing and filter design

---

## Methodology

1. **Design a Gilbert Cell Mixer** circuit in LTSpice.
2. **Simulate HB analysis** to extract frequency, amplitude, and phase data.
3. **Apply passive notch filters** and calculate the optimized IRR using signal attenuation techniques.
4. **Use ML algorithms** to tune notch filter parameters per application need.
5. **Compare before-and-after IRR values** to assess the improvement.
6. **Visualize** the results using bar graphs.

---

## User Interface (UI)

The application features a simple, intuitive UI built using HTML/CSS/JavaScript with Python backend.

### Homepage
![UI Home](https://github.com/profitter261/ML-based-Optimization-of-IRR-in-RF-mixer-circuits/blob/main/Screenshot%202025-03-26%20110213.png)

### Dataset Upload Page
![UI Upload](https://github.com/profitter261/ML-based-Optimization-of-IRR-in-RF-mixer-circuits/blob/main/Gilbert%20cell%20mixer/Screenshot%202025-04-09%20224640.png)

---

## Results & Visualizations

### Instrumentation

![Instrumentation](https://github.com/profitter261/ML-based-Optimization-of-IRR-in-RF-mixer-circuits/blob/main/static/Instrumentation_irr_plot.png?raw=true)

### Radar Systems

![Radar](https://github.com/profitter261/ML-based-Optimization-of-IRR-in-RF-mixer-circuits/blob/main/static/Radar_irr_plot.png?raw=true)

### Satellite Communications

![Satellite](https://github.com/profitter261/ML-based-Optimization-of-IRR-in-RF-mixer-circuits/blob/main/static/Wireless_irr_plot.png?raw=true)

### Wireless Communication

![Wireless](https://github.com/profitter261/ML-based-Optimization-of-IRR-in-RF-mixer-circuits/blob/main/static/statics/Satellite_graph.png?raw=true)

---

## Observations

| Application      | Initial IRR (dB) | Optimized IRR (dB) |
|------------------|------------------|--------------------|
| Instrumentation  | 20               | 27                 |
| Radar            | 20               | 46                 |
| Satellite        | 20               | 52                 |
| Wireless         | 20               | 37                 |

- All applications saw a **minimum IRR gain of 7 dB**, with satellite showing the highest improvement.
- ML-based tuning of passive notch filters provided **precise optimization** without active circuit modifications.
- IRR enhancement was tailored for each application, ensuring robustness and adaptability.

---

## Outcome

**Significant enhancement of Image Rejection Ratio (IRR) using application-specific passive notch filters optimized through AI/ML techniques for Gilbert Cell Mixers.**

---

## Future Scope

- Extend to **active filters** for even higher IRR gains.
- Apply deep learning for real-time IRR correction.
- Embed this system into a **web dashboard** for live circuit performance tuning.

---

## Acknowledgements
- Guidance from academic mentors  
- Tools and support provided by LTSpice, MATLAB, and Python open-source community
