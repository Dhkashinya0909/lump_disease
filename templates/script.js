document.getElementById('submitBtn').addEventListener('click', function() {
    const input = document.getElementById('imageInput');
    const imagePreview = document.getElementById('imagePreview');

    // Clear previous preview and messages
    imagePreview.innerHTML = '';

    if (input.files && input.files[0]) {
        const file = input.files[0];
        
        // Check if the file is an image
        const validImageTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
        if (!validImageTypes.includes(file.type)) {
            const errorMessage = document.createElement('div');
            errorMessage.style.color = 'red';
            errorMessage.className = 'error-message';
            errorMessage.innerHTML = '❌ <span>Upload Failed: Please upload a valid image file (JPEG, PNG, GIF, WEBP).</span>';
            imagePreview.appendChild(errorMessage);
            return;
        }

        const reader = new FileReader();

        reader.onload = function(e) {
            const img = document.createElement('img');
            img.src = e.target.result;
            img.style.maxWidth = '300px'; // Set max width for the image
            img.style.maxHeight = '300px'; // Set max height for the image
            
            // Create a div to hold the image and filename
            const container = document.createElement('div');
            container.style.textAlign = 'center'; // Center the content

            // Create a paragraph for the filename
            const filename = document.createElement('p');
            filename.textContent = file.name; // Set the filename text
            
            // Create success message with a tick icon
            const successMessage = document.createElement('div');
            successMessage.className = 'success-message';
            successMessage.innerHTML = '✔️ <span>Upload Success</span>'; // Tick icon with text

            container.appendChild(img);
            container.appendChild(filename);
            container.appendChild(successMessage);
            imagePreview.appendChild(container);
        }

        reader.readAsDataURL(file);
    } else {
        const errorMessage = document.createElement('div');
        errorMessage.style.color = 'red';
        errorMessage.className = 'error-message';
        errorMessage.innerHTML = '❌ <span>Upload Failed: No image selected.</span>';
        imagePreview.appendChild(errorMessage);
    }
});
