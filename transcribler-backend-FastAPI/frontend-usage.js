async function downloadAudio(url) {
    const response = await fetch('http://127.0.0.1:8000/download-audio/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: url })
    });

    if (!response.ok) {
        throw new Error('Network response was not ok');
    }

    const blob = await response.blob();
    const urlObject = URL.createObjectURL(blob);

    // Create a link element to download the file
    const link = document.createElement('a');
    link.href = urlObject;
    link.download = 'audio.mp3'; // Specify the file name
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Example usage
const youtubeUrl = 'https://www.youtube.com/watch?v=example'; // Replace with actual YouTube URL
downloadAudio(youtubeUrl).catch(error => console.error('Error downloading audio:', error));