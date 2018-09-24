var select_class = function (url, csrf, value) {
    $.ajax({
        type: 'POST',
        url: url,
        cache: false,
        async: true,
        data: {
            'csrfmiddlewaretoken': csrf,
            'character_class': true,
            'c_class': value
        },
        success: function (data) {
            $('.class_details').empty().html(data);
        },
        error: function (data) {
            console.log(data);
        }
    });
};
// Character Race details
var select_race = function (url, csrf, value) {
    $.ajax({
        type: 'POST',
        url: url,
        cache: false,
        async: true,
        data: {
            'csrfmiddlewaretoken': csrf,
            'character_race': true,
            'c_race': value
        },
        success: function (data) {
            $('.race_details').empty().html(data);
        },
        error: function (data) {
            console.log(data);
        }
    });
};
