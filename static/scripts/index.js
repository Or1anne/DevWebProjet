document.addEventListener("DOMContentLoaded", function () {
    // Applique la logique de lecture des textes tronqués
    document.querySelectorAll(".news-item p, .info-item p").forEach(p => {
        let fullText = p.innerText;
        if (fullText.length > 200) {  // Limite de caractères avant tronquer
            let truncated = fullText.substring(0, 200) + "..."; // Texte tronqué
            // Mise à jour du contenu HTML avec texte tronqué
            p.innerHTML = `<div class="text-container">
                                <span class="truncated-text">${truncated}</span>
                                <span class="full-text">${fullText}</span>
                            </div>
                            <span class="read-more">Lire plus</span>`;

            // Appliquer un style pour assurer le retour à la ligne
            p.querySelector(".truncated-text").style.whiteSpace = "normal";
            p.querySelector(".full-text").style.whiteSpace = "normal";

            p.querySelector(".read-more").addEventListener("click", function () {
                let textContainer = p.querySelector(".text-container");
                let truncatedText = textContainer.querySelector(".truncated-text");
                let fullText = textContainer.querySelector(".full-text");

                if (fullText.style.display === "none" || fullText.style.display === "") {
                    fullText.style.display = "inline"; // Afficher le texte complet
                    truncatedText.style.display = "none"; // Cacher le texte tronqué
                    this.textContent = "Lire moins"; // Changer le texte du bouton
                } else {
                    fullText.style.display = "none"; // Cacher le texte complet
                    truncatedText.style.display = "inline"; // Afficher le texte tronqué
                    this.textContent = "Lire plus"; // Réinitialiser le texte du bouton
                }
            });
        }
    });
});