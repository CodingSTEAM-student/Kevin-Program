window.Sound = new (function(){
  var that = this,
      _enabled = true,
      _currentMusic,
      _effects = {
        '8bit': { channels: 1, isMusic: true, loop: true, volume: .00001 },
        'explo': { channels: 3, volume: 0.05 },
        'flip1': { channels: 3, volume: 0.05 },
        'flip2': { channels: 3, volume: 0.05 },
        'flip3': { channels: 3, volume: 0.05 },
        'flip4': { channels: 3, volume: 0.05 },
        'flip5': { channels: 3, volume: 0.05 },
        'flip6': { channels: 3, volume: 0.05 },
        'flip7': { channels: 3, volume: 0.05 },
        'flip8': { channels: 3, volume: 0.05 },
        'gameover': { channels: 1 },
        'launch': { channels: 4, volume: .05 }
      };


  function init() {
    if (!Config.sound) return;
    for (var name in _effects) {
      var e = _effects[name],
          extension = '.mp3';
      var url = 'sound/' + name + extension,
          obj = new $bw.audio.fragment(name, url, e.volume, e.isMusic, e.loop, e.channels);
      _effects[name] = obj;
    }
  }

  function play(name, volume) {
    if (!Config.sound) return that;
    if (!_enabled) return that;

    var effect = _effects[name];
    if (effect.isMusic) {
      // if this music track is playing, don't interfere
      if (_currentMusic == name && effect.isPlaying)
        return that;

      _currentMusic = name;
    }

    effect.play(volume);
    effect.isPlaying = true;
    return that;
  }

  function stop(name) {
    if (!Config.sound) return;

    var effect = _effects[name];
    if (effect.isMusic)
      _currentMusic = undefined;

    effect.stop(volume);
    effect.isPlaying = false;
    return that;
  }

  function pauseAll() {
    if (!Config.sound) return;

    for (var name in _effects) {
      _effects[name].stop();
      _effects[name].isPlaying = false;
    }
  }

  function resumeAll() {
    if (!Config.sound) return;

    if (_currentMusic)
      play(_currentMusic);
  }

  this.init = init;

  this.play = play;
  this.stop = stop;

  this.pauseAll = pauseAll;
  this.resumeAll = resumeAll;

  this.__defineGetter__('currentMusic', function() { return _currentMusic; })
})();