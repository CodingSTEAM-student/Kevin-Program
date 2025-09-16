function Enemy() {
  var self = this,
      id,
      value,
      $el,
      x,
      y,
      speed,
      underAttack = false;

  start();

  function start() {
    var options = Enemy.options;
    if (!options) {
      var options = Utils.fillArray(Config.enemyValueMin, Config.enemyValueMax),
          remove = [1,2,4,8,16,32,64,128];
      for (var i=0; i<remove.length; i++) {
        Utils.removeFromArray(options, remove[i]);
      }
      Enemy.options = options;
    }
    value = Utils.pick(options);
    if (Config.enemyValueDebug)
      value = Config.enemyValueDebug;

    var hexatridecimal = Utils.intToBase(value, Config.base);
    id = Enemy.id++;
    $el = $('<div id="enemy-' + id + '" class="enemy" data-nr="' + value + '">' + hexatridecimal + '</div>');
    update();
    $('#game').append($el);

    x = Utils.between(30, screenWidth - 30 - Config.enemyWidth);
    y = -tileSize;

    speed = Enemy.speed;
    if (!Enemy.speed) {
      speed = Enemy.speed = Config.enemySpeed;
    }

    update();
  }

  function update() {
    Utils.cssVendor($el, 'transform', 'translate3d(' + x + 'px, ' + y + 'px, 0)');
  }

  function cycle() {
    y += speed;
  }

  function destroy() {
    $el.remove();
  }

  function reachedBottom() {
    return y >= (Config.ground - Config.enemyHeight);
  }

  function stop() {
    speed = 0;
  }

  function attack() {
    underAttack = true;
    $el.addClass('under-attack');
  }

  function explode() {
    var $explosion = $('<div class="explosion"></div>');
    $explosion.css({left:x+20, top:y+16});
    $('#game').append($explosion);
    setTimeout(function() {
      self.destroy();
    }, 150);
    setTimeout(function() {
      $explosion.remove();
    }, 350);
  }

  this.update = update;
  this.cycle = cycle;
  this.reachedBottom = reachedBottom;
  this.destroy = destroy;
  this.stop = stop;
  this.attack = attack;
  this.explode = explode;

  this.__defineGetter__('id', function() { return id; });
  this.__defineGetter__('x', function() { return x; });
  this.__defineGetter__('y', function() { return y; });
  this.__defineGetter__('speed', function() { return speed; });
  this.__defineGetter__('value', function() { return value; });
  this.__defineGetter__('underAttack', function() { return underAttack; });
}
Enemy.id = 1;
