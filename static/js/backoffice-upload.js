(() => {
    const uploadBox = document.getElementById("quickUploadBox");
    const fileInput = document.getElementById("id_image");
    const preview = document.getElementById("uploadPreview");

    if (!uploadBox || !fileInput || !preview) {
        return;
    }

    const assignFile = (file) => {
        if (!file || !file.type.startsWith("image/")) {
            return;
        }
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;
        renderPreview(file);
    };

    const renderPreview = (file) => {
        preview.innerHTML = "";
        const info = document.createElement("p");
        info.textContent = `Imagem selecionada: ${file.name}`;
        preview.appendChild(info);

        const img = document.createElement("img");
        img.alt = "Pré-visualização da imagem";
        img.src = URL.createObjectURL(file);
        preview.appendChild(img);
    };

    uploadBox.addEventListener("click", () => fileInput.click());

    uploadBox.addEventListener("dragover", (event) => {
        event.preventDefault();
        uploadBox.classList.add("drag-over");
    });

    uploadBox.addEventListener("dragleave", () => {
        uploadBox.classList.remove("drag-over");
    });

    uploadBox.addEventListener("drop", (event) => {
        event.preventDefault();
        uploadBox.classList.remove("drag-over");
        const file = event.dataTransfer.files?.[0];
        assignFile(file);
    });

    fileInput.addEventListener("change", (event) => {
        const file = event.target.files?.[0];
        if (file) {
            renderPreview(file);
        }
    });

    document.addEventListener("paste", (event) => {
        const items = event.clipboardData?.items || [];
        for (const item of items) {
            if (item.type.startsWith("image/")) {
                assignFile(item.getAsFile());
                break;
            }
        }
    });
})();
