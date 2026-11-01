EXOPLANET TRANSIT DETECTION & LIGHT-CURVE ANALYSIS SYSTEM

Simple Python demonstration project.

Features
- Generates a synthetic noisy stellar light curve
- Injects repeating exoplanet transits
- Removes NaN values and strong outliers
- Normalizes and detrends brightness
- Detects candidate transit dips
- Estimates orbital period
- Estimates transit depth
- Estimates planet-to-star radius ratio Rp/Rs
- Displays raw, detrended, detected-transit and phase-folded plots
- Tkinter desktop interface

How to run

1. Install Python 3.
2. Install dependencies:

   pip install -r requirements.txt

3. Run:

   python main.py

The hidden synthetic planet has an orbital period close to 5 days and a transit
depth close to 1.2%, so the demo should recover values near those numbers.
