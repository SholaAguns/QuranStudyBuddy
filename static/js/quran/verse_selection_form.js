$(document).ready(function () {
      loadOptions('/flashcards/get_range_options/' + 'verse', '#verseChapterRangeStart');
      loadOptions('/flashcards/get_range_options/' + 'verse', '#verseChapterRangeEnd');

$('#verseChapterRangeStart').change(function () {
    const startChapter = $(this).val();

    if (startChapter) {
      loadOptions(`/flashcards/get_verses_options/${startChapter}`, '#verseRangeStart');
    }
});

$('#verseChapterRangeEnd').change(function () {
    const endChapter = $(this).val();

    if (endChapter) {
      loadOptions(`/flashcards/get_verses_options/${endChapter}`, '#verseRangeEnd');
    }
});

function loadOptions(url, selector) {
    $.get(url, function (data) {
        const select = $(selector);
        select.empty();
        select.append(new Option('Select an option', ''));
        data.options.forEach(option => {
            select.append(new Option(option.label, option.value));
        });
    });
}


// Form submission
$('#verse_selection_form').submit(function (e) {
    e.preventDefault();

    const verseRangeStart = parseInt($('#verseRangeStart').val(), 10);
    const verseRangeEnd = parseInt($('#verseRangeEnd').val(), 10);

    if (isNaN(verseRangeStart) || isNaN(verseRangeEnd) || verseRangeEnd < verseRangeStart) {
        alert('Error: The end of the range must be greater than the start.');
        return;
    }

    if (verseRangeEnd - verseRangeStart > 300) {
            alert('Error: List cannot contain more than 300 vereses.');
            return;
    }


      const formData = $(this).serializeArray();

    $.post('/quran/create_verse_selection', formData, function (response) {
        if (response.redirect_url) {
            window.location.href = response.redirect_url;
        } else {
            alert('Verse Selection created successfully!');
        }
    }).fail(function (xhr) {
        alert('Form submission failed: ' + xhr.responseText);
    });
});
});
