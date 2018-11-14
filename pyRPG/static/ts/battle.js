var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var Character = /** @class */ (function () {
    function Character(_name, _hp, _full_hp, _speed, _armor, _strength, _constitution, _intelligence, wisdom, _charisma, _attack, _initiation) {
        this.name = _name;
        this.hp = _hp;
        this.full_hp = _full_hp;
        this.speed = _speed;
        this.armor = _armor;
        this.strength = _strength;
        this.constitution = _constitution;
        this.intelligence = _intelligence;
        this.wisdom = _wisdom;
        this.charisma = _charisma;
        this.attack = _attack;
        this.initiation = _initiation;
    }
    Character.prototype.takeDamage = function (dmg) {
        if (dmg > this.hp) {
            this.hp = 0;
        }
        else {
            this.hp -= dmg;
        }
    };
    Character.prototype.getHealed = function (heal) {
        if ((heal + this.hp) > this.full_hp) {
            this.hp = this.full_hp;
        }
        else {
            this.hp += heal;
        }
    };
    return Character;
}());
var Enemy = /** @class */ (function (_super) {
    __extends(Enemy, _super);
    function Enemy() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return Enemy;
}(Character));
function initBattle(data) {
    var fighters = [];
    for (d in data) {
        if (!data[d].enemy) {
            var fighter = new Character(data[d].name, data[d].hp, data[d].full_hp, data[d].speed, data[d].strength, data[d].constitution, data[d].intelligence, data[d].wisdom, data[d].charisma, data[d].attack, data[d].initiation);
        }
        else if (data[d].enemy) {
            var fighter = new Enemy(data[d].name, data[d].hp, data[d].full_hp, data[d].speed, data[d].strength, data[d].constitution, data[d].intelligence, data[d].wisdom, data[d].charisma, data[d].attack, data[d].initiation);
            fighter.type = data[d].type;
        }
        fighters.push(fighter);
        fighters.sort(function (a, b) {
            if (a.initiation > b.initiation) {
                return 1;
            }
            if (a.initiation < b.initiation) {
                return -1;
            }
            return 0;
        });
    }
    return fighters;
}
