const revealElements = document.querySelectorAll(".reveal");
const backToTop = document.getElementById("backToTop");
const lightbox = document.getElementById("imageLightbox");
const lightboxImage = document.getElementById("lightboxImage");
const lightboxClose = document.getElementById("lightboxClose");
const productImageButtons = document.querySelectorAll(".product-image-btn");
const emailCopyButtons = document.querySelectorAll(".email-copy-btn");

const observer = new IntersectionObserver(
    (entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
            }
        });
    },
    { threshold: 0.12 }
);

revealElements.forEach((element) => observer.observe(element));

window.addEventListener("scroll", () => {
    if (!backToTop) {
        return;
    }
    if (window.scrollY > 450) {
        backToTop.classList.add("show");
    } else {
        backToTop.classList.remove("show");
    }
});

if (backToTop) {
    backToTop.addEventListener("click", () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });
}

if (lightbox && lightboxImage && lightboxClose) {
    const closeLightbox = () => {
        lightbox.classList.remove("show");
        lightbox.setAttribute("aria-hidden", "true");
        lightboxImage.src = "";
    };

    productImageButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const img = button.querySelector("img");
            if (!img) {
                return;
            }
            lightboxImage.src = img.src;
            lightboxImage.alt = img.alt;
            lightbox.classList.add("show");
            lightbox.setAttribute("aria-hidden", "false");
        });
    });

    lightboxClose.addEventListener("click", closeLightbox);

    lightbox.addEventListener("click", (event) => {
        if (event.target === lightbox) {
            closeLightbox();
        }
    });

    window.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            closeLightbox();
        }
    });
}

if (emailCopyButtons.length > 0) {
    const fallbackCopy = (text) => {
        const tempInput = document.createElement("input");
        tempInput.value = text;
        document.body.appendChild(tempInput);
        tempInput.select();
        document.execCommand("copy");
        document.body.removeChild(tempInput);
    };

    emailCopyButtons.forEach((button) => {
        button.addEventListener("click", async (event) => {
            event.preventDefault();
            const email = button.dataset.email || "naiprints3d@gmail.com";
            try {
                await navigator.clipboard.writeText(email);
            } catch (error) {
                fallbackCopy(email);
            }
            const previousLabel = button.innerHTML;
            button.innerHTML = '<i class="fa-regular fa-circle-check"></i> Email copiado!';
            setTimeout(() => {
                button.innerHTML = previousLabel;
            }, 1400);
        });
    });
}
