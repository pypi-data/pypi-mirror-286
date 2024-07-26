import re
import json
from flask import g, request, jsonify


class SanitizeEscapeExtension:
    def __init__(self, app=None, sanitize_quotes=True, custom_characters=None):
        self.sanitize_quotes = sanitize_quotes
        self.custom_characters = custom_characters or []
        if app is not None:
            self.init_app(app)

    def sanitize_string(self, value):
        # Remove all tags and attributes:
        value = re.sub(r"<[^>]+>", "", value, flags=re.IGNORECASE)

        if self.sanitize_quotes:
            # Escape quotes:
            value = value.replace("'", "''").replace('"', '""')

        # Escape custom characters
        for char in self.custom_characters:
            value = value.replace(char, "\\" + char)

        # Remove suspicious keywords and patterns (RCE):
        value = re.sub(
            r"exec|eval|system|import|open|os\.", "", value, flags=re.IGNORECASE
        )

        return value

    def sanitize_int(self, value):
        # Allow only digits and an optional leading minus sign
        value = re.sub(r"[^\d-]", "", str(value))

        # Prevent very large integers
        try:
            value = int(value)
            if abs(value) > 2147483647:
                raise ValueError("Integer value too large")
        except ValueError:
            value = 0

        return value

    def sanitize_json(self, json_data):
        """Recursively sanitize JSON data, handling strings and nested structures."""
        if isinstance(json_data, dict):
            return {key: self.sanitize_json(value) for key, value in json_data.items()}
        elif isinstance(json_data, list):
            return [self.sanitize_json(item) for item in json_data]
        elif isinstance(json_data, str):
            return self.sanitize_string(json_data)
        elif isinstance(json_data, int):
            return self.sanitize_int(json_data)
        else:
            return json_data  # Leave other data types untouched

    def init_app(self, app):
        @app.before_request
        def _sanitize_request_data():
            # Sanitize query parameters
            sanitized_args = {}
            for key, values in request.args.lists():
                sanitized_values = [self.sanitize_string(value) for value in values]
                sanitized_args[key] = (
                    sanitized_values[0]
                    if len(sanitized_values) == 1
                    else sanitized_values
                )
            g.sanitized_args = sanitized_args

            # Sanitize form data
            sanitized_form = {}
            for key, values in request.form.lists():
                sanitized_values = [self.sanitize_string(value) for value in values]
                sanitized_form[key] = (
                    sanitized_values[0]
                    if len(sanitized_values) == 1
                    else sanitized_values
                )
            g.sanitized_form = sanitized_form

            # Sanitize JSON data
            if request.is_json:
                try:
                    json_data = request.get_json()
                    g.sanitized_json = self.sanitize_json(json_data)
                except json.JSONDecodeError:
                    app.logger.warning("Invalid JSON data in request")
                    g.sanitized_json = None

                if g.sanitized_json is None:  # Add this line
                    return jsonify({"error": "Invalid JSON data in request"}), 400

