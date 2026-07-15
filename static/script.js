// Encode Form Submission
document.getElementById('encode-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const encodeButton = document.querySelector('#encode-form button');
    const encodeSpinner = document.getElementById('encode-spinner');
    encodeButton.disabled = true;
    encodeButton.textContent = 'Encoding...';
    encodeSpinner.style.display = 'inline-block'; // Show spinner
    try {
        const response = await fetch('/encode', {
            method: 'POST',
            body: formData,
        });
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'encoded_image.png';
        a.click();
    } catch (error) {
        console.error('Error encoding image:', error);
    } finally {
        encodeButton.disabled = false;
        encodeButton.textContent = 'Encode and Download';
        encodeSpinner.style.display = 'none'; // Hide spinner
    }
  });
  
  // Decode Form Submission
  document.getElementById('decode-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const decodeButton = document.querySelector('#decode-form button');
    const decodeSpinner = document.getElementById('decode-spinner');
    decodeButton.disabled = true;
    decodeButton.textContent = 'Decoding...';
    decodeSpinner.style.display = 'inline-block'; // Show spinner
    try {
        const response = await fetch('/decode', {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();
        document.getElementById('decoded-message').textContent = data.message;
    } catch (error) {
        console.error('Error decoding image:', error);
    } finally {
        decodeButton.disabled = false;
        decodeButton.textContent = 'Decode Message';
        decodeSpinner.style.display = 'none'; // Hide spinner
    }
  });