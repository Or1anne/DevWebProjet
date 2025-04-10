document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("searchInput2");
    const resultsDiv = document.getElementById("results2"); // <- C'est ça qui manquait

    // Fonction pour mettre à jour les résultats
    function updateResults() {
        const query = input.value;
        const url = `/request_admin?q=${encodeURIComponent(query)}`;

        fetch(url)
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, "text/html");
                const newResults = doc.querySelector("#results2");

                if (newResults && resultsDiv) {
                    resultsDiv.innerHTML = newResults.innerHTML;
                } else {
                    console.error("Pas de #results dans la réponse HTML !");
                }
            })
            .catch(error => {
                console.error("Erreur lors de la recherche :", error);
            });
    }

    if (input) {
        input.addEventListener("input", updateResults);
    }
});
