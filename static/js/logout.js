document.addEventListener("DOMContentLoaded", function () {

    const logoutbtn = document.getElementById("logoutbtn");
    const logoutUrl = logoutbtn.getAttribute("data-logout-url");

    logoutbtn.addEventListener("click", function () {

      if (!confirm("Are you sure you want to log out?")) return;

      fetch(logoutUrl, {
          method: "POST",
          headers: {
              "X-CSRFToken": getCSRFToken(),
              "Content-Type": "application/json"
          },
      })
      .then(response => {
        if (response.ok) {
            window.location.reload();
        }
          else {
              alert("Logout failed. Please try again.");
          }
      })
      .catch(error => console.error("Logout error:", error));
    });

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

});
