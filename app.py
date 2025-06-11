from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Mail configuration
app.config['MAIL_SERVER'] = 'mail.hoofstad.co.ke'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'info@hoofstad.co.ke'
app.config['MAIL_PASSWORD'] = 'taN7TyVKTgkRMKh'
app.config['MAIL_DEFAULT_SENDER'] = 'info@hoofstad.co.ke'

mail = Mail(app)

# ✅ Route to serve your index.html
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')  # Ensure index.html exists in templates/

# ✅ API route to handle contact form submission
@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        data = request.form  # or request.get_json() if you're sending JSON
        name = data['name']
        email = data['email']
        service = data['service']
        phone = data.get('phone', 'Not provided')
        message = data['message']
        
        msg = Message(
            subject=f"New Contact Form Submission - {service}",
            recipients=["caleb.muteti@hoofstad.co.ke"],
            body=f"""
Name: {name}
Email: {email}
Phone: {phone}
Service Interest: {service}

Message:
{message}
            """
        )
        mail.send(msg)

        return jsonify({
            'success': True,
            'message': 'Your message has been sent successfully!'
        })
        
    except Exception as e:
        app.logger.error(f"Error sending email: {e}")
        return jsonify({
            'success': False,
            'message': 'There was an error sending your message. Please try again later.'
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
