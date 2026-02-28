const video = document.getElementById('video');

navigator.mediaDevices.getUserMedia({ video: true })
.then(stream => {
    video.srcObject = stream;
});

function capture() {
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0);

    canvas.toBlob(blob => {
        let formData = new FormData();
        formData.append('image', blob, 'scan.jpg');

        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById('result').innerHTML =
                "<h3>Detected:</h3>" + data.items.join("<br>");
        });
    });
}