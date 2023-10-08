RecaptchaV2-IA-Solver
=====================

This project automates the process of solving Google reCAPTCHAs using the Undetected WebDriver and a deep learning model. The main highlight of the project is the integration of the YOLOv8x (You Only Look Once) object detection model for identifying and selecting the correct images in the ReCaptcha Images.

https://github.com/LunaPy17/RecaptchaV2-IA-Solver/assets/69711934/9b0072ef-3e67-47e0-bb4f-ffe9ae6ec54f

## Features

- **YOLO Object Detection**: Utilizes the YOLO model for detecting objects in the CAPTCHA images. The model is loaded from a pre-trained .onnx file.
- **Dynamic & One-time Selection CAPTCHA Support**: The script can handle both dynamic reCAPTCHAs (where new images appear after selections) and one-time selection CAPTCHAs.
- **Proxy Support**: Allows the use of proxies with the WebDriver, which can be useful for evading IP-based limitations.
- **Recaptcha Token and Cookies Retrieval**: After solving the CAPTCHA, the script retrieves the reCAPTCHA token and cookies for further use.

## How To Use

To solve a reCAPTCHA on a given website, call the solver function with the URL of the site. Optionally, you can also pass cookies and proxy details.
You can download the model form [Dropbox](https://www.dropbox.com/scl/fi/srwinrdyxe4h8e104mqll/yolov8x.onnx?rlkey=uh1ra9b5bsgg822e7ojfv0cd4&dl=0)

```python
from recaptchaSolver import solver

data = solver("https://google.com/recaptcha/api2/demo")
print(data)

>>> {'recaptcha_token': '03AFcWeA5DAmOX4jOxRT0UtebPHstpHiAy8DCeYgFG1vcekDPVsSRHOsC-ELzjJIohG4wgOQwyK6gHIsJayzswis7qJOZPXDVplKRNG1Y3lM7oQoxdDwFCxsBAez-507jeyaGRwuXc2FYtrjslR2Q8tCRPaYz5vO07LY1nU-jZf4k6rehzQk6cX2Psdh_9EgF9yRteWemWiqFkx4TLMZjeVnCe18GPN1HQwNMiFwJK5IBubaJnyNsf3svbWnTMoTZKodGiU4S-cz6iEmkuIHZvunaW3G8C4WqAQdtgRxpHiu5yywgjJOOWdwwfO8lKKZv7569tNG9Zk9bhnrYNuuV_Mr2PT0SmqSyd5fuJKVaxA1qKOP5-36b5w09jJbKoEAjlTuplaWSbTkFEMsKQzG0MKFBPECybIHLelx5Eu7p5qK0frQBp-NMCvISdu282gSymqoVDMAlnC3DiKmAAdhB2o9ls7mFnMPvd55YIkhWjcFdknU3nA4cwZ6QHLVYVy88-S6bz_AeG_WrI50oPja19ppNoR4M3edaSU00Sjz3rgnAc0_kYJKPLoyll62oVhoOFuA4DCXgvVqvw', 'cookies': [{'domain': 'www.google.com', 'expiry': 1712090971, 'httpOnly': True, 'name': '_GRECAPTCHA', 'path': '/recaptcha', 'sameSite': 'None', 'secure': True, 'value': '09ABIyMg4lTwpqPFVOodY277MdxyhTyieMCdLi-lvuETHxnScwGYQL6vDW4tXuk6kMsha7nSpY144xhV9y2LyaGug'}], 'time_taken': 23.59}
```

Note: You must install the seleniumwire certificate following these [instructions](https://github.com/wkeeling/selenium-wire#certificates)

## Requirements

* python 3.x
* ultralytics
* undetected_chromedriver
* selenium-wire
* selenium

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
