function correct_answer(flashcard_id) {
    $.ajax({
      type: 'POST',
      url: "/flashcards/flashcardset/correct_answer/" + flashcard_id +"/",
      data: {
        'csrfmiddlewaretoken': "{{ csrf_token }}"
      },
      dataType: "json",
      success: function(payload) {
      //console.log("SUCCESS", data)
      },
      error: function(payload) {
      console.error("ERROR: ", data)
      },
      complete: function(payload){
        location.reload();
      }
    });
}
