document.addEventListener("DOMContentLoaded", function () {

    const selectButton = document.getElementById('select_button');
    const checkboxes = document.querySelectorAll('.checkbox');
    const deleteButton = document.getElementById('delete_selected_button');
    const form = document.getElementById('delete_selected_form');
    const selectAllButton = document.getElementById('select_all_button');

    // Function to update the delete button state
    function updateDeleteButton() {
        const anyChecked = Array.from(checkboxes).some(cb => cb.checked);
        deleteButton.disabled = !anyChecked;
    }

    selectButton.addEventListener('click', function (event) {
        event.preventDefault();
        
        document.querySelectorAll('.select_checkbox').forEach(function (checkbox) {
            if (checkbox.style.display === 'none' || checkbox.style.display === '') {
                selectButton.classList.add('highlight');
                checkbox.style.display = 'block';
                selectAllButton.style.display = 'block';
            } else {
                 selectButton.classList.remove('highlight');
                checkbox.style.display = 'none';
                selectAllButton.style.display = 'none';
            }
        });
    });

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
