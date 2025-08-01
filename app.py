from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
import traceback
import os

app = Flask(__name__)
application = app  # for passenger_wsgi.py on cPanel

# ✅ Brevo SMTP Configuration
app.config['MAIL_SERVER'] = 'smtp-relay.brevo.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = '8f853d001@smtp-brevo.com'  # Replace with your Brevo SMTP login
app.config['MAIL_PASSWORD'] = 'xsmtpsib-a38be493562102a86b2c5ef74e2f03ce30c2e6f20385155e27b398f9715e7ae5-d2CI8ATvtKkE0UbV'
app.config['MAIL_DEFAULT_SENDER'] = 'info@hoofstad.co.ke'  # Must be verified in Brevo

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        data = request.form
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
        return jsonify({'success': True, 'message': 'Your message has been sent successfully!'})

    except Exception as e:
        # ✅ Log error to file in cPanel
        log_path = os.path.expanduser("~/flask_mail_error.log")
        with open(log_path, "a") as f:
            f.write("---- Error on submit-form ----\n")
            f.write(traceback.format_exc())
            f.write("\n")

        return jsonify({
            'success': False,
            'message': 'An error occurred. Please try again later.',
            'error': str(e),
            'trace': traceback.format_exc()
        }), 500

# ✅ Optional test route to check SMTP directly
@app.route('/test-smtp')
def test_smtp():
    try:
        msg = Message(
            subject="SMTP Test Email",
            recipients=["caleb.muteti@hoofstad.co.ke"],
            body="This is a test email from your Flask app on cPanel using Brevo SMTP."
        )
        mail.send(msg)
        return "✅ SMTP Test Email Sent Successfully!"
    except Exception as e:
        log_path = os.path.expanduser("~/flask_mail_error.log")
        with open(log_path, "a") as f:
            f.write("---- Error on test-smtp ----\n")
            f.write(traceback.format_exc())
            f.write("\n")
        return f"❌ Failed to send SMTP test email: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
