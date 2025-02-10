document.addEventListener("DOMContentLoaded", function () {

    const checkboxes = document.querySelectorAll('.checkbox');
    const deleteButton = document.getElementById('delete_selected_button');
    const form = document.getElementById('delete_selected_form');
    const selectAllButton = document.getElementById('select_all_button');

    // Function to update the delete button state
    function updateDeleteButton() {
        const anyChecked = Array.from(checkboxes).some(cb => cb.checked);
        deleteButton.disabled = !anyChecked;
    }

    // Add event listeners to checkboxes
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateDeleteButton);
    });

    // Add event listener to the delete button
    deleteButton.addEventListener('click', function (event) {
        event.preventDefault();
        const confirmDeletion = confirm("Are you sure you want to delete the selected items? This action cannot be undone.");
        if (confirmDeletion) {
            form.submit();
        }
    });

    // Add event listener to the "Select All" button
    if (selectAllButton) {
        selectAllButton.addEventListener('click', function (event) {
            event.preventDefault();
            const allChecked = Array.from(checkboxes).every(cb => cb.checked);
            checkboxes.forEach(checkbox => {
                checkbox.checked = !allChecked;
            });
            updateDeleteButton();
        });
    }
});
