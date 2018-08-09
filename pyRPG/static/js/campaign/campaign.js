// starting a new campaign
var newCampaign = function (csrf, url, name, limit, obj, start, end) {
    var slug = name.toLowerCase().split(' ').join('-');
    // if (name == undefined || name == null) {
    //   return false
    // }
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
// get form
var getForm = function (csrf, url, form) {
    $.ajax({
        type: 'POST',
        url: url,
        cache: false,
        async: true,
        data: {
            'csrfmiddlewaretoken': csrf,
            'call_modal': true,
            'form': form
        },
        success: function (data) {
            $('.modal-content').empty().html(data);
            $('#camp_modal').modal('show');
        },
        error: function (data) {
            console.log(data);
        }
    });
};
// Create new enemy
var newEnemy = function (csrf, url, name, type, lvl, hp, dmg, spd, def, dex, con, int, cha, wis, act, info) {
    $.ajax({
        type: 'POST',
        url: url,
        cache: false,
        async: true,
        data: {
            'csrfmiddlewaretoken': csrf,
            'new_enemy': true,
            'name': name,
            'enemy_type': type,
            'hp': hp,
            'damage': dmg,
            'speed': spd,
            'defence': def,
            'dex': dex,
            'constitution': con,
            'intelligence': int,
            'charm': cha,
            'wisdom': wis,
            'actions': act,
            'additional-info': info
        },
        success: function (data) {
            console.log(data);
        },
        error: function (data) {
            console.log(data);
        }
    });
};
