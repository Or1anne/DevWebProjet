document.addEventListener("DOMContentLoaded", function () {
  const input = document.getElementById("searchInput");
  const useSelect = document.getElementById("UseSelect");
  const typeSelect = document.getElementById("typeSelect");
  const statusSelect = document.getElementById("StatusSelect");
  const resultsDiv = document.getElementById("results");

  // Fonction pour mettre à jour les résultats
  function updateResults() {
    const query = input.value;
    const serviceType = useSelect.value;   // Type de service (Utilisateurs, Objets, Chambres)
    const objectType = typeSelect.value;   // Type d'objet
    const status = statusSelect.value;     // Statut de l'objet (ON/OFF)

    // Construire l'URL avec tous les filtres
    let url = `/result?q=${encodeURIComponent(query)}&service=${encodeURIComponent(serviceType)}&type=${encodeURIComponent(objectType)}&status=${encodeURIComponent(status)}`;

    // Requête fetch avec les filtres
    fetch(url)
      .then(response => response.text())
      .then(html => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, "text/html");
        const newResults = doc.querySelector("#results");

        if (newResults) {
          resultsDiv.innerHTML = newResults.innerHTML;
        } else {
          console.error("Pas de #results dans la réponse HTML !");
        }
      })
      .catch(error => {
        console.error("Erreur lors de la recherche :", error);
      });
  }

  // Écouteurs pour chaque champ de filtrage
  input.addEventListener("input", updateResults);
  useSelect.addEventListener("change", updateResults);
  typeSelect.addEventListener("change", updateResults);
  statusSelect.addEventListener("change", updateResults);

  // Fonction de réinitialisation
  document.getElementById("resetBtn").addEventListener("click", function() {
    // Réinitialisation des champs
    input.value = "";
    useSelect.value = "";
    typeSelect.value = "";
    statusSelect.value = "";
    
    // Mise à jour des résultats après réinitialisation
    updateResults(); 
  });
});

