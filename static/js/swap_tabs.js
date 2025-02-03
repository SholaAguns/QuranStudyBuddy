  function swapTabs(current_div_id) {
         var current_div = document.getElementById(current_div_id);

         document.querySelectorAll('.swap_tab').forEach(input => {
           input.classList.remove("active");
         });

         document.querySelectorAll('.swap_div').forEach(input => {
           input.style.display = 'none';
           input.classList.remove("active");
         });

         current_div.style.display = 'block';
}
