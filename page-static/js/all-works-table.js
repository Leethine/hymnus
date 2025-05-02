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

  for(let i = 0; i < piecelistdata.length; i++) {
    piecelistdata[i]["title_ascii"] = piecelistdata[i]["title_ascii"].toLowerCase().to_ascii();
  }
  ascii_converted = 1;
}

var valueEl = document.getElementById("filter-value");
function updateFilter() {
  valueEl.disabled = false;
  table.setFilter("title_ascii", "like", valueEl.value);
}
document.getElementById("filter-value").addEventListener("keyup", updateFilter);

var table = new Tabulator("#all-works-table", {
  data: piecelistdata,
  layout: "fitColumns",
  pagination: "local",
  paginationSize: 20,
  paginationSizeSelector: [20, 50, 100],
  movableColumns: true,
  paginationCounter: "rows",
  columns: [
      {title:"Title", field:"title", sorter:"string", headerSort:true},
      {title:"Title ascii", field:"title_ascii", sorter:"string", headerSort:false, visible:false},
      {title:"Opus", field:"opus", hozAlign:"left", width:"100"},
      {title:"Composer", field:"composer_code", sorter:"string", hozAlign:"left", width:"100"},
      {title:"Path", field:"folder_hash", sorter:"string", hozAlign:"left", width:"100"},
  ],
});
