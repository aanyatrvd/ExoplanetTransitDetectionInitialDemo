
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, find_peaks
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ExoplanetTransitDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Exoplanet Transit Detection & Light-Curve Analysis")
        self.root.geometry("1200x760")

        self.time = None
        self.raw_flux = None
        self.clean_flux = None
        self.detrended_flux = None
        self.transit_times = []
        self.period = None
        self.depth = None
        self.radius_ratio = None

        self.build_ui()
        self.generate_demo_data()
        self.analyze_data()

    def build_ui(self):
        top = ttk.Frame(self.root, padding=10)
        top.pack(fill="x")

        title = ttk.Label(
            top,
            text="EXOPLANET TRANSIT ANALYZER",
            font=("Arial", 20, "bold")
        )
        title.pack(side="left")

        ttk.Button(
            top,
            text="Generate New Demo",
            command=self.regenerate
        ).pack(side="right", padx=5)

        ttk.Button(
            top,
            text="Run Analysis",
            command=self.analyze_data
        ).pack(side="right", padx=5)

        main = ttk.Frame(self.root, padding=10)
        main.pack(fill="both", expand=True)

        self.left = ttk.Frame(main)
        self.left.pack(side="left", fill="both", expand=True)

        self.right = ttk.LabelFrame(
            main,
            text="Analysis Results",
            padding=15
        )
        self.right.pack(side="right", fill="y", padx=(10, 0))

        self.result_text = tk.Text(
            self.right,
            width=36,
            height=28,
            font=("Courier New", 11)
        )
        self.result_text.pack()

        self.figure, self.axes = plt.subplots(2, 2, figsize=(9, 6))
        self.figure.tight_layout(pad=3)

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=self.left
        )
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def generate_demo_data(self):
        rng = np.random.default_rng()

        # 30 days of observations
        self.time = np.linspace(0, 30, 3000)

        # Slow stellar/instrument trend
        trend = (
            1.0
            + 0.004 * np.sin(2 * np.pi * self.time / 18)
            + 0.0015 * (self.time / self.time.max())
        )

        # Random measurement noise
        noise = rng.normal(0, 0.0015, len(self.time))

        self.raw_flux = trend + noise

        # Hidden synthetic exoplanet
        true_period = 5.0
        transit_depth = 0.012
        transit_duration = 0.28

        for center in np.arange(2.5, 30, true_period):
            in_transit = np.abs(self.time - center) < transit_duration / 2
            self.raw_flux[in_transit] -= transit_depth

        # Add missing data
        nan_indices = rng.choice(
            len(self.time),
            size=20,
            replace=False
        )
        self.raw_flux[nan_indices] = np.nan

        # Add a few obvious outliers
        valid = np.setdiff1d(
            np.arange(len(self.time)),
            nan_indices
        )
        outlier_indices = rng.choice(
            valid,
            size=12,
            replace=False
        )

        self.raw_flux[outlier_indices] += rng.choice(
            [-0.04, 0.04],
            size=len(outlier_indices)
        )

    def clean_and_detrend(self):
        mask = np.isfinite(self.time) & np.isfinite(self.raw_flux)

        time = self.time[mask]
        flux = self.raw_flux[mask]

        # Robust outlier rejection using median absolute deviation
        median = np.median(flux)
        mad = np.median(np.abs(flux - median))

        if mad == 0:
            mad = np.std(flux)

        robust_z = 0.6745 * (flux - median) / mad
        keep = np.abs(robust_z) < 6

        self.clean_time = time[keep]
        self.clean_flux = flux[keep]

        # Normalize around 1
        self.clean_flux = self.clean_flux / np.median(self.clean_flux)

        # Remove slow trend
        window = 301
        if window >= len(self.clean_flux):
            window = len(self.clean_flux) - 1

        if window % 2 == 0:
            window -= 1

        trend = savgol_filter(
            self.clean_flux,
            window_length=max(window, 11),
            polyorder=2
        )

        self.detrended_flux = self.clean_flux / trend

        return len(self.raw_flux) - len(self.clean_flux)

    def detect_transits(self):
        # Search for downward dips as peaks in inverted flux
        inverted = 1.0 - self.detrended_flux

        peaks, properties = find_peaks(
            inverted,
            height=0.004,
            distance=300,
            prominence=0.003
        )

        self.transit_times = self.clean_time[peaks]

        if len(self.transit_times) >= 2:
            intervals = np.diff(self.transit_times)
            self.period = float(np.median(intervals))
        else:
            self.period = None

        if len(peaks) > 0:
            local_depths = []

            for p in peaks:
                start = max(0, p - 15)
                end = min(len(self.detrended_flux), p + 16)
                local_depths.append(
                    1.0 - np.min(
                        self.detrended_flux[start:end]
                    )
                )

            self.depth = float(np.median(local_depths))
            self.radius_ratio = np.sqrt(
                max(self.depth, 0)
            )
        else:
            self.depth = None
            self.radius_ratio = None

    def analyze_data(self):
        try:
            removed = self.clean_and_detrend()
            self.detect_transits()
            self.update_results(removed)
            self.update_plots()
        except Exception as exc:
            messagebox.showerror(
                "Analysis Error",
                str(exc)
            )

    def update_results(self, removed):
        self.result_text.delete("1.0", tk.END)

        candidate = (
            "YES"
            if self.period is not None
            and len(self.transit_times) >= 3
            else "UNCERTAIN"
        )

        period_text = (
            f"{self.period:.2f} days"
            if self.period is not None
            else "Not detected"
        )

        depth_text = (
            f"{self.depth * 100:.2f}%"
            if self.depth is not None
            else "Not detected"
        )

        ratio_text = (
            f"{self.radius_ratio:.3f}"
            if self.radius_ratio is not None
            else "N/A"
        )

        text = f"""
--------------------------------
EXOPLANET TRANSIT ANALYZER
--------------------------------

Target:
Synthetic Demo Star

Original observations:
{len(self.time)}

Valid observations:
{len(self.clean_time)}

Data points removed:
{removed}

Candidate transit events:
{len(self.transit_times)}

Estimated orbital period:
{period_text}

Transit depth:
{depth_text}

Estimated Rp/Rs:
{ratio_text}

Transit candidate:
{candidate}

--------------------------------
"""

        self.result_text.insert(tk.END, text)

    def update_plots(self):
        for ax in self.axes.flatten():
            ax.clear()

        # Raw
        ax = self.axes[0, 0]
        ax.plot(
            self.time,
            self.raw_flux,
            ".",
            markersize=2
        )
        ax.set_title("1. Raw Light Curve")
        ax.set_xlabel("Time (days)")
        ax.set_ylabel("Flux")

        # Cleaned / detrended
        ax = self.axes[0, 1]
        ax.plot(
            self.clean_time,
            self.detrended_flux,
            ".",
            markersize=2
        )
        ax.axhline(
            1.0,
            linewidth=1,
            linestyle="--"
        )
        ax.set_title("2. Cleaned & Detrended")
        ax.set_xlabel("Time (days)")
        ax.set_ylabel("Normalized Flux")

        # Detected transit events
        ax = self.axes[1, 0]
        ax.plot(
            self.clean_time,
            self.detrended_flux,
            ".",
            markersize=2
        )

        if len(self.transit_times) > 0:
            for t in self.transit_times:
                ax.axvline(
                    t,
                    linestyle="--",
                    alpha=0.6
                )

        ax.set_title("3. Detected Transit Candidates")
        ax.set_xlabel("Time (days)")
        ax.set_ylabel("Normalized Flux")

        # Phase folded
        ax = self.axes[1, 1]

        if self.period is not None:
            t0 = self.transit_times[0]

            phase = (
                ((self.clean_time - t0) / self.period + 0.5)
                % 1
            ) - 0.5

            order = np.argsort(phase)

            ax.plot(
                phase[order],
                self.detrended_flux[order],
                ".",
                markersize=2
            )

            ax.set_xlabel("Orbital Phase")
            ax.set_ylabel("Normalized Flux")
            ax.set_title("4. Phase-Folded Light Curve")
        else:
            ax.text(
                0.5,
                0.5,
                "Period not detected",
                ha="center",
                va="center",
                transform=ax.transAxes
            )
            ax.set_title("4. Phase-Folded Light Curve")

        self.figure.tight_layout(pad=2.5)
        self.canvas.draw()

    def regenerate(self):
        self.generate_demo_data()
        self.analyze_data()


if __name__ == "__main__":
    root = tk.Tk()
    app = ExoplanetTransitDemo(root)
    root.mainloop()
