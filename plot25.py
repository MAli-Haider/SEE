#!/usr/bin/env python3
"""
plot_ev3_paths_wide_5.py
-----------------------
Generate overview figures of EV3 robot trajectories.
Changes versus the previous version:
  • Each figure now contains **up to five** paths instead of ten (BATCH_SIZE = 5).
  • Each subplot panel is larger (8×5 in) for improved readability while
    preserving the DPI setting.
Everything else—axis limits, tick spacing, CLI options, and file naming—remains the same.
"""

import argparse, glob, math, os, re, sys
from typing import Iterable, List

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ───── absolute search path ──────────────────────────────────────────────
ABS_GLOB = (r"C:\\Users\\User\\Desktop\\SEE_EV3_all 3 paths\\SEE_EV3"
            r"\\left csv\\rounded\\robot_path*.csv")

# ───── axis windows & MAJOR tick spacing (metres) ───────────────────────
X_MIN, X_MAX = -14,  0.6
X_STEP       =   1

Y_MIN, Y_MAX = -60.0,   1.0
Y_STEP       =   5.0
# ─────────────────────────────────────────────────────────────────────────

# Larger panels (in inches)
FIG_WIDTH_PER_PANEL  = 8.0
FIG_HEIGHT_PER_PANEL = 5.0

# Number of trajectories per output figure
BATCH_SIZE = 5

# ───── command-line options ─────────────────────────────────────────────
ap = argparse.ArgumentParser()
ap.add_argument("--save-prefix", metavar="NAME",
                help="write each batch to NAME_batchN.png/pdf/svg …")
ap.add_argument("--dpi", type=int, default=300)
ap.add_argument("--no-show", action="store_true")
args = ap.parse_args()

# ───── helpers ──────────────────────────────────────────────────────────

def natural_key(path: str):
    """Return the first integer embedded in *path* for natural sorting."""
    m = re.search(r"(\d+)", os.path.basename(path))
    return int(m.group(1)) if m else path


def chunks(seq: List[str], size: int = BATCH_SIZE) -> Iterable[List[str]]:
    """Yield successive *size*-element chunks from *seq*."""
    for i in range(0, len(seq), size):
        yield seq[i : i + size]

# ───── locate files ─────────────────────────────────────────────────────
FILES = sorted(glob.glob(ABS_GLOB), key=natural_key)
if not FILES:
    sys.exit(f"❌  No files matched:\n{ABS_GLOB}")
print(f"Found {len(FILES)} CSV files.")

# ───── batch plotting loop ──────────────────────────────────────────────
for b_idx, batch in enumerate(chunks(FILES), start=1):
    n = len(batch)
    # Choose a roughly square grid layout for the current figure
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)

    fig_width  = cols * FIG_WIDTH_PER_PANEL
    fig_height = rows * FIG_HEIGHT_PER_PANEL

    fig, axes = plt.subplots(rows, cols,
                             figsize=(fig_width, fig_height),
                             sharex=False, sharey=False)
    axes = axes.flatten()

    for ax, path in zip(axes, batch):
        df = pd.read_csv(path, sep=r"\s+|,", engine="python")

        ax.plot(df["x"], df["y"], linewidth=0.8)

        # major ticks & limits
        ax.set_xlim(X_MIN, X_MAX)
        ax.set_xticks(np.arange(X_MIN, X_MAX + X_STEP, X_STEP))
        ax.set_ylim(Y_MIN, Y_MAX)
        ax.set_yticks(np.arange(Y_MIN, Y_MAX + Y_STEP, Y_STEP))

        ax.grid(True, linestyle="--", linewidth=0.25)
        ax.set_aspect("auto")
        ax.set_xlabel("X [m]", fontsize=7)
        ax.set_ylabel("Y [m]", fontsize=7)
        ax.set_title(os.path.basename(path), fontsize=8)

    # hide any empty panes (when n < rows*cols)
    for ax in axes[n:]:
        ax.set_visible(False)

    fig.suptitle(f"EV3 robot paths — batch {b_idx}", y=0.96)
    fig.tight_layout()

    # save?
    if args.save_prefix:
        base, ext = os.path.splitext(args.save_prefix)
        if not ext:
            ext = ".png"
        out_file = f"{base}_batch{b_idx}{ext}"
        fig.savefig(out_file, dpi=args.dpi, bbox_inches="tight")
        print(f"✔ saved {out_file}")

    if args.no_show:
        plt.close(fig)

if not args.no_show:
    plt.show()
