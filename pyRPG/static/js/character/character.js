// Character
// Create Character Section
var ability = function () {
    var ability_result = [];
    for (var i_1 = 0; i_1 < 6; i_1++) {
        var abilities = [];
        for (var j = 0; j < 4; j++) {
            var ability = Math.floor(Math.random() * 6) + 1;
            abilities.push(ability);
        }
        abilities.sort();
        abilities.shift();
        var result = abilities.reduce(function (a, b) { return a + b; });
        ability_result.push(result);
    }
    var html = "";
    for (var i = 0; i < ability_result.length; i++) {
        html += "<span class=\"ability_result\">" + ability_result[i] + "</span>";
        if (i != (ability_result.length - 1)) {
            html += ", ";
        }
    }
    var ability_number = $('.ability-numbers').html(html);
};
// modifier
var modifier = function (ability) {
    var mod;
    if (ability == 1) {
        mod = -5;
    }
    else if (2 <= ability && ability <= 3) {
        mod = -4;
    }
    else if (4 <= ability && ability <= 5) {
        mod = -3;
    }
    else if (6 <= ability && ability <= 7) {
        mod = -2;
    }
    else if (8 <= ability && ability <= 9) {
        mod = -1;
    }
    else if (10 <= ability && ability <= 11) {
        mod = 0;
    }
    else if (12 <= ability && ability <= 13) {
        mod = 1;
    }
    else if (14 <= ability && ability <= 15) {
        mod = 2;
    }
    else if (16 <= ability && ability <= 17) {
        mod = 3;
    }
    else if (18 <= ability && ability <= 19) {
        mod = 4;
    }
    else if (20 <= ability && ability <= 21) {
        mod = 5;
    }
    else if (22 <= ability && ability <= 23) {
        mod = 6;
    }
    else if (24 <= ability && ability <= 25) {
        mod = 7;
    }
    else if (26 <= ability && ability <= 27) {
        mod = 8;
    }
    else if (28 <= ability && ability <= 29) {
        mod = 9;
    }
    else if (ability >= 30) {
        mod = 10;
    }
    return mod;
};
