from PIL import Image
import numpy as np
import cv2
import potrace
import re
import io
    
def preProcess(img):
  # Resize the image to reduce processing time. 
  img = img.resize((200, 200)) 
  width, height = img.size

  # Quantitize image to reduce the number of colors 
  img = img.quantize(colors=6, kmeans=4).convert('RGB')
  return img

def calculateLuminance(img):
# Extract dominant colors
  n_dom_colors = 6
  dom_colors = sorted(img.getcolors(2 ** 24), reverse=True)[:n_dom_colors]
  
  # Calculate luminance/brightness of dominant colors
  luminance = []
  for val in dom_colors:
    #v = (val[1][0] + val[1][1] + val[1][2])
    #v = round(v/3.5)
    #luminance.append((-(v)+255)*1)
    v = ((0.2126*val[1][0]) + (0.7152*val[1][1]) + (0.0722*val[1][2]))
    luminance.append((-(v)+255))
    luminance = sorted(luminance)
  return [luminance, dom_colors]
   
def convertToBitmap(img):
  imgArray = np.array(img)
  
  # Convert image to bitmap
  # Split the three channels
  r,g,b = np.split(imgArray,3,axis=2)
  r=r.reshape(-1)
  g=r.reshape(-1)
  b=r.reshape(-1)

  # Standard RGB to grayscale 
  bitmap = list(map(lambda x: int(0.299*x[0]+0.587*x[1]+0.114*x[2]), zip(r,g,b)))
  bitmap = np.array(bitmap).reshape([imgArray.shape[0], imgArray.shape[1]])
  return bitmap


def extract(bitmap, threshold, color):

  # Use threshold value to determine area to trace
  bitmap = np.dot((bitmap > threshold).astype(float), 255)

  # Convert image's white pixels to 0 and black pixels to 1
  # since potrace uses values 0 and 1 for tracing
  data = bitmap
  data[data == 0] = 1
  data[data == 255] = 0
  
  # Trace bitmap
  bmp = potrace.Bitmap(data)
  bmp.trace()
  
  # convert bitmap to xml
  xml = bmp.to_xml()
  
  # Extract paths from xml
  pattern = r'(?<=<path d=").*?(?=")'
  pathList = re.findall(pattern, xml)
  
  # Group paths and fill with color
  body = f'<g transform="scale(0.05, 0.05)" fill="{color}" stroke="none">'
  for path in pathList:
    body += f'<path d="{path}"/>'
  body += "</g>"
  
  return body

def fullSVG(img):
  #paths = ""
  #for i, val in enumerate(reversed(dom_colors)):
    #s = luminance[i]
    #paths += extract(s, f'rgb{val[1]}')
    
  img = Image.open(io.BytesIO(img))
  preProcessedImg = preProcess(img)
  bitmap = convertToBitmap(preProcessedImg)
  colorDetails = calculateLuminance(preProcessedImg)
  luminance = colorDetails[0]
  dom_colors = colorDetails[1]
  
  # Use color luminance and color for svg extraction
  zero = extract(bitmap, luminance[5], f'rgb{dom_colors[5][1]}')
  one = extract(bitmap, luminance[4], f'rgb{dom_colors[4][1]}')
  two = extract(bitmap, luminance[3], f'rgb{dom_colors[3][1]}')
  three = extract(bitmap, luminance[2], f'rgb{dom_colors[2][1]}')
  four = extract(bitmap, luminance[1], f'rgb{dom_colors[1][1]}')
  five = extract(bitmap, luminance[0], f'rgb{dom_colors[0][1]}')
  paths = zero + one + two + three + four + five
  
  
  header = f'<svg version="1.0" xmlns="http://www.w3.org/2000/svg" width="300" height="300" viewBox="0 0 100 100" >\n'
  footer = f'</svg>'
  combinedSVG = header + paths + footer
  return combinedSVG
  

  
  
  

