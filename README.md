# Image Processing: Blur Reduction and Clarity Enhancement

A Python image-processing project that applies noise reduction, Fourier transformation, Richardson–Lucy deconvolution, contrast enhancement, and sharpening to an input image.

The script displays a side-by-side comparison containing **only two images**:

1. The original input image.
2. The transformed image.

The transformed image is also saved as `final_clear_image.jpg`.

## Features

- Loads an image using OpenCV.
- Converts the image from BGR to RGB.
- Converts the image to LAB colour space so that luminance can be processed separately from colour.
- Reduces noise using a bilateral filter.
- Calculates the Fourier transform of the luminance channel.
- Applies Richardson–Lucy deconvolution using a Gaussian point spread function.
- Improves local contrast with CLAHE.
- Sharpens the processed luminance channel.
- Reconstructs the colour image.
- Displays exactly two images side by side.
- Saves the final transformed image.

## Requirements

- Python 3.10 or later
- The packages listed in `requirements.txt`
- Visual Studio Code, PyCharm, or another Python editor (optional)

## Project files

```text
image-processing-project/
├── image_processing.py
├── blurred.jpg
├── README.md
├── requirements.txt
└── .gitignore
```

> **Important:** Save your Python script as `image_processing.py`, or change the run command below to match the actual script filename. Place the input image in the same folder and name it `blurred.jpg`.

## Installation and setup

### 1. Install Python

Install Python 3.10 or later. During installation on Windows, enable **Add Python to PATH** if that option is available.

### 2. Open the project folder

Open the project folder in Visual Studio Code or a terminal.

### 3. Create a virtual environment (recommended)

On Windows:

```bash
py -m venv .venv
.venv\Scripts\activate
```

On Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install the required packages

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5. Add the input image

Copy the image you want to process into the project folder and name it:

```text
blurred.jpg
```

The script expects this exact filename unless you change the argument in `cv2.imread("blurred.jpg")`.

### 6. Run the program

```bash
python image_processing.py
```

A Matplotlib window should open showing the original image and the transformed image side by side. Close the display window to allow the program to finish.

## Output

After a successful run, the script saves:

```text
final_clear_image.jpg
```

The output is saved in the same folder as the Python script.

## Troubleshooting

### `FileNotFoundError: Image not found!`

- Confirm that `blurred.jpg` is in the same folder from which you are running the script.
- Check the spelling and file extension.
- If your image has another name, update `cv2.imread("blurred.jpg")` accordingly.

### `ModuleNotFoundError`

Activate your virtual environment and install the dependencies:

```bash
python -m pip install -r requirements.txt
```

### Matplotlib does not display the comparison

Check that Matplotlib is installed and that your Python environment supports graphical windows. Run the script from a local desktop environment rather than a headless terminal.

## Important technical note

The Fourier spectrum is calculated in this script but is not currently used to reconstruct or restore the image. The Gaussian point spread function is an assumed blur model. Image restoration quality depends on how closely that model matches the actual blur.

Deconvolution and sharpening cannot reliably recover background details that were completely lost or never captured by the camera. The result may therefore improve perceived clarity without recreating the exact original scene.