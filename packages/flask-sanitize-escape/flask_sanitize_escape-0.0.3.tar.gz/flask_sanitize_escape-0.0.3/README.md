# Flask-Sanitize-Escape 🛡️

[![PyPI Version](https://img.shields.io/pypi/v/flask-sanitize-escape)](https://pypi.org/project/flask-sanitize-escape/)
[![Github Build](https://github.com/mayur19/flask-sanitize-escape/actions/workflows/publish_to_pypi.yml/badge.svg)](https://github.com/mayur19/flask-sanitize-escape/actions/workflows/publish_to_pypi.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/release/python-3116/)
[![Flask Version](https://img.shields.io/badge/flask-2.x-green.svg)](https://flask.palletsprojects.com/en/2.3.x/)


A Flask middleware extension for automatic input sanitization, guarding against common web vulnerabilities like XSS, SQL injection, and other code injection attacks.


## Key Features

- **Effortless Integration:**  Works in the middleware
- **Automatic Protection:** Sanitizes incoming request data without requiring manual intervention in your route handlers.
- **Comprehensive Coverage:** Scrubs query parameters, form data, and JSON payloads.
- **Targeted Defense:** Neutralizes malicious code through HTML entity encoding and regex-based filtering.
- **Customizable:** Easily adapt the sanitization logic to your specific application's needs.
- **Custom Escaping:** Seamless custom escaping for specific characters as you need.

## Installation

```bash
pip install flask-sanitize-escape
```

## Usage

#### 1. Activate Middleware:
```python
from flask import Flask
from flask_sanitize_escape import SanitizeEscapeExtension  

app = Flask(__name__)

# Initialize the extension with options
sanitize_extension = SanitizeEscapeExtension(
    app, sanitize_quotes=True, custom_characters=["$", "#", "%"]
)

sanitize_extension.init_app(app) # Register the middleware
```
---
**NOTE**

It is suggested to use ```sanitize_quotes=True```

---
#### 2. Relax! Your application's input data is now automatically sanitized before it reaches your route handlers.

## Example
```python
@app.route('/submit', methods=['POST'])
def submit_data():
    data = g.sanitized_json  # accessing JSON from request.get_json()
    data = g.sanitized_args  # accessing arguments from request.args
    data = g.sanitized_form  # accessing values from request.form

    # Safely process the sanitized data...
```

## Customization
Stay tune for upcoming version

## Contributing
We welcome contributions! Feel free to open issues for bugs or feature requests, or submit pull requests with improvements.

## License
This project is licensed under the MIT License - see the LICENSE file for details.