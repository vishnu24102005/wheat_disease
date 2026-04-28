const fileInput = document.getElementById("fileInput");
const previewImage = document.getElementById("previewImage");
const resultText = document.getElementById("result");

// Preview image
fileInput.addEventListener("change", function () {
    const file = fileInput.files[0];
    if (file) {
        previewImage.src = URL.createObjectURL(file);
        previewImage.style.display = "block";
    }
});

// Send to Flask backend
function uploadImage() {
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select an image first");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    resultText.innerHTML = "⏳ Predicting...";

    fetch("/predict", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        resultText.innerHTML = "🌿 Prediction: " + data.prediction;
    })
    .catch(error => {
        resultText.innerHTML = "❌ Error occurred";
        console.error(error);
    });
}