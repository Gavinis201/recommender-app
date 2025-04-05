from flask import Flask, request, jsonify, render_template
import pandas as pd
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Load the CSV files for the models
collab_df = pd.read_csv('collaborative_filtering.csv')
content_df = pd.read_csv('content_recommendations.csv')

# Strip any extra spaces in the column names
collab_df.columns = collab_df.columns.str.strip()
content_df.columns = content_df.columns.str.strip()

@app.route('/')
def index():
    return render_template('index.html')  # Serve the form page

@app.route('/get_recommendations', methods=['GET'])
def get_recommendations():
    item_id = request.args.get('itemID')  # Get the itemID from the URL
    
    try:
        # Ensure item_id is provided
        if not item_id:
            return jsonify({'error': 'itemID is required'}), 400
        
        item_id = int(item_id)  # Convert to integer if it's valid

        # Collaborative filtering recommendations (top 5)
        collab_recs = collab_df[collab_df['contentId'] == item_id]['recommendedContentId'].head(5).tolist()

        # Content-based filtering recommendations (top 5)
        content_recs = content_df[content_df['contentId'] == item_id]['recommendedContentId'].head(5).tolist()

        return render_template('index.html', 
                               collab_recs=collab_recs, 
                               content_recs=content_recs)  # Render the template with recommendations

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
