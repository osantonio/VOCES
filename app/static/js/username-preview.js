document.addEventListener('DOMContentLoaded', function () {
  var input = document.getElementById('username');
  var preview = document.getElementById('username-url-preview');
  if (!input || !preview) return;
  var base = window.location.origin + '/usuarios/';
  function update() {
    var u = (input.value || '').trim();
    preview.textContent = base + u;
  }
  update();
  input.addEventListener('input', update);
});
