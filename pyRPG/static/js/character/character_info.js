// import * as $ from 'jquery';
var submit_trait = function (url, csrf, trait, description) {
    $.ajax({
        type: 'POST',
        url: url,
        async: true,
        cache: false,
        data: {
            'csrfmiddlewaretoken': csrf,
            'add_feature': true,
            'trait': trait,
            'description': description
        },
        success: function (data) {
            if (trait == 'background') {
                $('.character_background').empty().html(data);
            }
            else if (trait.startsWith('feature')) {
                $('.character_feature').empty().html(data);
            }
            else {
                $('.character_traits').empty().html(data);
            }
            getInfo();
        }
    });
};
// edit button
var getInfo = function () {
    var info = document.getElementsByClassName('info-div');
    console.log(info.length);
    for (var i = 0; i < info.length; i++) {
        info[i].addEventListener('mouseenter', function (i) {
            var update = i.path[0].dataset.update;
            var edit = document.getElementsByClassName('edit_' + update)[0];
            if (edit) {
                edit.style.visibility = 'visible';
            }
        });
        info[i].addEventListener('mouseleave', function (i) {
            var update = i.path[0].dataset.update;
            var edit = document.getElementsByClassName('edit_' + update)[0];
            if (edit) {
                edit.style.visibility = 'hidden';
            }
        });
    }
};
var openEdit = function (update, text) {
    var toUpdate = update;
    if (toUpdate.startsWith('feature')) {
        toUpdate = 'feature';
    }
    var html = "\n  <form class=\"" + toUpdate + "_form\" data-update=\"" + update + "\">\n    <div class=\"form-group\">\n      <textarea name=\"" + update + "\" class=\"form-control\" rows=\"5\" cols=\"80\">" + text + "</textarea>\n    </div>\n    <button type=\"submit\" class=\"btn btn-primary\" name=\"button\">Submit</button> <button type=\"button\" class=\"btn cancel\" data-update=\"" + update + "\">Cancel</button>\n  </form>";
    $('.info-text-edit-' + update).empty().html(html);
    document.getElementsByClassName('edit_' + update)[0].style.visibility = 'hidden';
    getInfo();
    return false;
};
// add New Feature
var addNewFeature = function (url, csrf, name, desc, skills, object) {
    $.ajax({
        type: 'POST',
        url: url,
        async: true,
        cache: false,
        data: {
            'csrfmiddlewaretoken': csrf,
            'new_feature': true,
            'object': object,
            'name': name,
            'desc': desc,
            'skills': skills
        },
        success: function (data) {
            if (object === 'feature') {
                $('.character_feature').empty().html(data);
            }
            else if (object === 'background') {
                $('.character_background').empty().html(data);
                $('.character-bg-name').empty().html(name);
            }
            $('body').removeClass('modal-open');
            $('.modal-backdrop').remove();
        }
    });
};
// Choose ability
var add_skill_set = function (url, csrf, skills) {
    $.ajax({
        type: 'POST',
        url: url,
        async: true,
        cache: false,
        data: {
            'csrfmiddlewaretoken': csrf,
            'add_skills': true,
            'skills': skills
        },
        success: function (data) {
            $('.character_skills').empty().html(data);
        }
    });
};
var add_equipment = [];
var skill_add_to_list = function (id, name, category) {
    var div = document.createElement('div');
    var parent = document.getElementsByClassName('chosen-equipment')[0];
    div.setAttribute('class', 'equip');
    div.setAttribute('data-skill', id);
    div.innerHTML = "<button type=\"button\" class=\"btn btn-danger btn-sm remove-equip\" style=\"float: left; margin-right: 2px;\" data-equip-id=\"" + id + "\"><span class=\"fa fa-minus\"></span></button><p><b>" + name + "</b><br><span style=\"font-size: 10px\"><i>" + category + "</i></span></p>";
    parent.appendChild(div);
};
var check_equipped = function () {
    if (add_equipment.length == 0) {
        $('.submit-equipment').attr('disabled', 'disabled');
    }
    else {
        $('.submit-equipment').removeAttr('disabled');
    }
};
check_equipped();
var refresh_equipment = function (url, csrf) {
    $.ajax({
        type: 'GET',
        url: url,
        async: false,
        success: function (data) {
        }
    });
};
var submit_equipment = function (url, csrf) {
    $.ajax({
        type: 'POST',
        url: url,
        async: true,
        cache: false,
        data: {
            'csrfmiddlewaretoken': csrf,
            'add_equipment': true,
            'equip': add_equipment
        },
        success: function (data) {
            window.location.href = data;
        }
    });
};
var add_spell = function (url, csrf, spell) {
    $.ajax({
        type: 'POST',
        url: url,
        async: true,
        cache: false,
        data: {
            'csrfmiddlewaretoken': csrf,
            'add_spell': true,
            'spell': spell
        },
        success: function (data) {
            $('.character-spells').empty().html(data);
        }
    });
};
var remove = function (url, csrf, subject, item) {
    $.ajax({
        type: 'POST',
        url: url,
        async: true,
        cache: false,
        data: {
            'csrfmiddlewaretoken': csrf,
            'remove': true,
            'subject': subject,
            'item': item
        },
        success: function (data) {
            if (subject == 'equip') {
                $('.character-inventory').empty().html(data);
            }
            if (subject == 'feat') {
                $('.character_feature').empty().html(data);
                getInfo();
            }
        }
    });
};
