function showFields() {
    var type = document.getElementById("objectType").value;

    // Masquer tous les champs spécifiques
    document.getElementById("Screens").style.display = "none";
    document.getElementById("Lux").style.display = "none";

    // Afficher les champs spécifiques au type choisi
    if (type === "Ecran" || type === "Television") {
        document.getElementById("Screens").style.display = "block";
    }
    if (type === "Lumiere") {
        document.getElementById("Lux").style.display = "block";
    }
}