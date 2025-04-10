document.addEventListener("DOMContentLoaded", function () {
  const input = document.getElementById("searchInput");
  const useSelect = document.getElementById("UseSelect");
  const typeSelect = document.getElementById("typeSelect");
  const statusSelect = document.getElementById("StatusSelect");
  const resultsDiv = document.getElementById("results"); 

  // Fonction pour mettre à jour les résultats
  function updateResults() {
    const query = input.value;
    let serviceType = 'objets'; // Par défaut pour index.html
    if (useSelect) {
      serviceType = useSelect.value;   // Type de service (Utilisateurs, Objets, Chambres)
    }
    const objectType = typeSelect.value;   // Type d'objet
    const status = statusSelect.value;     // Statut de l'objet (ON/OFF)

    // Construire l'URL avec tous les filtres
    let url;
    if (window.location.pathname === '/search') {
      // Si on est sur la page de recherche
      url = `/search?q=${encodeURIComponent(query)}&service=${encodeURIComponent(serviceType)}&type=${encodeURIComponent(objectType)}&status=${encodeURIComponent(status)}`;
    } else {
      // Si on est sur la page d'index
      url = `/?q=${encodeURIComponent(query)}&service=${encodeURIComponent(serviceType)}&type=${encodeURIComponent(objectType)}&status=${encodeURIComponent(status)}`;
    }

    // Requête fetch avec les filtres
    fetch(url)
      .then(response => response.text())
      .then(html => {
        // Parser la réponse HTML et mettre à jour le contenu des résultats
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

  // Ajout des événements pour mettre à jour les résultats
  input.addEventListener("input", updateResults);
  if (useSelect) {
    useSelect.addEventListener("change", updateResults);
  }
  typeSelect.addEventListener("change", updateResults);
  statusSelect.addEventListener("change", updateResults);

  // Réinitialisation des champs
  document.getElementById("resetBtn").addEventListener("click", function() {
    input.value = "";
    useSelect.value = "";
    typeSelect.value = "";
    statusSelect.value = "";
    
    // Actualiser les résultats après réinitialisation
    updateResults(); 
  });
});