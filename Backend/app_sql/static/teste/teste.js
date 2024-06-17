async function createProduct() {
    const formData = new FormData();

    // Adicione os dados do formulário
    formData.append('title', 'Product Title');
    formData.append('description', 'Product Description');
    formData.append('value', 100.0);

    // Adicione os arquivos (imagens)
    const imageFiles = document.getElementById('imageFiles').files;
    for (let i = 0; i < imageFiles.length; i++) {
        formData.append('images', imageFiles[i]);
    }

    try {
        const response = await fetch('http://localhost:8000/products/', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }

        const data = await response.json();
        console.log('Product created successfully:', data);
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

// Supondo que você tenha um botão no HTML para enviar o formulário
document.getElementById('createProductButton').addEventListener('click', createProduct);
