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
            $('.character_traits').empty().html(data);
            getInfo();
        }
    });
};
// edit button
var getInfo = function () {
    var info = document.getElementsByClassName('info-div');
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
    var html = "\n  <form class=\"" + update + "_form\" data-update=\"" + update + "\">\n    <div class=\"form-group\">\n      <textarea name=\"" + update + "\" class=\"form-control\" rows=\"5\" cols=\"80\">" + text + "</textarea>\n    </div>\n    <button type=\"submit\" class=\"btn btn-primary\" name=\"button\">Submit</button> <button type=\"button\" class=\"btn\">Cancel</button>\n  </form>";
    $('.info-text-' + update).empty().html(html);
    document.getElementsByClassName('edit_' + update)[0].style.visibility = 'hidden';
    getInfo();
    return false;
};
// infoText.mousemove(() => {
//   console.log($(this).find('.edit-conteiner'));
//   $(this).find('.edit-conteiner').css('visibility', 'visible');
// })
