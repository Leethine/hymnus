if (!ascii_converted) {
  var ascii={};
  ascii.char_map = {
  "é":"e",
  "ä":"ae",
  "œ":"oe",
  "ö":"o",
  "è":"e",
  "ë":"e",
  "ÿ":"y",
  "í":"i",
  "ř":"r",
  "á":"a",
  "ç":"c"
  }
  String.prototype.to_ascii=function(){return this.replace(/[^A-Za-z0-9\[\] ]/g,function(a){return ascii.char_map[a]||a})};

  for(let i = 0; i < composerlistdata.length; i++) {
    composerlistdata[i]["fullname_ascii"] = composerlistdata[i]["fullname_ascii"].toLowerCase().to_ascii();
  }
  ascii_converted = 1;
}

var valueEl = document.getElementById("filter-value");
function updateFilter() {
  valueEl.disabled = false;
  table.setFilter("fullname_ascii", "like", valueEl.value);
}
document.getElementById("filter-value").addEventListener("keyup", updateFilter);

var table = new Tabulator("#composer-table", {
  data: composerlistdata,
  layout: "fitColumns",
  pagination: "local",
  paginationSize: 10,
  paginationSizeSelector: [10, 20, 30, 50],
  movableColumns: true,
  paginationCounter: "rows",
  columns: [
      {title:"Full Name", field:"knownas_name", sorter:"string", headerSort:false},
      {title:"Full Name ascii", field:"fullname_ascii", headerSort:false, visible:false},
      {title:"Name", field:"lastname", sorter:"string"},
      {title:"Born", field:"bornyear", hozAlign:"left", width:"100"},
      {title:"Died", field:"diedyear", hozAlign:"left", width:"100"},
  ],
});
