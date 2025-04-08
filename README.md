# ML-based-Optimization-of-IRR-in-RF-mixer-circuits

The project is a web-based platform built using Flask that enables users to optimize the Image Rejection Ratio (IRR) of a Gilbert Cell Mixer using pre-executed Jupyter Notebooks.

Key Features:
User Input: Upload IRR dataset and choose one of four application scenarios.

Notebook Execution: Based on user selection, the corresponding notebook is automatically run.

Output Extraction: The system extracts IRR (before and after), optimized Q-factor, and notch frequency from the notebook’s output JSON file.

Visualization: A bar chart displays IRR improvement, and optimized parameters are shown clearly on the interface.

Modular Setup: Each application has its own dedicated notebook and logic, making the system scalable and easy to maintain.

This project bridges hardware simulation with a user-friendly web interface, delivering accurate, fast, and visually interpretable IRR optimization.
