function disableCheckBoxes() {
  document.getElementById("also-delete-pieces").disabled = true;
  document.getElementById("also-delete-collections").disabled = true;
}

function enableCheckBoxes() {
  document.getElementById("also-delete-pieces").disabled = false;
  document.getElementById("also-delete-collections").disabled = false;
}

function toggleCheckBoxesOnChange() {
  if (document.getElementById("select-action").value === "delete") {
    enableCheckBoxes();
  } else {
    disableCheckBoxes();
  }
}
