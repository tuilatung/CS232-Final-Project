const dropArea = document.querySelector('.drag-area');
const dragText = document.querySelector('.header');
const showRes =  document.querySelector(".range");
const showImg =  document.querySelector("#showIMG");
const uploadImg =  document.querySelector("#uploadIMG");
const imgArea =  document.querySelector(".img__box");
const slideValue = document.querySelector("#number");
const inputSlider = document.querySelector("#slider");


let button = document.querySelector('.button');
let input = dropArea.querySelector('input');
let file;
let imgForm = document.querySelector(".get_img");
var w;
var h;
var base64_image;

button.onclick = () => {
  input.click();
};

inputSlider.addEventListener('change', function(){
  // window.alert('changed');
  // console.log('On Sliderbar changes...');
  // const URL = '/getslider'
  const URL = '/svd'
  const xhr = new XMLHttpRequest();
  sender = inputSlider.value
  xhr.open('POST', URL, true);
  xhr.send(sender);
  xhr.onreadystatechange = function(e) {
    e.preventDefault();
    if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
      const update =  new Date();
      const data = JSON.parse(xhr.responseText).data;
      document.querySelector('.img__box').innerHTML = `<img src="${data[0]}?v=${update.getTime()}" />`; // To update avoid using image from cache
      document.querySelector('#img__size').innerHTML = `${data[1]} x ${data[2]}`;
      document.querySelector('#num__pixel').innerHTML = `${data[1]*data[2]}`;
      document.querySelector('#compressed__size').innerHTML = `${data[3]}`;
      document.querySelector('#compression__ratio').innerHTML = `${(data[1]*data[2])/data[3]}`;
    }
  }
})

function sendIMG(file){
  const URL = '/upload';
  const xhr = new XMLHttpRequest();
  const formData = new FormData();
  formData.append('file', file);
  xhr.open('POST', URL);
  xhr.send(formData);
}

// when browse
input.addEventListener('change', function () {
  file = this.files[0];
  dropArea.classList.add('active');
  displayFile();
  sendIMG(file);
});

// when file is inside drag area
dropArea.addEventListener('dragover', (event) => {
  event.preventDefault();
  dropArea.classList.add('active');
  dragText.textContent = 'Release to Upload';
  // console.log('File is inside the drag area');
});

// when file leave the drag area
dropArea.addEventListener('dragleave', () => {
  dropArea.classList.remove('active');
  // console.log('File left the drag area');
  dragText.textContent = 'Drag & Drop';
});

// when file is dropped
dropArea.addEventListener('drop', (event) => {
  event.preventDefault();
  file = event.dataTransfer.files[0]; // grab single file even of user selects multiple files
  displayFile();
  uploadImg.style.display = "none"
  showRes.style.display = "block";
  showImg.style.display = "block";
  sendIMG(file);
  // containerRes.style.height = h + 500;
});

imgForm.addEventListener("change", function(e) {
  e.preventDefault();
  displayFile();
  uploadImg.style.display = "none"
  showRes.style.display = "block";
  showImg.style.display = "block";

  // const formData = new FormData();
  // if (file != null){
  //   formData.append('file', file);
  // }
  // const URL = '/uploader';
  // xhr.open('POST', URL, true);
  // xhr.send(formData);
});

function displayFile() {
  let fileType = file.type;
  // console.log(fileType);

  let validExtensions = ['image/jpeg', 'image/jpg', 'image/png'];

  if (validExtensions.includes(fileType)) {
    // console.log('This is an image file');
    let fileReader = new FileReader();

    fileReader.onload = () => {
      let fileURL = fileReader.result;
      var image = new Image();
      image.src = fileReader.result;
      image.onload = function(){
        w = this.width;
        h = this.height;
      };
      base64_image = image
      // console.log(image)
      
      imgTag = `<img src="${fileURL}" id="user__img">`;
      imgArea.innerHTML = imgTag;
    };
    // containerRes.style.he
    fileReader.readAsDataURL(file);
  } 
  else {
     
    Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: 'This file is not supported!',
    })
    dropArea.classList.remove('active');
    file = null;
  }
}

inputSlider.oninput = (()=>{
  let value = inputSlider.value;
  slideValue.textContent = value;
  slideValue.style.left = (value/3) + "%";
  slideValue.classList.add("show");
});

inputSlider.onblur = (()=>{
  slideValue.classList.remove("show");
});

// const xhr = new XMLHttpRequest();
// xhr.onreadystatechange = function(e) {
//   e.preventDefault();
//   window.alert(2);
//   console.log(3);
//   if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
//     const update =  new Date();
//     const data = JSON.parse(xhr.responseText).data;
//     // document.querySelector('.img__box').textContent = '';
//     document.querySelector('.img__box').textContent = `<img src="${data}?v=${update.getTime()}" />`; // To update avoid using image from cache
//   }
// }