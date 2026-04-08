var has_composer = 0;

function toggleComposerList() {
  if (has_composer == 0) {
    has_composer = 1;
  }
  else {
    has_composer = 0;
  }
  if (! has_composer) {
    document.getElementById("select-composer").value = "";
  }
}

function prettifyText(strval) {
  // Remove extra spaces and escape quotes
  var s = strval.replace(/ +/g, " ");
  //s = s.replace("'","\\'");
  s = s.replace("'","’");
  s = s.replace('"','\\"');
  s = s.trim();
  // Make the first letter uppercase
  s = s.charAt(0).toUpperCase() + s.substring(1);
  return s; 
}

function createDropDownMenu(elem_id) {
  document.getElementById(elem_id).innerHTML = "";
  var options = ""

  for (var composer of COMPOSERLISTDATA) {
    if (composer.length == 2) {
      var composercode = composer[0];
      var composername = composer[1];
      options += "<option "  + "value=" + "\""
              + composercode + "\">" + composername + "</option>";
    }
  }

  document.getElementById(elem_id).innerHTML = options;
}

function validateInput() {
  document.getElementById("new-collection-script").className = "form-control";
  document.getElementById("new-collection-title").className = "form-control";
  document.getElementById("select-composer").className = "form-control";

  var title        = document.getElementById("new-collection-title").value;
  var subtitle     = document.getElementById("new-collection-subtitle").value;
  var subsubtitle  = document.getElementById("new-collection-subsubtitle").value;
  var editor       = document.getElementById("new-collection-editor").value;
  var opus         = document.getElementById("new-collection-opus").value;
  var volume       = document.getElementById("new-collection-volume").value;
  var instruments  = document.getElementById("new-collection-instrument").value;
  var description  = document.getElementById("new-collection-description").value;

  var err_msg = "";

  title       = prettifyText(title);
  subtitle    = prettifyText(subtitle);
  subsubtitle = prettifyText(subsubtitle);
  editor      = prettifyText(editor);
  opus        = prettifyText(opus);
  volume      = prettifyText(volume);
  volume      = volume.toUpperCase();
  instruments = prettifyText(instruments);
  description = prettifyText(description);

  // check composer
  if (has_composer) {
    composercode = document.getElementById("select-composer").value;
  }
  else {
    composercode = "zzz_unknown";
  }
  if (has_composer && ! composercode) {
    err_msg = "Please select composer or uncheck the \"Yes\" box.";
    document.getElementById("select-composer").className = "form-control is-invalid";
  }
  // check title
  if (! title) {
    err_msg = "Title cannot be empty!!!";
    document.getElementById("new-collection-title").className = "form-control is-invalid";
  }

  if (err_msg) {
    document.getElementById("new-collection-script").value = err_msg;
    document.getElementById("new-collection-script").className = "form-control is-invalid";
  }
  else {
    document.getElementById("new-collection-script").value     = "OK";
    document.getElementById("new-collection-script").className = "form-control is-valid";
    document.getElementById("new-collection-title").className  = "form-control";
    document.getElementById("select-composer").className       = "form-control";
    document.getElementById("button-submit-form").className    = "btn btn-success";
    document.getElementById("button-submit-form").disabled     = false;
  }

  document.getElementById("new-collection-title").value       = title;
  document.getElementById("new-collection-subtitle").value    = subtitle;
  document.getElementById("new-collection-subsubtitle").value = subsubtitle;
  document.getElementById("new-collection-editor").value      = editor;
  document.getElementById("new-collection-opus").value        = opus;
  document.getElementById("new-collection-volume").value      = volume;
  document.getElementById("new-collection-instrument").value  = instruments;
  document.getElementById("new-collection-description").value = description;
}

function clearInput() {
  document.getElementById("new-collection-title").value       = "";
  document.getElementById("new-collection-subtitle").value    = "";
  document.getElementById("new-collection-subsubtitle").value = "";
  document.getElementById("new-collection-editor").value      = "";
  document.getElementById("new-collection-opus").value        = "";
  document.getElementById("new-collection-volume").value      = "";
  document.getElementById("select-composer").value            = "";
  document.getElementById("new-collection-instrument").value  = "";
  document.getElementById("new-collection-description").value = "";
  document.getElementById("collection-has-composer").checked = false;

  has_composer = 0;

  document.getElementById("new-collection-title").className = "form-control";
  document.getElementById("select-composer").className = "form-control";

  document.getElementById("new-collection-script").className = "form-control";
  document.getElementById("new-collection-script").value = "";
}

