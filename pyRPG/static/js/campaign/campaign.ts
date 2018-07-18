// starting a new campaign
var newCampaign = (csrf, url, name, limit, obj, start, end) => {
  var slug = name.toLowerCase().split(' ').join('-');
  // if (name == undefined || name == null) {
  //   return false
  // }
  console.log('obj: ' + end)
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
    success: (data) => {
      window.location.href = data;
    },
    error: (data) => {
      console.log(data);
    }
  });
};
