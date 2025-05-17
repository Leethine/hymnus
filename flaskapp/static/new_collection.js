var has_composer = 0;

function setHasComposer() {
  has_composer = 1;
}

function setHasNoComposer() {
  has_composer = 0;
  document.getElementById("select-composer").value = "";
}

function prettifyText(strval) {
  // Remove extra spaces and escape quotes
  var s = strval.replace(/ +/g, " ");
  s = s.replace("\"","");
  s = s.replace("'","\\'")
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

function generateScript() {
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

  title = prettifyText(title);
  subtitle = prettifyText(subtitle);
  subsubtitle = prettifyText(subsubtitle);
  editor = prettifyText(editor);
  opus = prettifyText(opus);
  volume = prettifyText(volume);
  volume = volume.toUpperCase();
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
    err_msg = "Please select composer or select \"No\".";
    document.getElementById("select-composer").className = "form-control is-invalid";
  }
  // check title
  if (! title) {
    err_msg = "Title cannot be empty!!!";
    document.getElementById("new-collection-title").className = "form-control is-invalid";
  }

  var script_command = "script/new-collection.sh --title " + " \"" + title + " \"";
  if (subtitle && subtitle != "") {
    script_command += "  --subtitle  \"";
    script_command += subtitle;
    script_command += "\"  ";
  }
  if (subsubtitle && subsubtitle != "") {
    script_command += "  --subsubtitle  \"";
    script_command += subsubtitle;
    script_command += "\"  ";
  }
  if (editor && editor != "") {
    script_command += "  --editor  \"";
    script_command += editor;
    script_command += "\"  ";
  }
  if (opus && opus != "") {
    script_command += "  --opus  \"";
    script_command += opus;
    script_command += "\"  ";
  }
  if (volume && volume != "") {
    script_command += "  --volume  \"";
    script_command += volume;
    script_command += "\"  ";
  }
  if (has_composer && composercode != "") {
    script_command += "  --composer-code  \"";
    script_command += composercode;
    script_command += "\"  ";
  }
  if (instruments && instruments != "") {
    script_command += "  --instruments  \"";
    script_command += instruments;
    script_command += "\"  ";
  }
  if (description && description != "") {
    script_command += "  --description  \"";
    script_command += description;
    script_command += "\"  ";
  }

  if (err_msg) {
    document.getElementById("new-collection-script").value = err_msg;
    document.getElementById("new-collection-script").className = "form-control is-invalid";
  }
  else {
    document.getElementById("new-collection-script").value = script_command;
    document.getElementById("new-collection-script").className = "form-control is-valid";
    document.getElementById("new-collection-title").className = "form-control";
    document.getElementById("select-composer").className = "form-control";
  }

  document.getElementById("new-collection-title").value = title;
  document.getElementById("new-collection-subtitle").value = subtitle;
  document.getElementById("new-collection-subsubtitle").value = subsubtitle;
  document.getElementById("new-collection-editor").value = editor;
  document.getElementById("new-collection-opus").value = opus;
  document.getElementById("new-collection-volume").value = volume;
  document.getElementById("new-collection-instrument").value = instruments;
  document.getElementById("new-collection-description").value = description;
}

function clearScript() {
  document.getElementById("new-collection-title").value = "";
  document.getElementById("new-collection-subtitle").value = "";
  document.getElementById("new-collection-subsubtitle").value = "";
  document.getElementById("new-collection-editor").value = "";
  document.getElementById("new-collection-opus").value = "";
  document.getElementById("new-collection-volume").value = "";
  document.getElementById("select-composer").value = "";
  document.getElementById("new-collection-instrument").value = "";
  document.getElementById("new-collection-description").value = "";
  document.getElementById("has-composer-radio1").checked = false;
  document.getElementById("has-composer-radio2").checked = true;
  document.getElementById("select-composer").value = "";
  has_composer = 0;

  document.getElementById("new-collection-title").className = "form-control";
  document.getElementById("select-composer").className = "form-control";

  document.getElementById("new-collection-script").className = "form-control";
  document.getElementById("new-collection-script").value = "";
}

function copyScript() {
  var copyText = document.getElementById("new-collection-script");
  copyText.select();
  copyText.setSelectionRange(0, 99999);
  navigator.clipboard.writeText(copyText.value);
  alert("Copied to clipboard:\n" + copyText.value);
}

function copyToClipboard() {
  var copyText = document.getElementById("new-collection-script");
  copyText.select();
  copyText.setSelectionRange(0, 99999);
  window.prompt("Copy to clipboard: Ctrl+C, Enter", copyText.value);
}
