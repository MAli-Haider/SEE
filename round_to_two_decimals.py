
#!/usr/bin/env python3
"""
Fix-and-round robot_path*.csv that are SPACE-delimited (x  y  theta).

After running you’ll get:
    rounded/robot_path1.csv  … robot_path25.csv
each with numbers shown as 'xx.yy'.
"""
import glob, os, pandas as pd

SRC_GLOB  = "C:\\Users\\User\\Desktop\\SEE_EV3_all 3 paths\\SEE_EV3\\forward csv\\robot_path*.csv"
DST_DIR   = "C:\\Users\\User\\Desktop\\SEE_EV3_all 3 paths\\SEE_EV3\\forward csv\\rounded\\"          # change to "." if you want to overwrite
COLS      = ["x", "y", "theta"]

os.makedirs(DST_DIR, exist_ok=True)

for f in sorted(glob.glob(SRC_GLOB)):
    # 1️⃣ correct parsing: whitespace-delimited, no header
    df = pd.read_csv(
        f,
        sep=r"\s+",
        header=None,
        names=COLS,          # x  y  theta
        engine="python"
    )

    # 2️⃣ round numeric columns
    df = df.round(2)         # or df[COLS] = df[COLS].round(2)

    # 3️⃣ save with two-decimal text formatting
    out = os.path.join(DST_DIR, os.path.basename(f))
    df.to_csv(out, index=False, float_format="%.2f")
    print(f"✔ saved {out}")

print("All files parsed and rounded.")
