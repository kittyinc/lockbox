const fileInput = document.getElementById('file-upload');
fileInput.addEventListener('change', handleFileUpload);
const csrftoken = getCookie('csrftoken');
let file_id;

function handleFileUpload(event) {
  const file = event.target.files[0];
  let start = 0;
  let end = 0;
  let chunk;

  while (start < file.size) {
    chunk = file.slice(start, start + chunk_size);
    end = chunk.size - start;
    console.log("LID: ", file_id);
    file_id = uploadChunk(chunk, start, end, file.size, file_id);
    start += chunk_size;
  }
}

function uploadChunk(chunk, start, end, total, file_id=null) {
    const formData = new FormData();
    const range_header = `bytes ${start}-${end}/${total}`;
    formData.append('file', chunk);


    if (file_id) {
        formData.append("lid", file_id);
    }

    let request = new Request(".", {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-range': range_header
        }
    })
    return _uploadChunk(request);
}   

async function _uploadChunk(request) {
    const _response = await fetch(request)
    .then(async (response)=>response.json())
    .then((data) =>{
        return data.lid;
    })
    return _response;
}