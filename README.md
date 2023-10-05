RecaptchaV2-IA-Solver
=====================

This project automates the process of solving Google reCAPTCHAs using the Undetected WebDriver and a deep learning model. The main highlight of the project is the integration of the YOLOv8x (You Only Look Once) object detection model for identifying and selecting the correct images in the ReCaptcha Images.

## Features

- **YOLO Object Detection**: Utilizes the YOLO model for detecting objects in the CAPTCHA images. The model is loaded from a pre-trained .onnx file.
- **Dynamic & One-time Selection CAPTCHA Support**: The script can handle both dynamic reCAPTCHAs (where new images appear after selections) and one-time selection CAPTCHAs.
- **Proxy Support**: Allows the use of proxies with the WebDriver, which can be useful for evading IP-based limitations.
- **Recaptcha Token and Cookies Retrieval**: After solving the CAPTCHA, the script retrieves the reCAPTCHA token and cookies for further use.

## How To Use

To solve a reCAPTCHA on a given website, call the solver function with the URL of the site. Optionally, you can also pass cookies and proxy details.

```python
from recaptchaSolver import solver
data = solver("https://google.com/recaptcha/api2/demo")
print(data)

>>> {"recaptcha_token":"03AF...", "cookies":[{'domain': 'google.com', 'expiry': 1712089489, 'httpOnly': True, 'name': '_GRECAPTCHA', 'path': '/recaptcha', 'sameSite': 'None', 'secure': True, 'value': '09ABIyMg698...'}], "time_taken":42.43}
```

## Requirements

* python 3.x
* ultralytics

## Installation

1. Clone the repository
```bash
git clone https://github.com/LunaPy17/RecaptchaV2-IA-Solver
```

2. Install the required packages
```bash
pip install -r requirements.txt
```

3. Execute the app
```bash
python main.py
```

## License

This project is licensed under the MIT License [License](https://github.com/LunaPy17/BulletDroid/blob/main/LICENSE). See the LICENSE file for details.
