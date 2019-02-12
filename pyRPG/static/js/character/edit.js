$(document).ready(function() {

    $(document).on('submit', '.personality_traits_form, .ideals_form, .bonds_form, .flaws_form, .equipment_form, .background_form, .feature_form', function(e) {
      e.preventDefault();
      console.log("Submitted");
      var trait = $(this).attr('data-update');
      var description = $('textarea[name="'+trait+'"]').val();
      submit_trait(url, csrf, trait, description);
      return false;
    })
    getInfo();
    // Edit Feature
    $(document).on('click', '.edit', function(e) {
      e.preventDefault();
      var update = $(this).attr('data-update');
      var text = $('.info-text-' + update + ' > p').text();
      $('.info-text-' + update).hide();
      openEdit(update, text);
      getInfo();
    });
    // Add new feature
    $(document).on('submit', '.new_feature_form', function() {
      var name = $('input[name="feature_name"]').val(),
          desc = $('textarea[name="feature_desc"]').val();
      addNewFeature(url, csrf, name, desc, 'none', 'feature');
      return false;
    });
    // Add new Background
    $(document).on('click', '.submit-background', function() {
      var name = $('input[name="background_name"]').val(),
          desc = $('textarea[name="background_desc"]').val();
      var get_skills = $('input[name="bg_skills');
      var checked_skills = []
      for (let i = 0; i < get_skills.length; i++){
        if (get_skills[i].checked) { 
          checked_skills.push(get_skills[i]); 
          console.log(get_skills[i]);
        }
      }
      if (checked_skills.length != 2) {
        return false;
      }
      var skills = checked_skills[0].value + ', ' + checked_skills[1].value;
      addNewFeature(url, csrf, name, desc, skills, 'background');
      return false;
    })
    // cancel update
    $(document).on('click', '.cancel', function() {
      var update = $(this).attr('data-update');
      $('.info-text-edit-' + update).empty();
      $('.info-text-' + update).show();
    });
    // count checked
    $(document).on('click', '.skill_checkbox', function() {
      let checkbox = $('input[name="choose_skill"]');
      let chosen = 0;
      for (let i = 0; i < checkbox.length; i++) {
        if (checkbox[i].checked) {
          chosen += 1;
        }
      }
      if (chosen === class_skill_limit) {
        document.getElementsByClassName('skill_count')[0].style.color = '#16a085';
      } else if (chosen > class_skill_limit) {
        document.getElementsByClassName('skill_count')[0].style.color = '#ff0000';
      }
      document.getElementById('skills_chosen').innerHTML = chosen;
    })
    // apply checked
    $(document).on('click', '.submit_skills', function() {
      let checkbox = $('input[name="choose_skill"]');
      let chosen = 0;
      let skills = [];
      for (let i = 0; i < checkbox.length; i++) {
        if (checkbox[i].checked) {
          chosen += 1;
          skills.push(checkbox[i].value);
        }
      }
      if (skills.length != class_skill_limit) {
        document.getElementsByClassName('skills_alert')[0].style.display = 'block';
        return false;
      }
      let add_skill = skills.join(', ');
      add_skill_set(url, csrf, add_skill);

      return false;
    })
    $(document).on('click', '.add-equipment', function() {
      let equip_id = $(this).attr('data-equip-id');
      let equip_name = $(this).attr('data-equip-name');
      let equip_cat = $(this).attr('data-equip-cat');
      add_equipment.push(parseInt(equip_id));
      console.log(add_equipment);
      skill_add_to_list(equip_id, equip_name, equip_cat);
      $(this).attr('disabled', 'disabled')
      check_equipped();
      return false;
    });
    $(document).on('click', '.remove-equip', function() {
      let equip_id = $(this).attr('data-equip-id');
      for (let i = 0; i < add_equipment.length; i++) {
        if (add_equipment[i] == parseInt(equip_id)) {
          add_equipment.splice(i, 1);
        }
      }
      console.log(add_equipment);
      let div = document.querySelectorAll('div[data-skill="' + equip_id + '"]')[0];
      let parent = document.getElementsByClassName('chosen-equipment')[0];
      parent.removeChild(div);
      $('.add-equipment[data-equip-id="'+ equip_id +'"]').removeAttr('disabled');
      check_equipped();
      return false;
    });
    $(document).on('click', '.submit-equipment', function() {
      submit_equipment(url, csrf);
      return false;
    });
    $(document).on('click', '.equip-remove', function() {
      let equip = $(this).attr('data-equip');
      let conf = confirm('Are you sure you want to remove this?');
      if (conf) {
        remove(url, csrf, 'equip', equip);
      }
      return false;
    });
    $(document).on('click', '.add-spell', function() {
      let spell_id = $(this).attr('data-spell');
      add_spell(url, csrf, spell_id);
      $(this).attr('disabled', 'disabled');
      return false;
    })
    $(document).on('click', '.delete_feat', function() {
      let feat = $(this).attr('data-delete');
      let conf = confirm('Are you sure you want to remove this Feature?');
      if (conf) {
        remove(url, csrf, 'feat', feat);
      }
      return false;
    });
    $(document).on('click', '.remove-spell', function() {
      let spell_id = $(this).attr('data-spell');
      let conf = confirm('Are you sure you want to remove this spell from your spell list?');
      if (conf) {
        remove(url, csrf, 'spell', spell_id);
      }
      return false;
    })
    var active_spell_info = NaN;
    var active_equip_info = NaN;
    $(document).on('click', '.get_spell_info', function(event) {
      let spell_id = $(this).attr('data-spell');
      let info = $('.spell-info[data-spell="' + spell_id + '"]');
      if (active_spell_info !== spell_id && active_spell_info === NaN) {
        active_spell_info = spell_id;
        } else if (active_spell_info !== spell_id) {
        $('.spell-info[data-spell="' + active_spell_info + '"]').css('opacity', 0);
        $('.spell-info[data-spell="' + active_spell_info + '"]').css('display', 'none')
        active_spell_info = spell_id;
      }
      if (info.css('display') == 'none') {
        info.css('display', 'block');
        setTimeout(function() {
          info.css('opacity', 1);
          if (event.clientY < 300) {
            info.css('top', 0);
            info.css('left', -300)
          }
          console.log(event.clientY)
        }, 1)
        info.css('top', -info.outerHeight() + 5 + 'px')
      } else {
        info.css('opacity', 0);
        setTimeout(function() {
          info.css('display', 'none')
        }, 500);
        active_spell_info = NaN
      }
    });
    $(document).on('click', '.equip-info', function() {
      let equip_id = $(this).attr('data-equip');
      let info = $('.equip-details[data-equip="' + equip_id + '"]');
      if (active_equip_info !== equip_id && active_equip_info === NaN) {
        active_equip_info = equip_id;
        } else if (active_equip_info !== equip_id) {
        $('.equip-details[data-equip="' + active_equip_info + '"]').css('opacity', 0);
        $('.equip-details[data-equip="' + active_equip_info + '"]').css('display', 'none')
        active_equip_info = equip_id;
      }
      if (info.css('display') == 'none') {
        info.css('display', 'block');
        setTimeout(function() {
          info.css('opacity', 1);
        }, 1)
        info.css('top', -info.outerHeight() + 5 + 'px')
      } else {
        info.css('opacity', 0);
        setTimeout(function() {
          info.css('display', 'none')
        }, 500);
        active_equip_info = NaN
      }
    });
  })