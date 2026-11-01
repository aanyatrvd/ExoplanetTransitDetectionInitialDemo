# Exoplanet Transit Detection Initial Demo

A Python-based demonstration project for detecting periodic exoplanet transit signals from stellar light-curve data.

The project simulates a noisy stellar light curve, performs preprocessing and detrending, detects repeated brightness dips, estimates the orbital period and transit depth, calculates the approximate planet-to-star radius ratio, and visualizes the result using multiple plots.

This repository represents the initial synthetic-data prototype. A later version will be extended to work with real-world Kepler or TESS observations.

---

## Project Overview

An exoplanet transit occurs when a planet passes in front of its host star from the observer's point of view.

During the transit, the planet blocks a small fraction of the star's light, producing a temporary decrease in measured brightness.

This brightness over time is called a light curve.

The objective of this project is to identify repeating transit-like dips hidden inside noisy time-series data.

The analysis pipeline is:

Raw Light Curve  
↓  
Remove Missing Values  
↓  
Remove Strong Outliers  
↓  
Normalize Flux  
↓  
Detrend Slow Variations  
↓  
Detect Transit Candidates  
↓  
Estimate Orbital Period  
↓  
Estimate Transit Depth  
↓  
Calculate Rp/Rs  
↓  
Phase Fold the Light Curve  
↓  
Display Results

---

## Features

- Generates a synthetic stellar light curve
- Adds random measurement noise
- Adds long-term brightness variation
- Inserts artificial exoplanet transits
- Introduces missing values and outliers for testing
- Removes invalid observations
- Uses robust outlier rejection
- Normalizes stellar flux
- Removes slow trends using a Savitzky-Golay filter
- Detects candidate transit events
- Estimates orbital period
- Estimates transit depth
- Calculates approximate planet-to-star radius ratio
- Produces a phase-folded light curve
- Displays results through a Tkinter desktop GUI

---

## Technologies Used

- Python
- NumPy
- SciPy
- Matplotlib
- Tkinter

---

## Main Scientific Concepts

### Light Curve

A light curve represents the measured brightness of a star as a function of time.

Flux = measured stellar brightness.

The normal brightness is normalized close to:

1.0

A transit appears as a temporary reduction below this value.

---

### Transit Detection

The synthetic planet produces repeated dips in stellar brightness.

The application converts downward dips into upward peaks using:

inverted_flux = 1 - normalized_flux

SciPy's peak-detection algorithm is then used to locate significant transit candidates.

---

### Data Cleaning

The generated dataset intentionally contains:

- Missing values
- Random measurement noise
- Strong outliers

Invalid values are removed before further analysis.

Outlier rejection is performed using the Median Absolute Deviation method, which is more robust to extreme values than the ordinary mean and standard deviation.

---

### Normalization

Flux is divided by its median value so the ordinary stellar brightness becomes approximately:

1.0

This makes relative brightness changes easier to analyze.

---

### Detrending

The raw light curve contains slow brightness variation that is not caused by the planet.

A Savitzky-Golay filter is used to estimate this long-term trend.

The measured flux is then divided by the estimated trend so short transit signals remain visible while slow variation is reduced.

---

### Orbital Period

If detected transit events occur at approximately:

2.5 days  
7.5 days  
12.5 days  
17.5 days  
22.5 days  
27.5 days

then the spacing is approximately:

5 days

Therefore the estimated orbital period is approximately:

P ≈ 5 days

---

### Transit Depth

Transit depth represents the fraction of stellar light blocked by the planet.

For normalized flux:

Transit Depth ≈ 1 - Minimum Transit Flux

For example:

Normal flux = 1.000  
Transit flux = 0.988

Transit depth:

1 - 0.988 = 0.012

or approximately:

1.2%

---

### Planet-to-Star Radius Ratio

For a simplified transit model:

Transit Depth ≈ (Rp / Rs)²

Therefore:

Rp / Rs ≈ √Transit Depth

where:

Rp = planet radius  
Rs = star radius

A transit depth of approximately 1.2% gives:

Rp / Rs ≈ 0.11

This means the planet's radius is roughly 11% of the star's radius.

---

### Phase Folding

Phase folding maps observations from multiple orbital cycles onto a single orbit.

Instead of displaying transits separately across 30 days, all repeated transit events are aligned around the same orbital phase.

This makes a periodic transit signal much easier to identify.

---

## Output Plots

The application displays four main plots.

### 1. Raw Light Curve

Shows the original synthetic observations containing:

- Noise
- Long-term trend
- Outliers
- Transit dips

### 2. Cleaned and Detrended Light Curve

Shows the signal after:

- Removing invalid observations
- Removing strong outliers
- Normalizing the flux
- Removing slow brightness trends

### 3. Detected Transit Candidates

Shows the processed light curve with detected transit events highlighted.

### 4. Phase-Folded Light Curve

Combines all orbital cycles into one phase range.

Repeated transit events align near orbital phase zero.

---

## Example Result

A typical run produces results similar to:

```text
EXOPLANET TRANSIT ANALYZER

Target:
Synthetic Demo Star

Original observations:
3000

Valid observations:
2968

Data points removed:
32

Candidate transit events:
6

Estimated orbital period:
≈ 5.0 days

Transit depth:
≈ 1.2%

Estimated Rp/Rs:
≈ 0.11

Transit candidate:
YES
```

Because random noise is generated each time, the exact values may vary slightly between runs.

---

## Synthetic Ground Truth

The demo intentionally generates a synthetic exoplanet with approximately:

Orbital Period:

5 days

Transit Depth:

1.2%

The purpose is to test whether the analysis pipeline can recover values close to the known ground truth.

---

## Project Structure

```text
ExoplanetTransitDemo/
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## How to Run

Clone the repository:

```bash
git clone https://github.com/aanyatrvd/ExoplanetTransitDetectionInitialDemo.git
```

Open the folder:

```bash
cd ExoplanetTransitDetectionInitialDemo
```

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run the application:

```bash
python3 main.py
```

The desktop interface will open automatically.

---

## Controls

Run Analysis

Processes the current synthetic light curve and displays the calculated results.

Generate New Demo

Creates another synthetic dataset with new random noise, outliers and missing observations while keeping the same underlying exoplanet model.

---

## Current Limitations

This repository is an initial proof-of-concept and does not yet represent a complete astronomical exoplanet-detection pipeline.

Current limitations include:

- Synthetic data only
- Simplified transit model
- Simple peak-based transit detection
- Period estimated from spacing between detected events
- Transit depth estimated from local minimum flux
- No stellar limb-darkening model
- No astronomical false-positive classification
- No telescope quality flags
- No real Kepler or TESS data

---

## Future Development

The refined version of this project may include:

- Real Kepler light curves
- Real TESS light curves
- Astropy integration
- Lightkurve integration
- FITS file support
- Box Least Squares period search
- Transit periodograms
- More advanced detrending
- Physical transit-model fitting
- Stellar limb darkening
- Transit duration estimation
- Multiple-planet detection
- False-positive analysis
- Machine-learning classification

---

## Why Synthetic Data Is Used First

Synthetic data provides known ground truth.

The true transit period and depth are known before analysis, allowing the output of the detection algorithm to be directly validated.

This makes the initial version useful for testing the complete signal-processing pipeline before applying it to real telescope observations.

---

## Author

Aanya Trivedi

B.Tech CSE II Year  

---

## Project Status

Initial Demo / Proof of Concept

This repository is intended as the first working prototype. A separate future repository will contain the refined real-world-data version using actual astronomical observations.
