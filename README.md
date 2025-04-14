# 🧠 Brain Tumor Detection using CNN

This project uses Convolutional Neural Networks (CNN) to detect brain tumors from MRI images. The pipeline includes preprocessing of images, model training, and prediction visualization to assist in medical image analysis.

## 🚀 Project Overview

- **Goal:** Accurately detect the presence of a brain tumor in MRI images.
- **Dataset:** MRI brain scan images categorized into `yes` (tumor) and `no` (no tumor).
- **Model Type:** Deep learning model built using TensorFlow and Keras.
- **Input Format:** RGB MRI images.
- **Output:** Tumor classification - Tumor present / Not present.

## 🛠️ Tech Stack

- Python
- TensorFlow / Keras
- OpenCV
- NumPy
- Matplotlib
- scikit-learn

## 📷 Image Preprocessing

Before passing images to the model, we:
- Convert to grayscale
- Apply Gaussian blur
- Perform binary thresholding
- Extract brain contours
- Crop the region of interest (ROI) to focus on the brain

## 📊 Model Performance

- **Model Architecture:** CNN with Conv2D, MaxPooling, BatchNorm, Dense layers
- **Loss Function:** Binary Crossentropy
- **Optimizer:** Adam
- **Accuracy Achieved:** ~98% on test data (depending on hyperparameters)


## 🧪 How to Run

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/brain-tumor-detection.git
    cd brain-tumor-detection
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the Jupyter Notebook:
    ```bash
    jupyter notebook Brain\ Tumor\ Detection-checkpoint.ipynb
    ```

## ✅ Results

| Metric     | Value |
|------------|-------|
| Accuracy   | 98%   |
| F1 Score   | 0.97  |
| Loss       | 0.06  |

> Note: These metrics may vary slightly depending on dataset split and preprocessing.

## 📌 Future Improvements

- Improve segmentation for noisy images
- Deploy model using a Flask/Django app
- Extend to multiclass tumor classification (glioma, meningioma, etc.)


---

