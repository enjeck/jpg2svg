from flask import Flask, request, json, send_file
from flask import send_from_directory
from svg import fullSVG
from cairosvg import svg2png
from PIL import Image 


app = Flask(__name__,static_url_path='')

@app.route('/')
def home_page():
   return send_from_directory("static/", 'index.html')  

@app.route('/svg', methods=['POST'])
def getCharacter():
  #img = request.files['file']
  img = request.files['file'].read()
  #img.save('upload.jpg')
  figure = {
  'svg': fullSVG(img)
  }
  return figure

@app.route('/download', methods=['POST'])  
def downloadSVG():
  xml = request.json['svgCode']
  with open("image.svg", "w") as f:
    f.write(xml)  
  return send_file('image.svg', mimetype='image/svg+xml')

# run app  
# app.run(debug=True)
