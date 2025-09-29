function showAnnonymous() {
    document.getElementById('annonymous-field').style.display = 'flex';
    document.getElementById('specializations-field').classList.remove('md:col-span-13');
    document.getElementById('specializations-field').classList.add('md:col-span-10');
}
function hideAnnonymous() {
    document.getElementById('annonymous-field').style.display = 'none';
    document.getElementById('specializations-field').classList.remove('md:col-span-10');
    document.getElementById('specializations-field').classList.add('md:col-span-13');
}

var tagSelector = new MultiSelectTag('id_post_type', {
    maxSelection: 1,
    required: true,
    placeholder: '.',
    onChange: function (selected) {
        console.log('Selection changed:', selected);
        if (selected.length > 0 && selected[0]['id'] == 3) {
            showAnnonymous();
        } else {
            hideAnnonymous();
        }
    }
});
var tagSelector = new MultiSelectTag('id_years', {
    maxSelection: 4,
    required: true,
    placeholder: '.',
    onChange: function (selected) {
        console.log('Selection changed:', selected);
    }
});
var tagSelector = new MultiSelectTag('id_majors', {
    maxSelection: 4,
    required: true,
    placeholder: '.',
    onChange: function (selected) {
        console.log('Selection changed:', selected);
    }
});
var tagSelector = new MultiSelectTag('id_specializations', {
    maxSelection: 5,
    required: false,
    placeholder: '.',
    onChange: function (selected) {
        console.log('Selection changed:', selected);
    }
});

if (document.getElementById('id_post_type').value) {
    var selected = JSON.parse(document.getElementById('id_post_type').value);
    if (selected == 3) {
        showAnnonymous();
    } else {
        hideAnnonymous();
    }
}