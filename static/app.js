// Confirmación antes de acciones destructivas: <form data-confirm="mensaje">
document.querySelectorAll("form[data-confirm]").forEach(function (form) {
  form.addEventListener("submit", function (event) {
    if (!window.confirm(form.dataset.confirm)) {
      event.preventDefault();
    }
  });
});

// Filtro en vivo de la tabla de inventario (nombre o SKU).
var search = document.getElementById("search");
if (search) {
  var rows = document.querySelectorAll("#products tbody tr");
  var noResults = document.getElementById("no-results");

  search.addEventListener("input", function () {
    var term = search.value.trim().toLowerCase();
    var visible = 0;
    rows.forEach(function (row) {
      var match = row.dataset.search.indexOf(term) !== -1;
      row.hidden = !match;
      if (match) { visible += 1; }
    });
    noResults.hidden = visible !== 0;
  });
}

// Barras de existencias: cada una es proporcional al producto con más stock.
var meters = document.querySelectorAll(".meter[data-stock]");
var max = 0;
meters.forEach(function (m) { max = Math.max(max, Number(m.dataset.stock)); });
meters.forEach(function (m) {
  var pct = max ? (Number(m.dataset.stock) / max) * 100 : 0;
  m.style.setProperty("--w", pct + "%");
});
