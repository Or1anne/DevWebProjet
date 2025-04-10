document.addEventListener('DOMContentLoaded', function () {
    const noNetworkCheckbox = document.getElementById('no-network');
    const otherCheckboxes = document.querySelectorAll('input[name="connectivity"]:not(#no-network)');

    noNetworkCheckbox.addEventListener('change', function () {
        if (this.checked) {
            otherCheckboxes.forEach(cb => cb.checked = false);
        }
    });

    otherCheckboxes.forEach(cb => {
        cb.addEventListener('change', function () {
            if (this.checked) {
                noNetworkCheckbox.checked = false;
            }
        });
    });
});