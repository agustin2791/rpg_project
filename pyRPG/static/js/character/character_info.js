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
