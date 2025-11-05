var is_arranged = 0;

function setArranged() {
  is_arranged = 1;
}

function setNotArranged() {
  is_arranged = 0;
  document.getElementById("select-arranger").value = "";
}

function prettifyText(strval) {
  // Remove extra spaces
  var s = strval.replace(/ +/g, " ");
  s = s.trim();
  // Make the first letter uppercase
  s = s.charAt(0).toUpperCase() + s.substring(1);
  // Escape quotes
  //s = s.replace("'","\\'");
  s = s.replace("'","’");
  s = s.replace('"','\\"');
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
  document.getElementById("new-piece-title").className = "form-control";
  document.getElementById("select-arranger").className = "form-control";
  document.getElementById("select-composer").className = "form-control";
  document.getElementById("new-piece-script").className = "form-control";

  var title        = document.getElementById("new-piece-title").value;
  var subtitle     = document.getElementById("new-piece-subtitle").value;
  var subsubtitle  = document.getElementById("new-piece-subsubtitle").value;
  var dedicated_to = document.getElementById("new-piece-dedicated").value;
  var opus         = document.getElementById("new-piece-opus").value;
  var year         = document.getElementById("new-piece-year").value;
  var composercode = document.getElementById("select-composer").value;
  var instruments  = document.getElementById("new-piece-instrument").value;
  var comment      = document.getElementById("new-piece-comment").value;
  
  var err_msg = "";

  title = prettifyText(title);
  subtitle = prettifyText(subtitle);
  subsubtitle = prettifyText(subsubtitle);
  dedicated_to = prettifyText(dedicated_to);
  opus = prettifyText(opus);
  year = prettifyText(year);
  instruments = prettifyText(instruments);
  comment = prettifyText(comment);

  var arrangercode = "";
  if (is_arranged) {
    arrangercode = document.getElementById("select-arranger").value;
  }
  if (is_arranged && ! arrangercode) {
    err_msg = "Please chose the arranger.";
    document.getElementById("select-arranger").className = "form-control is-invalid";
  }
  if (! composercode) {
    err_msg = "Please chose the composer.";
    document.getElementById("select-composer").className = "form-control is-invalid";
  }
  if (! title) {
    err_msg = "Title cannot be empty!!!";
    document.getElementById("new-piece-title").className = "form-control is-invalid";
  }

  var script_command = "script/new-piece.sh --title " + " \"" + title + "\" "
                     + " --composer-code " + composercode;
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
  if (dedicated_to && dedicated_to != "") {
    script_command += "  --dedicated  \"";
    script_command += dedicated_to;
    script_command += "\"  ";
  }
  if (opus && opus != "") {
    script_command += "  --opus  \"";
    script_command += opus;
    script_command += "\"  ";
  }
  if (year && year != "") {
    script_command += "  --year  \"";
    script_command += year;
    script_command += "\"  ";
  }
  if (is_arranged && arrangercode && arrangercode != "") {
    script_command += "  --arranger-code  \"";
    script_command += arrangercode;
    script_command += "\"  ";
  }
  if (instruments && instruments != "") {
    script_command += "  --instruments  \"";
    script_command += instruments;
    script_command += "\"  ";
  }
  if (comment && comment != "") {
    script_command += "  --comment  \"";
    script_command += comment;
    script_command += "\"  ";
  }

  if (err_msg) {
    document.getElementById("new-piece-script").value = err_msg;
    document.getElementById("new-piece-script").className = "form-control is-invalid";
  }
  else {
    document.getElementById("new-piece-script").value = script_command;
    document.getElementById("new-piece-script").className = "form-control is-valid";
    document.getElementById("new-piece-title").className = "form-control";
    document.getElementById("select-arranger").className = "form-control";
    document.getElementById("select-composer").className = "form-control";
  }

  document.getElementById("new-piece-title").value = title;
  document.getElementById("new-piece-subtitle").value = subtitle;
  document.getElementById("new-piece-subsubtitle").value = subsubtitle;
  document.getElementById("new-piece-dedicated").value = dedicated_to;
  document.getElementById("new-piece-opus").value = opus;
  document.getElementById("new-piece-instrument").value = instruments;
  document.getElementById("new-piece-comment").value = comment;
}

function clearScript() {
  document.getElementById("new-piece-script").value = "";

  document.getElementById("new-piece-title").value = "";
  document.getElementById("new-piece-subtitle").value = "";
  document.getElementById("new-piece-subsubtitle").value = "";
  document.getElementById("new-piece-dedicated").value = "";
  document.getElementById("new-piece-opus").value = "";
  document.getElementById("new-piece-year").value = "";
  document.getElementById("select-composer").value = "";
  document.getElementById("select-arranger").value = "";
  document.getElementById("new-piece-instrument").value = "";
  document.getElementById("new-piece-comment").value = "";
  document.getElementById("check-arranged-piece-radio1").checked = false;
  document.getElementById("check-arranged-piece-radio2").checked = true;

  is_arranged = 0;
  document.getElementById("select-arranger").value = "";
  document.getElementById("select-composer").value = "";

  document.getElementById("new-piece-title").className = "form-control";
  document.getElementById("select-arranger").className = "form-control";
  document.getElementById("select-composer").className = "form-control";

  document.getElementById("new-piece-script").className = "form-control";
}

function copyScript() {
  var copyText = document.getElementById("new-piece-script");
  copyText.select();
  copyText.setSelectionRange(0, 99999);
  navigator.clipboard.writeText(copyText.value);
  alert("Copied to clipboard:\n" + copyText.value);
}

function copyToClipboard() {
  var copyText = document.getElementById("new-piece-script");
  copyText.select();
  copyText.setSelectionRange(0, 99999);
  window.prompt("Copy to clipboard: Ctrl+C, Enter", copyText.value);
}
