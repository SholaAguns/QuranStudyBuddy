function correct_answer(flashcard_id) {
    $.ajax({
        type: "POST",
        url: "/flashcards/flashcardset/correct_answer/" + flashcard_id + "/",
        headers: {
            "X-CSRFToken": getCSRFToken()
        },
        success: function (payload) {
            console.log("SUCCESS", payload);
        },
        error: function (payload) {
            console.error("ERROR: ", payload);
        },
        complete: function () {
            location.reload();
        }
    });
}

function getCSRFToken() {
    let cookieValue = null;
    let cookies = document.cookie.split("; ");
    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].split("=");
        if (cookie[0] === "csrftoken") {
            cookieValue = cookie[1];
            break;
        }
    }
    return cookieValue;
}
