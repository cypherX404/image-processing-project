import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.restoration import richardson_lucy

# ==========================================
# STEP 1: LOAD ORIGINAL IMAGE
# ==========================================

image = cv2.imread("blurred.jpg")

if image is None:
    raise FileNotFoundError("Image not found! Check blurred.jpg")

# Convert BGR to RGB
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Convert RGB to LAB colour space
lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)

L, A, B = cv2.split(lab)

# ==========================================
# STEP 2: NOISE REDUCTION
# ==========================================

denoised = cv2.bilateralFilter(
    L,
    d=7,
    sigmaColor=40,
    sigmaSpace=40
)

# ==========================================
# STEP 3: FOURIER TRANSFORMATION
# ==========================================

fourier = np.fft.fft2(denoised)
fourier_shift = np.fft.fftshift(fourier)

frequency_spectrum = np.log1p(
    np.abs(fourier_shift)
)

# ==========================================
# STEP 4: CREATE GAUSSIAN POINT SPREAD FUNCTION
# ==========================================

def create_psf(size=15, sigma=2.0):

    x = np.arange(size) - size // 2
    y = np.arange(size) - size // 2

    X, Y = np.meshgrid(x, y)

    psf = np.exp(
        -(X**2 + Y**2) / (2 * sigma**2)
    )

    psf /= psf.sum()

    return psf


psf = create_psf(size=15, sigma=2.0)

# ==========================================
# STEP 5: RICHARDSON-LUCY DECONVOLUTION
# ==========================================

normalized = denoised.astype(np.float32) / 255.0

restored = richardson_lucy(
    normalized,
    psf,
    num_iter=25,
    clip=False
)

restored = np.clip(
    restored * 255, 0, 255
).astype(np.uint8)

# ==========================================
# STEP 6: IMPROVE IMAGE CONTRAST
# ==========================================

clahe = cv2.createCLAHE(
    clipLimit=2.0,
    tileGridSize=(8, 8)
)

enhanced = clahe.apply(restored)

# ==========================================
# STEP 7: SHARPEN IMAGE
# ==========================================

soft = cv2.GaussianBlur(
    enhanced,
    (0, 0),
    sigmaX=2.0
)

sharpened = cv2.addWeighted(
    enhanced,
    2.0,
    soft,
    -1.0,
    0
)

sharpened = np.clip(
    sharpened, 0, 255
).astype(np.uint8)

# ==========================================
# STEP 8: RECONSTRUCT COLOUR IMAGE
# ==========================================

final_lab = cv2.merge([
    sharpened,
    A,
    B
])

final_image = cv2.cvtColor(
    final_lab,
    cv2.COLOR_LAB2RGB
)

# ==========================================
# STEP 9: DISPLAY ONLY TWO IMAGES
# ==========================================

plt.figure(figsize=(14, 7))

# Original image
plt.subplot(1, 2, 1)
plt.imshow(image)
plt.title("ORIGINAL BLURRED IMAGE", fontsize=14)
plt.axis("off")

# Transformed image
plt.subplot(1, 2, 2)
plt.imshow(final_image)
plt.title("TRANSFORMED IMAGE - IMPROVED CLARITY", fontsize=14)
plt.axis("off")

plt.tight_layout()
plt.show()

# ==========================================
# STEP 10: SAVE FINAL RESULT
# ==========================================

final_bgr = cv2.cvtColor(
    final_image,
    cv2.COLOR_RGB2BGR
)

cv2.imwrite(
    "final_clear_image.jpg",
    final_bgr
)

print("--------------------------------")
print("IMAGE PROCESSING COMPLETED!")
print("--------------------------------")
print("Original image: blurred.jpg")
print("Final image: final_clear_image.jpg")
print("Only two images displayed!")
