from flask import Flask, request, redirect, url_for, render_template
import os
import esptool

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'bootloader' not in request.files or 'partitions' not in request.files or 'firmware' not in request.files:
        return 'Missing one or more binary files'
    
    bootloader = request.files['bootloader']
    partitions = request.files['partitions']
    firmware = request.files['firmware']
    
    if bootloader.filename == '' or partitions.filename == '' or firmware.filename == '':
        return 'No selected files'
    
    bootloader_path = os.path.join(app.config['UPLOAD_FOLDER'], bootloader.filename)
    partitions_path = os.path.join(app.config['UPLOAD_FOLDER'], partitions.filename)
    firmware_path = os.path.join(app.config['UPLOAD_FOLDER'], firmware.filename)
    
    bootloader.save(bootloader_path)
    partitions.save(partitions_path)
    firmware.save(firmware_path)
    
    port = request.form['port']
    baudrate = request.form['baudrate']
    
    flash_firmware(port, baudrate, bootloader_path, partitions_path, firmware_path)
    
    return 'Files successfully uploaded and flashed'

def flash_firmware(port, baudrate, bootloader_path, partitions_path, firmware_path):
    esptool_args = [
        '--chip', 'esp32',
        '--port', port,
        '--baud', baudrate,
        'write_flash',
        '0x1000', bootloader_path,
        '0x8000', partitions_path,
        '0x10000', firmware_path
    ]
    esptool.main(esptool_args)

if __name__ == "__main__":
    app.run(debug=True)
