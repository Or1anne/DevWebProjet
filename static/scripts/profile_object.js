function openRequestMotif(type) {
    console.log("Bouton cliqué, ouverture du formulaire...");
    document.getElementById("requestMotifOverlay-" + type).style.display = "flex";
    document.getElementById("requestMotif-" + type).style.display = "block";
}

function closeRequestMotif(type) {
    document.getElementById("requestMotifOverlay-" + type).style.display = "none";
    document.getElementById("requestMotif-" + type).style.display = "none";
}