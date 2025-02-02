  function swapTabs(current_card_id) {
         var current_card = document.getElementById(current_card_id);
         var current_tab_id =current_card_id + '_tab';
         var current_tab = document.getElementById(current_tab_id);

         document.querySelectorAll('.answers_card_tab').forEach(input => {
           input.classList.remove("active");
         });

         document.querySelectorAll('.answers_card').forEach(input => {
           input.style.display = 'none';
           input.classList.remove("active");
         });

         current_card.style.display = 'block';
         current_tab.classList.add("active");
       }
