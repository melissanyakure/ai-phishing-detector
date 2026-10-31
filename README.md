# AI-Based Phishing Email Detection System Using Machine Learning

## Project Overview

The AI-Based Phishing Email Detection System is a machine-learning application designed to identify potentially malicious phishing emails and distinguish them from legitimate emails.

The system uses Natural Language Processing (NLP) and machine-learning techniques to analyze email content and predict whether an email is phishing or legitimate.

It also provides URL scanning, detection history, dashboard statistics, and CSV report export.

## Features

- **Email Detection:** Classifies emails as phishing or legitimate.
- **Machine Learning:** Uses TF-IDF for text feature extraction and Logistic Regression for classification.
- **URL Scanner:** Examines URLs for basic suspicious indicators.
- **Detection History:** Stores previous detection results using SQLite.
- **Dashboard:** Displays total scans, phishing detections, legitimate emails, and phishing percentage.
- **CSV Export:** Allows users to export detection history reports.
- **Web Interface:** Provides an easy-to-use interface built with HTML and CSS.

## Technologies Used

- Python
- Flask
- Pandas
- Scikit-learn
- Natural Language Processing (NLP)
- TF-IDF Vectorization
- Logistic Regression
- SQLite
- HTML
- CSS

## Project Structure

```text
ai-phishing-detector/
│
├── dataset/
│   └── phishing_email.csv
│
├── model/
│   └── phishing_model.pkl
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
├── app.py
├── train_model.py
├── requirements.txt
├── README.md
└── .gitignore
```

**Note:** The dataset is stored locally and is not included in this GitHub repository because of its large file size.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/melissanyakure/ai-phishing-detector.git
```

### 2. Enter the Project Directory

```bash
cd ai-phishing-detector
```

### 3. Create a Virtual Environment

```bash
python3 -m venv venv
```

### 4. Activate the Virtual Environment

On Kali Linux:

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Obtain the Dataset

Download the Phishing Email Dataset by Naser Abdullah Alam from Kaggle and place it inside the `dataset` folder.

Make sure the filename is:

```text
phishing_email.csv
```

### 7. Train the Machine Learning Model (Optional)

If you want to retrain the model using the dataset, run:

```bash
python train_model.py
```

The trained model is saved in the `model` directory.

The repository already contains a trained model, so retraining is not necessary just to run the application.

### 8. Run the Application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

## Model Performance

The Logistic Regression model achieved approximately **98.59% accuracy** on the project's test dataset.

This is a test-set result and does not guarantee the same accuracy on real-world emails. Performance may vary depending on the data and email patterns.

## Security Notice

This project is intended for educational and demonstration purposes.

The URL scanner uses basic suspicious indicators and should not be considered a complete website security or malware detection solution. Always exercise caution when opening suspicious links or emails.

## Future Improvements

- Integrate real-time threat intelligence.
- Improve URL analysis and phishing detection.
- Add user authentication.
- Improve the machine-learning model using additional datasets.
- Develop more advanced email analysis features.

## Author

**Melissa Nyakure**

## License

This project is available for educational and learning purposes.

## Application Screenshots

### Dashboard
![Application Dashboard](screenshots/dashboard.png)

### Phishing Email Detection
![Phishing Detection Result](screenshots/phishing-detection.png)

### Detection History
![Detection History](screenshots/detection-history.png)
