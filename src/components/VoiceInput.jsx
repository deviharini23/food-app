import React from 'react';
import axios from 'axios';

function VoiceInput({ userId, setResponse }) {
  const handleUpload = async (e) => {
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append("file", file);
    formData.append("user_id", userId);

    const res = await axios.post("http://localhost:8000/upload-audio/", formData);
    setResponse(res.data);
  };

  return (
    <div>
      <h3>Upload Voice Order</h3>
      <input type="file" accept="audio/*" onChange={handleUpload} />
    </div>
  );
}
 
export default VoiceInput;
