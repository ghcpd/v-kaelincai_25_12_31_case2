"""
Flask Web Application for Event Registration System (Fixed)
"""

from flask import Flask, request, jsonify, render_template
from .event_service import EventService, RegistrationError
import os


# Get the directory where this file is located
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__,
            template_folder=os.path.join(basedir, 'templates'),
            static_folder=os.path.join(basedir, 'static'))
event_service = EventService()


@app.route('/')
def index():
    """Serve the registration form"""
    return render_template('index.html')


@app.route('/api/register', methods=['POST'])
def register():
    """Handle registration API endpoint"""
    try:
        data = request.get_json()
        
        result = event_service.register_participant(
            name=data.get('name'),
            email=data.get('email'),
            event_datetime=data.get('event_datetime'),
            event_name="Tech Conference 2024"
        )
        
        return jsonify(result), 200
        
    except RegistrationError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }), 500


@app.route('/api/registrations', methods=['GET'])
def get_registrations():
    """Get all registrations"""
    return jsonify({
        "count": event_service.get_registration_count(),
        "registrations": event_service.get_registrations()
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
