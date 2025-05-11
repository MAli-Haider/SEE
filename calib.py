import cv2, glob, numpy as np, os, pandas as pd

pattern = (9, 6)                    # inner‑corner grid
sq = 0.024                           # side length in metres
objp = np.zeros((np.prod(pattern), 3), np.float32)
objp[:, :2] = np.mgrid[0:pattern[0], 0:pattern[1]].T.reshape(-1, 2)
objp *= sq

objpoints, imgpoints, used = [], [], []
flags = cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_NORMALIZE_IMAGE
criteria = (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-3)

for f in sorted(glob.glob('img_*.png')):
    gray = cv2.cvtColor(cv2.imread(f), cv2.COLOR_BGR2GRAY)
    ok, corners = cv2.findChessboardCorners(gray, pattern, flags)
    if not ok:
        continue
    corners = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
    objpoints.append(objp.copy())
    imgpoints.append(corners)
    used.append(os.path.basename(f))

h, w = gray.shape
rms, K, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, (w, h), None, None)

# per‑image reprojection error
errs = []
for f, op, ip, rv, tv in zip(used, objpoints, imgpoints, rvecs, tvecs):
    proj,_ = cv2.projectPoints(op, rv, tv, K, dist)
    errs.append([f, cv2.norm(ip, proj, cv2.NORM_L2)/len(proj)])

print('RMS reprojection error:', rms)
print('K:\n', K)
print('dist:', dist.ravel())
print(pd.DataFrame(errs, columns=['image', 'error_px']))
