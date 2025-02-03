document.addEventListener("DOMContentLoaded", function () {
    const checkboxes = document.querySelectorAll('.checkbox');
    const deleteButton = document.getElementById('delete_selected_button');
    const form = document.getElementById('delete_selected_form');

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            const anyChecked = Array.from(checkboxes).some(cb => cb.checked);
            deleteButton.disabled = !anyChecked;
        });
    });
    deleteButton.addEventListener('click', function (event) {
        event.preventDefault();
        const confirmDeletion = confirm("Are you sure you want to delete the selected items? This action cannot be undone.");
        if (confirmDeletion) {
            form.submit();
        }
    });
});
