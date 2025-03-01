$("#verse_score_tab").on("click", function() {
    $.ajax({
        url: "/scorecard/get_verse_stats/",
        type: "GET",
        dataType: "json",
        success: function(data) {
            let strongestChapterDetails = data.verse_strongest_chapter
                ? `${data.verse_strongest_chapter} (${data.verse_strongest_chapter_correct_count}/${data.verse_strongest_chapter_total_count})`
                : "N/A";

            let weakestChapterDetails = data.verse_weakest_chapter
                ? `${data.verse_weakest_chapter} (${data.verse_weakest_chapter_correct_count}/${data.verse_weakest_chapter_total_count})`
                : "N/A";

            $("#verse_total_count").text(data.verse_total_count || "N/A");
            $("#verse_overall_score").text(
            (data.verse_overall_score !== undefined && data.verse_overall_score !== null)
                ? data.verse_overall_score + ' %'
                : "N/A"
            );
            $("#verse_strongest_chapter").text(strongestChapterDetails);

            $("#verse_weakest_chapter").text(weakestChapterDetails);

        },
        error: function(xhr, status, error) {
            console.error("Error fetching stats:", error);
        }
    });
});

$("#phrase_score_tab").on("click", function() {
    $.ajax({
        url: "/scorecard/get_phrase_stats/",
        type: "GET",
        dataType: "json",
        success: function(data) {
            let strongestCategoryDetails = data.phrase_strongest_category
                ? `${data.phrase_strongest_category} (${data.phrase_strongest_category_correct_count}/${data.phrase_strongest_category_total_count})`
                : "N/A";

            let weakestCategoryDetails = data.phrase_weakest_category
                ? `${data.phrase_weakest_category} (${data.phrase_weakest_category_correct_count}/${data.phrase_weakest_category_total_count})`
                : "N/A";

            $("#phrase_total_count").text(data.phrase_total_count || "N/A");
            $("#phrase_overall_score").text(
            (data.phrase_overall_score !== undefined && data.phrase_overall_score !== null)
                ? data.phrase_overall_score + ' %'
                : "N/A"
            );
            $("#phrase_strongest_category").text(strongestCategoryDetails);

            $("#phrase_weakest_category").text(weakestCategoryDetails);

        },
        error: function(xhr, status, error) {
            console.error("Error fetching stats:", error);
        }
    });
});

$("#verse_selection_score_tab").on("click", function() {
    $.ajax({
        url: "/scorecard/get_verse_selection_stats/",
        type: "GET",
        dataType: "json",
        success: function(data) {
            let strongestChapterDetails = data.verse_selection_strongest_chapter
                ? `${data.verse_selection_strongest_chapter} (${data.verse_selection_strongest_chapter_correct_count}/${data.verse_selection_strongest_chapter_total_count})`
                : "N/A";

            let weakestChapterDetails = data.verse_selection_weakest_chapter
                ? `${data.verse_selection_weakest_chapter} (${data.verse_selection_weakest_chapter_correct_count}/${data.verse_selection_weakest_chapter_total_count})`
                : "N/A";

            $("#verse_selection_total_count").text(data.verse_selection_total_count || "N/A");
            $("#verse_selection_overall_score").text(
            (data.verse_selection_overall_score !== undefined && data.verse_selection_overall_score !== null)
                ? data.verse_selection_overall_score + ' %'
                : "N/A"
            );
            $("#verse_selection_strongest_chapter").text(strongestChapterDetails);

            $("#verse_selection_weakest_chapter").text(weakestChapterDetails);

        },
        error: function(xhr, status, error) {
            console.error("Error fetching stats:", error);
        }
    });
});

$("#word_score_tab").on("click", function() {
    $.ajax({
        url: "/scorecard/get_word_stats/",
        type: "GET",
        dataType: "json",
        success: function(data) {
            let strongestChapterDetails = data.word_strongest_chapter
                ? `${data.word_strongest_chapter} (${data.word_strongest_chapter_correct_count}/${data.word_strongest_chapter_total_count})`
                : "N/A";

            let weakestChapterDetails = data.word_weakest_chapter
                ? `${data.word_weakest_chapter} (${data.word_weakest_chapter_correct_count}/${data.word_weakest_chapter_total_count})`
                : "N/A";

            $("#word_total_count").text(data.word_total_count || "N/A");
            $("#word_overall_score").text(
            (data.word_overall_score !== undefined && data.word_overall_score !== null)
                ? data.word_overall_score + ' %'
                : "N/A"
            );
            $("#word_strongest_chapter").text(strongestChapterDetails);

            $("#word_weakest_chapter").text(weakestChapterDetails);

        },
        error: function(xhr, status, error) {
            console.error("Error fetching stats:", error);
        }
    });
});