# jpg2svg

An attempt at converting colored JPG images to colored SVG. It automatically traces the image in layers and automatically applies dominant colors selected from the image to each layers. 

<h3 style="text-align:center"> Some results (JPG and converted SVG side by side)</h3>
Images with higher contrast, and with white backgrounds produce better results:
            <div class="images">
            <div class="image" style="display:flex">
              <img src="/static/images/examples/facebook.jpg" alt="" width="200px" />
              <img src="/static/images/examples/facebook.svg" alt="" width="200px"/>
             </div>
            <div class="image" style="display:flex">
              <img src="/static/images/examples/amongus.jpg" alt="" width="200px"/>
              <img src="/static/images/examples/amongus.svg" alt="" width="200px"/>
             </div>
             <div class="image" style="display:flex">
              <img src="/static/images/examples/chip.jpg" alt="" width="200px"/>
              <img src="/static/images/examples/chip.svg" alt="" width="200px"/>
             </div>
             <div class="image" style="display:flex">
              <img src="/static/images/examples/drawing.jpg" alt="" width="200px"/>
              <img src="/static/images/examples/drawing.svg" alt="" width="200px"/>
             </div>
             <div class="image" style="display:flex">
              <img src="/static/images/examples/house.jpg" alt="" width="200px"/>
              <img src="/static/images/examples/house.svg" alt="" width="200px"/>
             </div>
  </div>

### Technical details

The actual image conversion code is held at [svg.py](svg.py). Below is a summary of the steps it follows:
- Resizes the image to reduce processing time
- Quantitizes the image to reduce the number of colors to work with
- Calculates the luminance/brightness of dominant colors
- Converts the JPG image to bitmap (since Potrace, used for tracing, only supports the Bitmap format)
- Uses luminance values as thresholds for tracing the image into multiple layers
- Converts the tracing to XML
- Applies dominant colors to each of the layers
- Groups the various layers into one SVG element
