document.addEventListener("DOMContentLoaded", function () {
    const userList = document.querySelector(".gestion-container ul");
    const users = userList.querySelectorAll("li");
    
    if (users.length > 3) {
        // Cacher les utilisateurs au-delà des deux premiers
        for (let i = 3; i < users.length; i++) {
            users[i].style.display = "none";
        }

        // Créer le bouton "Afficher plus"
        const toggleButton = document.createElement("button");
        toggleButton.textContent = "Afficher plus";
        toggleButton.classList.add("search-button");
        userList.parentNode.appendChild(toggleButton);
        
        let isExpanded = false;

        toggleButton.addEventListener("click", function () {
            if (isExpanded) {
                for (let i = 3; i < users.length; i++) {
                    users[i].style.display = "none";
                }
                toggleButton.textContent = "Afficher plus";
            } else {
                for (let i = 3; i < users.length; i++) {
                    users[i].style.display = "list-item";
                }
                toggleButton.textContent = "Afficher moins";
            }
            isExpanded = !isExpanded;
        });
    }
});