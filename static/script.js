let imageLoader = document.getElementById("imageUpload");
imageLoader.addEventListener('change', loadImage, false);


// Draw image on canvas 
function loadImage(e) {
 if (!(document.getElementById("canvas"))){
  let c = document.createElement("canvas");
  c.setAttribute('id', "canvas");
  const canvasContainer = document.getElementById("canvas-box");
  canvasContainer.appendChild(c);
  }
  let canvas = document.getElementById('canvas');
  let ctx = canvas.getContext('2d');

  let reader = new FileReader();
  reader.onload = function(event) {
    let img = new Image();
    img.onload = function() {
      canvas.width = img.width;
      canvas.height = img.height;
      ctx.drawImage(img, 0, 0);
    }
    img.src = event.target.result;
    
    // Create convert button after image is loaded to canvas, if it doesn't already exist 
    if (!(document.getElementById("generate"))){
         const btnContainer = document.querySelector(".buttons");
    let generateBtn = document.createElement("button");
     const node = document.createTextNode("Convert to SVG");
     generateBtn.appendChild(node);
     generateBtn.setAttribute('id', "generate");
     btnContainer.appendChild(generateBtn);
     
     document.getElementById("generate").addEventListener("click", function() {
  generateSVG();
})
    }
    document.querySelector('.upload-details').remove();

  }

  reader.readAsDataURL(e.target.files[0]);
}


function generateSVG() {
  let imageLoader = document.getElementById("imageUpload");
  const files = imageLoader.files;
  const myImage = files[0]
  const imageType = /image.(jpg|jpeg)/

  if (!myImage.type.match(imageType)) {
    alert('Sorry, only JPG/JPEG images are allowed')
    return
  }

  if (myImage.size > (200 * 1024)) {
    alert('Sorry, the max allowed size for images is 200KB')
    return
  }

  const formData = new FormData()
  formData.append('file', myImage)
  console.log(formData)

  async function postChar(url = '', data = {}) {
    const response = await fetch(url, {
      method: 'POST',
      mode: 'cors',
      cache: 'no-cache',
      credentials: 'same-origin',
      redirect: 'follow',
      referrerPolicy: 'no-referrer',
      body: formData,

    });
    let svg = response.json();
    return svg
  }

  postChar('/svg')
    .then(data => {
      let svgData = data.svg
      
      // Show SVG image on page
      let svgContainer = document.getElementById("svg-box");
      svgContainer.innerHTML = svgData;
      
    // Create svg download button after svg is generated, if it doesn't already exist 
    if (!(document.getElementById("download"))){
    const btnContainer = document.querySelector(".buttons");
    let downloadBtn = document.createElement("button");
     const node = document.createTextNode("Save SVG");
     downloadBtn.appendChild(node);
     downloadBtn.setAttribute('id', "download");
     btnContainer.appendChild(downloadBtn);
     document.getElementById("download").addEventListener("click", function() {
  download();
}) 
}
    });
}

function download() {
  let svgContainer = document.getElementById("svg-box");
  let svgToDownload = {
    svgCode: svgContainer.innerHTML,
  }
  async function postPNG(url = '', data = {}) {
    const response = await fetch(url, {
      method: 'POST',
      mode: 'cors',
      cache: 'no-cache',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json'
      },
      redirect: 'follow',
      referrerPolicy: 'no-referrer',
      body: JSON.stringify(data)
    });
    let pngData = response;
    return pngData
  }

  postPNG('/download', svgToDownload)
    .then(response => response.blob())
    .then(blob => {
      let url = window.URL.createObjectURL(blob);
      let a = document.getElementById("download-text");
      a.href = url;
      a.download = `image.svg`;
      a.click()
    });
}

