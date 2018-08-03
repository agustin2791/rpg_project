interface Attack {
  name: string;
  description: string;
}

class Character {
  name: string;
  hp: number;
  full_hp: number;
  speed: number;
  armor: number;
  strength: number;
  constitution: number;
  intelligence: number;
  wisdom: number;
  charisma: number;
  attack: Attack;
  initiation: number;

  constructor(_name: string, _hp: number, _full_hp: number, _speed: number, _armor: number, _strength: number, _constitution: number, _intelligence: number, wisdom: number, _charisma: number, _attack: Attack, _initiation: number) {
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

  takeDamage(dmg: number): void {
    if (dmg > this.hp) {
      this.hp = 0;
    } else {
      this.hp -= dmg;
    }
  }

  getHealed(heal: number): void {
    if ((heal + this.hp) > this.full_hp) {
      this.hp = this.full_hp;
    } else {
      this.hp += heal;
    }
  }
}
class Enemy extends Character {
  public type: string;

}

function initBattle(data: any[]): any[] {
  var fighters: Character[] = [];
  for (d in data) {
    if (!data[d].enemy) {
      var fighter = new Character(data[d].name, data[d].hp, data[d].full_hp, data[d].speed, data[d].strength, data[d].constitution, data[d].intelligence, data[d].wisdom, data[d].charisma, data[d].attack, data[d].initiation);
    } else if (data[d].enemy) {
      var fighter = new Enemy(data[d].name, data[d].hp, data[d].full_hp, data[d].speed, data[d].strength, data[d].constitution, data[d].intelligence, data[d].wisdom, data[d].charisma, data[d].attack, data[d].initiation);
      fighter.type = data[d].type;
    }
    fighters.push(fighter);
    fighters.sort((a, b) => {
      if (a.initiation > b.initiation) {
        return 1;
      }
      if (a.initiation < b.initiation) {
        return -1;
      }
      return 0;
    })
  }
  return fighters;
}
