
    $(document).ready(function () {
// Fetch service types
$.get('/flashcards/get_service_types/', function (data) {
    const serviceTypeSelect = $('#serviceType');
    data.service_types.forEach(service => {
        serviceTypeSelect.append(new Option(service, service));
    });
});

// Fetch request types when service type changes
$('#serviceType').change(function () {


    document.querySelectorAll('.added_option').forEach(function(el) {
        el.remove();
    });


    document.querySelectorAll('.select_container').forEach(function(el) {
        el.style.display = 'none';
    });

    const serviceType = $(this).val();
    const requestTypeSelect = $('#requestType');
    requestTypeSelect.empty();

     const addButton = $('#addIdField');

     if (serviceType) {
       let label = "";
       switch(serviceType){
         case "Verse":
            label = "Add Chapter";
            break;
        case "VerseSelection":
           label = "Add Verse Selection";
           break;
        case "Phrase":
            label = "Add Phrase";
            break;
        case "Word":
            label = "Add Chapter";
            break;
        default:
            label ="Add"
       }
       addButton.text(`${label}`);
     } else {
         addButton.text('Add');
     }

    if (serviceType) {
        $.get(`/flashcards/get_request_types/${serviceType}/`, function (data) {
            data.request_types.forEach(requestType => {
                requestTypeSelect.append(new Option(requestType.label, requestType.value));
            });
        });
        $('#requestTypeContainer').toggle(serviceType !== '');
    }
});

// Handle request type change
$('#requestType').change(function () {
    const requestType = $(this).val();

    // Show or hide input sections based on request type
    $('#idListContainer').toggle(requestType === 'byIds');
    $('#juzListContainer').toggle(requestType === 'byJuz');
    $('#rangeContainer').toggle(requestType === 'byRange');
    $('#categoryContainer').toggle(requestType === 'byCategory');
    $('#verseRangeContainer').toggle(requestType === 'byVerseRange');
    $('#tagsContainer').toggle(requestType === 'byTags');

    // Load options for category if "byCategory" is selected
    if (requestType === 'byCategory') {
        loadOptions('/flashcards/get_category_options/' + $('#serviceType').val(), '#category');
    }

    if (requestType === 'byRange') {
            loadOptions('/flashcards/get_range_options/' + $('#serviceType').val(), '#rangeStart');
            loadOptions('/flashcards/get_range_options/' + $('#serviceType').val(), '#rangeEnd');
    }
    if (requestType === 'byVerseRange' ) {
            loadOptions('/flashcards/get_range_options/' + $('#serviceType').val(), '#verseChapterRangeStart');
            loadOptions('/flashcards/get_range_options/' + $('#serviceType').val(), '#verseChapterRangeEnd');
    }
});

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

// Load options dynamically
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

// Dynamic ID List
$('#addIdField').click(function () {
    const idDropdown = `
        <div class="added_option id-dropdown">
            <select class="id-select form-select-sm"></select>
            <button type="button" class="remove_field_btn removeIdField">Remove</button>
        </div>
    `;
    $('#idListFields').append(idDropdown);
    loadOptions('/flashcards/get_id_options/' + $('#serviceType').val(), '#idListFields .id-select:last');
});

// Dynamic Juz List
$('#addJuzField').click(function () {
    const juzDropdown = `
        <div class="added_option juz-dropdown">
            <select class="juz-select form-select-sm"></select>
            <button type="button" class="remove_field_btn removeJuzField">Remove</button>
        </div>
    `;
    $('#juzListFields').append(juzDropdown);
    loadOptions('/flashcards/get_juz_options/' + $('#serviceType').val(), '#juzListFields .juz-select:last');
});

// Remove dropdowns
$(document).on('click', '.removeIdField', function () {
    $(this).parent().remove();
});
$(document).on('click', '.removeJuzField', function () {
    $(this).parent().remove();
});

// Form submission
$('#flashcard_form').submit(function (e) {
    e.preventDefault();

    const rangeStart = parseInt($('#rangeStart').val(), 10);
    const rangeEnd = parseInt($('#rangeEnd').val(), 10);
    const verseRangeStart = parseInt($('#verseRangeStart').val(), 10);
    const verseRangeEnd = parseInt($('#verseRangeEnd').val(), 10);

    if ($('#rangeContainer').is(':visible')) {
    if (isNaN(rangeStart) || isNaN(rangeEnd) || rangeEnd <= rangeStart) {
        alert('Error: The end of the range must be greater than the start.');
        return;
      }
    }

    if ($('#verseRangeContainer').is(':visible')) {
    if (isNaN(verseRangeStart) || isNaN(verseRangeEnd) || verseRangeEnd <= verseRangeStart) {
        alert('Error: The end of the range must be greater than the start.');
        return;
      }
    }

    // Collect dynamic ID List
    const idList = [];
    $('#idListFields .id-select').each(function () {
        idList.push($(this).val());
    });

    // Collect dynamic Juz List
    const juzList = [];
    $('#juzListFields .juz-select').each(function () {
        juzList.push($(this).val());
    });

    // Prepare form data
    const formData = $(this).serializeArray();
    formData.push({ name: 'idList', value: JSON.stringify(idList) });
    formData.push({ name: 'juzList', value: JSON.stringify(juzList) });

    // Submit the form via AJAX
    $.post('/flashcards/submit_flashcardset_form/', formData, function (response) {
        if (response.redirect_url) {
            window.location.href = response.redirect_url;
        } else {
            alert('Flashcard set created successfully!');
        }
    }).fail(function (xhr) {
        alert('Form submission failed: ' + xhr.responseText);
    });
});
});
