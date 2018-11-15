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

// Choose ability
let add_skill_set = (url: string, csrf: string, skills: string): void => {
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
    success: function(data) {
      $('.character_skills').empty().html(data);
    }
  })
}
let add_equipment: number[] = [];
let skill_add_to_list = (id: string, name: string, category: string): void => {
  let div = document.createElement('div');
  let parent = document.getElementsByClassName('chosen-equipment')[0];
  div.setAttribute('class', 'equip');
  div.setAttribute('data-skill', id);
  div.innerHTML = `<button type="button" class="btn btn-danger btn-sm remove-equip" style="float: left; margin-right: 2px;" data-equip-id="${id}"><span class="fa fa-minus"></span></button><p><b>${name}</b><br><span style="font-size: 10px"><i>${category}</i></span></p>`;
  parent.appendChild(div);
}
let check_equipped = (): void => {
  if (add_equipment.length == 0) {
    $('.submit-equipment').attr('disabled', 'disabled');
  } else {
    $('.submit-equipment').removeAttr('disabled');
  }
}
check_equipped();
let refresh_equipment = (url: string, csrf: string): void => {
  $.ajax({
    type: 'GET',
    url: url,
    async: false,
    success: function(data) {
      
    }
  })
}
let submit_equipment = (url: string, csrf: string): void => {
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
    success: function(data) {
      window.location.href = data;
    }
  })
}

let remove_equipment = (url: string, csrf: string, equip: number): void => {
  $.ajax({
    type: 'POST',
    url: url,
    async: true,
    cache: false,
    data: {
      'csrfmiddlewaretoken': csrf,
      'remove_equipment': true,
      'equip': equip
    },
    success: function(data) {
      $('.character-inventory').empty().html(data);
    }
  })
}
