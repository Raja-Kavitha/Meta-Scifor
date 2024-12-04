from flask import Flask, render_template, request, send_file
from PIL import Image
import os
import docx2pdf
import zipfile
from django.contrib import messages


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/resize', methods=['POST'])
def resize_images():
    if 'images' not in request.files:
        return "No files uploaded", 400
    
    files = request.files.getlist('images')
    width = int(request.form['width'])
    height = int(request.form['height'])
    output_files=[]

    # Save and process the image
    for file in files:
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(input_path)
        output_path = os.path.join(UPLOAD_FOLDER, f"resized_{file.filename}")

    with Image.open(input_path) as img:
        resized_img = img.resize((width, height))
        resized_img.save(output_path)
        output_files.append(output_path)

    zip_path = os.path.join(UPLOAD_FOLDER,"resized_images.zip")
    with zipfile.ZipFile(zip_path,'w')as zipf:
        for file in output_files:
            zipf.write(file,os.path.basename(file))

    return send_file(zip_path, as_attachment=True) 

@app.route('/convert_format',methods=['POST'])
def convert_files():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['file']
    format = request.form['format'].lower()

    file_ext = os.path.splitext(file.filename)[1].lower()
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)
    output_filename = f"converted_{os.path.splitext(file.filename)[0]}.{format}"
    output_path = os.path.join(UPLOAD_FOLDER, output_filename)

    # Validate file and format
    if file_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif'] and format in ['jpg', 'jpeg', 'png', 'bmp', 'gif']:
        # Convert image format
        with Image.open(input_path) as img:
            img.save(output_path, format=format.upper())
        return send_file(output_path, as_attachment=True)
    elif file.filename.lower().endswith('.docx') and format == 'pdf':
        docx2pdf.convert(input_path,output_path)
    else:
        return "Unsupported file type or conversion type", 400
    
    return send_file(output_path, as_attachment=True)


@app.route('/convert_pdf', methods=['POST'])
def convert_files_to_pdf():
    # Check if the request contains files
    if 'files' not in request.files or not request.files.getlist('files'):
        return 'No files uploaded', 400

    files = request.files.getlist('files')  # Get multiple files
    images = []

    for file in files:
        if file.filename == '':
            continue  # Skip empty filenames

        if file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            input_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(input_path)
            # Open and convert each image to RGB for compatibility with PDF
            with Image.open(input_path) as img:
                images.append(img.convert('RGB'))
        else:
            return f"Unsupported file type: {file.filename}", 400

    # Output PDF path
    output_path = os.path.join(UPLOAD_FOLDER, 'output.pdf')

    if images:
        # Save all images as a single PDF
        images[0].save(output_path, save_all=True, append_images=images[1:])
        return send_file(output_path, as_attachment=True)
    else:
        return "No valid images to convert", 400
   
 
if __name__ == '__main__':
    app.run(debug=True)
