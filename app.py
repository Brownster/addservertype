from flask import Flask, request, render_template, send_from_directory, safe_join, abort
from csv_processor import update_config_item_name_with_correct_logic
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files or 'existing_yaml' not in request.files:
            return 'File part missing in the request'
        
        file = request.files['file']
        matrix_file = request.files['existing_yaml']
        
        if file.filename == '' or matrix_file.filename == '':
            return 'No selected file'
        
        if file and matrix_file:
            # Save the uploaded files temporarily
            config_path = os.path.join('/tmp', file.filename)
            matrix_path = os.path.join('/tmp', matrix_file.filename)
            file.save(config_path)
            matrix_file.save(matrix_path)
            
            # Process files
            output_path = os.path.join('/tmp', 'processed_config.csv')
            update_config_item_name_with_correct_logic(config_path, matrix_path, output_path)
            
            # Serve the processed file and then remove it
            try:
                return send_from_directory('/tmp', 'processed_config.csv', as_attachment=True)
            finally:
                os.remove(config_path)
                os.remove(matrix_path)
                os.remove(output_path)
    
    # If no file has been uploaded, show the upload form
    return render_template('upload.html')

@app.route('/downloads/<path:filename>', methods=['GET'])
def download(filename):
    if not os.path.isfile(safe_join('/tmp', filename)):
        abort(404)
    return send_from_directory('/tmp', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
