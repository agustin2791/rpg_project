// Character
// Create Character Section
var ability = function () {
    var ability_result = [];
    var html = "<div class=\"row generate-ability\">";
    for (var i = 0; i < 6; i++) {
        var abilities = [];
        for (var j = 0; j < 4; j++) {
            var ability = Math.floor(Math.random() * 6) + 1;
            abilities.push(ability);
        }
        abilities.sort();
        html += "<div class=\"col-2\"><p style=\"text-align: justify\">";
        for (var a in abilities) {
            if (a == 0) {
                html += "<span style=\"text-decoration:line-through; color: red\">" + abilities[a] + "</span> ";
            }
            else {
                html += abilities[a] + " ";
            }
        }
        abilities.shift();
        var result = abilities.reduce(function (a, b) { return a + b; });
        html += "</p><h3>" + result + "</h3></div>";
        ability_result.push(result);
    }
    html += "</div>";
    var ability_number = $('.ability-numbers').html(html);
};
// modifier
var modifier = function (ability) {
    var mod;
    if (ability == 1) {
        mod = -5;
    }
    else if (ability >= 30) {
        mod = 10;
    }
    else {
        mod = Math.floor(ability / 2) - 5;
    }
    return mod;
};
