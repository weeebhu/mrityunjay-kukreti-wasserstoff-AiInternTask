import React, { useState } from 'react';
import axios from 'axios';
import './Uploader.css'

function FileUpload() {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [message, setMessage] = useState('');

  const handleFileChange = (event) => {
    setSelectedFiles(event.target.files);  // FileList object
  };

  const handleUpload = async () => {
    const formData = new FormData();
    // FileList supports iteration, so for...of works
    for (let file of selectedFiles) {
      formData.append("files", file);
    }

    try {
      const response = await axios.post("https://mrityunjay-kukreti-wasserstoff.onrender.com/upload/", formData);
      setMessage(`Uploaded ${response.data.filenames.length} files successfully.`);
    } catch (error) {
      console.error(error);
      setMessage("Upload failed.");
    }
  };

  return (
    <div className='file-upload-container'>
      <h2>Upload Multiple Files</h2>
      <input type="file" multiple onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      <p>{message}</p>
    </div>
  );
}

export default FileUpload;
