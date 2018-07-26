// starting a new campaign
var newCampaign = function (csrf, url, name, limit, obj, start, end) {
    var slug = name.toLowerCase().split(' ').join('-');
    // if (name == undefined || name == null) {
    //   return false
    // }
    console.log('obj: ' + end);
    $.ajax({
        type: 'POST',
        url: url,
        cache: false,
        async: true,
        data: {
            'csrfmiddlewaretoken': csrf,
            'name': name,
            'slug': slug,
            'player_limit': limit,
            'obj': obj,
            'start': start,
            'end': end
        },
        success: function (data) {
            window.location.href = data;
        },
        error: function (data) {
            console.log(data);
        }
    });
};
// New Chapter for the campaign
var newChapter = function (csrf, url, name, desc) {
    var slug = name.toLowerCase().split(' ').join('-');
    $.ajax({
        type: 'POST',
        url: url,
        cache: false,
        async: true,
        data: {
            'csrfmiddlewaretoken': csrf,
            'slug': slug,
            'name': name,
            'desc': desc
        },
        success: function (data) {
            window.location.href = data;
            console.log('success');
        },
        error: function (data) {
            console.log(data);
        }
    });
};
