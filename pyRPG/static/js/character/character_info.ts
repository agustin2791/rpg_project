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
      if (trait == 'background') {
        $('.character_background').empty().html(data);
      } else if (trait.startsWith('feature')) {
        $('.character_feature').empty().html(data)
      } else {
        $('.character_traits').empty().html(data)
      }
      getInfo();
    }
  })
}

// edit button
var getInfo = (): void => {
  var info = document.getElementsByClassName('info-div');
  console.log(info.length);
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
  let toUpdate = update;
  if (toUpdate.startsWith('feature')) {
    toUpdate = 'feature';
  }
  var html = `
  <form class="${toUpdate}_form" data-update="${update}">
    <div class="form-group">
      <textarea name="${update}" class="form-control" rows="5" cols="80">${text}</textarea>
    </div>
    <button type="submit" class="btn btn-primary" name="button">Submit</button> <button type="button" class="btn cancel" data-update="${update}">Cancel</button>
  </form>`
  $('.info-text-edit-' + update).empty().html(html);
  document.getElementsByClassName('edit_' + update)[0].style.visibility = 'hidden';
  getInfo();
  return false;
}
// add New Feature
var addNewFeature = (url: string, csrf: string, name: string, desc: string, skills: string, object: string): void => {
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
      'desc':desc,
      'skills': skills
    },
    success: function(data) {
      if (object === 'feature') {
        $('.character_feature').empty().html(data);
      } else if (object === 'background') {
        $('.character_background').empty().html(data);
        $('.character-bg-name').empty().html(name);
      }
      $('body').removeClass('modal-open');
      $('.modal-backdrop').remove();
    }
  })
}
