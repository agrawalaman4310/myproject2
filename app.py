from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite3 database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prompts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the database model
class Prompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    curriculum = db.Column(db.String(100), nullable=False)
    education_level = db.Column(db.String(100), nullable=False)
    language = db.Column(db.String(100), nullable=False)
    prompt = db.Column(db.Text, nullable=False)

# Create the database and tables (run this only once to create the database)
with app.app_context():
    db.create_all()

# API to add new prompt to the database
@app.route('/add-prompt', methods=['POST'])
def add_prompt():
    data = request.get_json()  # Get the data from the request
    
    # Extract values from the JSON body
    subject = data.get('subject')
    curriculum = data.get('curriculum')
    education_level = data.get('education_level')
    language = data.get('language')
    prompt = data.get('prompt')

    # Validate if all required fields are provided
    if not subject or not curriculum or not education_level or not language or not prompt:
        return jsonify({'error': 'All fields are required'}), 400
    
    # Create a new Prompt record
    new_prompt = Prompt(
        subject=subject,
        curriculum=curriculum,
        education_level=education_level,
        language=language,
        prompt=prompt
    )
    
    # Add to session and commit to the database
    db.session.add(new_prompt)
    db.session.commit()

    # Return success response
    return jsonify({'message': 'Prompt added successfully'}), 201

# API to retrieve prompt based on filters
@app.route('/get-prompt', methods=['GET'])
def get_prompt():
    # Get filter parameters from query string
    subject = request.args.get('subject')
    curriculum = request.args.get('curriculum')
    education_level = request.args.get('education_level')
    language = request.args.get('language')
    
    # Query the database with filters
    query = Prompt.query
    if subject:
        query = query.filter_by(subject=subject)
    if curriculum:
        query = query.filter_by(curriculum=curriculum)
    if education_level:
        query = query.filter_by(education_level=education_level)
    if language:
        query = query.filter_by(language=language)
    
    result = query.first()  # Return the first matching record
    if result:
        return jsonify({'prompt': result.prompt}), 200
    else:
        return jsonify({'error': 'No matching prompt found'}), 404

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
