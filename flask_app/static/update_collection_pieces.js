function toggleInputField() {
  action = document.getElementById("select-action").value;

  if (action === "add-to") {
    document.getElementById("list-of-pieces-add").disabled = false;
    document.getElementById("list-of-pieces-remove").disabled = true;
  } else if (action === "remove-from") {
    document.getElementById("list-of-pieces-add").disabled = true;
    document.getElementById("list-of-pieces-remove").disabled = false;
  }
}
