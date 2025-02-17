  document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("flashcards_questions_form");
    const carousel = new bootstrap.Carousel('#carouselExampleDark');
    const showAllImagesButton = document.getElementById("show-all-images-checkbox");

    showAllImagesButton.addEventListener("change", function () {
      document.querySelectorAll('.show_image_checkbox').forEach(checkbox => {
        if (this.checked) {
          checkbox.checked = true; // Check all checkboxes
          const image = checkbox.closest('.image_container').querySelector('.flashcard_image');
          if (image) {
            image.style.filter = "none"; // Remove blur from all images
          }
        } else {
          checkbox.checked = false; // Check all checkboxes
          const image = checkbox.closest('.image_container').querySelector('.flashcard_image');
          if (image) {
            image.style.filter = "blur(8px)"; // Remove blur from all images
          }
        }

      });
    });

    // Add event listener to all checkboxes to toggle image visibility
    document.querySelectorAll('.show_image_checkbox').forEach((checkbox, index) => {
      checkbox.addEventListener('change', function () {
        const image = checkbox.closest('.image_container').querySelector('.flashcard_image');

        // Toggle blur on image based on checkbox state
        if (this.checked) {
          image.style.filter = "none";  // Remove blur
        } else {
          image.style.filter = "blur(8px)";  // Add blur
        }
      });
    });

    document.querySelectorAll("input[name^='user_answer_'],select[name^='user_answer_']").forEach(input => {
      input.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
          event.preventDefault();
          // Check if input is valid before moving to the next slide
          if (input.checkValidity()) {
            carousel.next();
          }
        }
      });
    });
    document.querySelectorAll(".record_btn").forEach((recordButton) => {
        const stopButton = recordButton.closest("div").querySelector(".stop_btn");
        const playback = recordButton.closest("div").querySelector(".playback_controls");
        const audioDataInput = recordButton.closest("div").querySelector(".audio_data");

        let mediaRecorder;
        let chunks = [];

        recordButton.addEventListener("click", async (event) => {
            // Start recording
            event.preventDefault();
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();

            mediaRecorder.ondataavailable = (e) => {
                chunks.push(e.data);
            };

            mediaRecorder.onstop = () => {
                const blob = new Blob(chunks, { type: "audio/wav" });
                chunks = [];

                // Set playback source
                const audioURL = URL.createObjectURL(blob);
                playback.src = audioURL;
                playback.style.display = "block";

                // Convert blob to Base64 and store in the hidden field
                const reader = new FileReader();
                reader.readAsDataURL(blob);
                reader.onloadend = () => {
                    audioDataInput.value = reader.result; // Set Base64 audio string
                };
            };

            recordButton.disabled = true;
            stopButton.disabled = false;
        });

        stopButton.addEventListener("click", () => {
            mediaRecorder.stop();
            recordButton.disabled = false;
            stopButton.disabled = true;
        });
    });

    // Form submission validation
    form.addEventListener("submit", function (event) {
        event.preventDefault();
        const flashcardsetId = document.getElementById("flashcardset").getAttribute("data-id");
        const answers = {};
        const audioAnswers = {};
        let unansweredFlashcards = [];
        let unanswered = false;

        document.querySelectorAll('.carousel-indicators button').forEach(button => {
           button.classList.remove("bg-danger");
       });

        // Check if all flashcards have text or audio answers
        document.querySelectorAll("input[name^='user_answer_'],select[name^='user_answer_']").forEach((input, index) => {
            const flashcardId = input.name.split("_")[2];
            const value = input.tagName === "SELECT" && input.value === "Choose a chapter" ? "" : input.value.trim();
            const audioInput = document.querySelector(`input[name='audio_data_${flashcardId}']`);

            answers[flashcardId] = value;

            if (!value || !audioInput || !audioInput.value) {
                    unanswered = true;
                    unansweredFlashcards.push(flashcardId);
                    const indicatorButton = document.querySelector(`[data-bs-slide-to="${index}"]`);
                    if (indicatorButton) {
                        indicatorButton.classList.add("bg-danger");
                    }
            }
        });

        if (unanswered) {
            const confirmSubmission = confirm("Not all flashcards have been answered.\n\nAre you sure you want to submit? ");

            if (confirmSubmission) {
              const csrfToken = document.querySelector("[name='csrfmiddlewaretoken']").value;

              fetch(`/flashcards/submit_flashcardset_answers/${flashcardsetId}/`, {
                  method: "POST",
                  headers: {
                      "Content-Type": "application/json",
                      "X-CSRFToken": csrfToken,
                  },
                  body: JSON.stringify({
                      answers: answers,
                      audio_answers: Object.fromEntries(
                          Array.from(document.querySelectorAll("input[name^='audio_data_']")).map((input) => [
                              input.name.split("_")[2],
                              input.value,
                          ])
                      ),
                  }),
              })
                  .then((response) => {
                      if (response.ok) {
                          window.location.reload();
                      } else {
                          alert("Failed to submit answers. Please try again.");
                      }
                  })
                  .catch((error) => {
                      console.error("Error submitting answers:", error);
                      alert("An error occurred. Please try again.");
                  });
            }
        } else {
            // Submit form via AJAX
            const csrfToken = document.querySelector("[name='csrfmiddlewaretoken']").value;

            fetch(`/flashcards/submit_flashcardset_answers/${flashcardsetId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
                body: JSON.stringify({
                    answers: answers,
                    audio_answers: Object.fromEntries(
                        Array.from(document.querySelectorAll("input[name^='audio_data_']")).map((input) => [
                            input.name.split("_")[2],
                            input.value,
                        ])
                    ),
                }),
            })
                .then((response) => {
                    if (response.ok) {
                        window.location.reload();
                    } else {
                        alert("Failed to submit answers. Please try again.");
                    }
                })
                .catch((error) => {
                    console.error("Error submitting answers:", error);
                    alert("An error occurred. Please try again.");
                });
        }
    });


  });
