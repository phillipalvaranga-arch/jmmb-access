(function () {
  'use strict';

  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
      navigator.serviceWorker.register('./sw.js').catch(function () {});
    });
  }

  var live = document.getElementById('hoursLive');
  if (!live) return;

  function partsInZone(date, zone) {
    var fmt = new Intl.DateTimeFormat('en-US', {
      timeZone: zone,
      weekday: 'short',
      hour: 'numeric',
      minute: 'numeric',
      hour12: false
    });
    var out = { weekday: '', hour: 0, minute: 0 };
    fmt.formatToParts(date).forEach(function (p) {
      if (p.type === 'weekday') out.weekday = p.value;
      if (p.type === 'hour') out.hour = parseInt(p.value, 10) % 24;
      if (p.type === 'minute') out.minute = parseInt(p.value, 10);
    });
    return out;
  }

  function prettyTime(date, zone) {
    return new Intl.DateTimeFormat('en-US', {
      timeZone: zone,
      weekday: 'long',
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    }).format(date);
  }

  function isOpenJamaica(date) {
    var p = partsInZone(date, 'America/Jamaica');
    var mins = p.hour * 60 + p.minute;
    var open = 8 * 60;
    var close = p.weekday === 'Sun' ? 17 * 60 : 21 * 60;
    return mins >= open && mins < close;
  }

  function render() {
    var now = new Date();
    var open = isOpenJamaica(now);
    var ja = prettyTime(now, 'America/Jamaica');
    var ct = prettyTime(now, 'America/Chicago');
    live.hidden = false;
    live.className = 'live ' + (open ? 'open' : 'closed');
    live.textContent = (open
      ? 'Client Care is open now.'
      : 'Client Care is closed now.') +
      ' Jamaica time: ' + ja + '. Central Time: ' + ct + '.';
  }

  render();
  setInterval(render, 60000);
})();
