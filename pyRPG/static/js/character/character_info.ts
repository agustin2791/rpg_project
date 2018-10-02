// import * as $ from 'jquery';


var submit_trait = (url, csrf, trait, description) => {
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
    success: function(data) {
      $('.character_traits').empty().html(data)
      getInfo();
    }
  })
}

// edit button
var getInfo = (): void => {
  var info = document.getElementsByClassName('info-div');
  for (var i = 0; i < info.length; i++) {
    info[i].addEventListener('mouseenter', (i) => {
      var update = i.path[0].dataset.update;
      var edit = document.getElementsByClassName('edit_' + update)[0];
      if (edit) { edit.style.visibility = 'visible' }
    })
    info[i].addEventListener('mouseleave', (i) => {
      var update = i.path[0].dataset.update;
      var edit = document.getElementsByClassName('edit_' + update)[0];
      if (edit) {edit.style.visibility = 'hidden';}
    })
  }
}
var openEdit = (update: string, text: string): boolean => {
  var html = `
  <form class="${update}_form" data-update="${update}">
    <div class="form-group">
      <textarea name="${update}" class="form-control" rows="5" cols="80">${text}</textarea>
    </div>
    <button type="submit" class="btn btn-primary" name="button">Submit</button> <button type="button" class="btn">Cancel</button>
  </form>`
  $('.info-text-' + update).empty().html(html);
  document.getElementsByClassName('edit_' + update)[0].style.visibility = 'hidden';
  getInfo();
  return false;
}
// add New Feature
var addNewFeature = (url: string, csrf: string, name: string, desc: string): void => {
  $.ajax({
    type: 'POST',
    url: url,
    async: true,
    cache: false,
    data: {
      'csrfmiddlewaretoken': csrf,
      'new_feature': true,
      'name': name,
      'desc':desc
    },
    success: function(data) {
      $('.character_feature').empty().html(data);
      $('body').removeClass('modal-open');
      $('.modal-backdrop').remove();
    }
  })
}
