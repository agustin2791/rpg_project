
var select_class = (url, csrf, value) => {
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
    success: function(data) {
      $('.class_details').empty().html(data);
    },
    error: function(data) {
      console.log(data)
    }
  })
}

// Character Race details
var select_race = (url, csrf, value) => {
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
    success: function(data) {
      $('.race_details').empty().html(data);
    },
    error: function(data) {
      console.log(data)
    }
  })
}
// Submit character
var submit_character = (url, csrf, c_class, c_race, alignment, name, level, hit_points, speed, strength, dex, cons, int, charm, wisdom) => {
  $.ajax({
    type: 'POST',
    url: url,
    async: true,
    cache: false,
    data: {
      'csrfmiddlewaretoken': csrf,
      'new_character': true,
      'c_class': c_class,
      'c_race': c_race,
      'alignment': alignment,
      'name': name,
      'level': level,
      'hit_points': hit_points,
      'speed': speed,
      'strength': strength,
      'dex': dex,
      'cons': cons,
      'int': int,
      'charm': charm,
      'wisdom': wisdom
    },
    success: function(data) {
      window.location.href = data;
    }
  })
}
