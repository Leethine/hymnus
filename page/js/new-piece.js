var is_arranged = 0;

function setArranged() {
  is_arranged = 1;
}

function setNotArranged() {
  is_arranged = 0;
}

function createDropDownMenu(elem_id) {
  document.getElementById(elem_id).innerHTML = "";
  var options = ""
  var newlist_composer = [];

  for (var composer of composerlistdata) {
    var composercode = composer["code"];
    var composername = composer["fullname_ascii"];
    var namelist = composername.split(' ');
    var lastname = namelist[namelist.length - 1] + ", ";
    var firstnames = "";
    for (var i = 0; i < namelist.length - 1; i++) {
      firstnames += namelist[i] + " ";
    }
    newlist_composer.push(lastname + firstnames + "|" + composercode);
  }

  newlist_composer.sort();
  for (var composer of newlist_composer) {
    var composersplit = composer.split('|');
    var composercode = composersplit[1];
    var composername = composersplit[0];
    options += "<option "  + "value=" + "\""
            + composercode + "\">" + composername + "</option>";
  }

  document.getElementById(elem_id).innerHTML = options;
}

function generateScript() {
  var title        = document.getElementById("new-piece-title").value;
  var subtitle     = document.getElementById("new-piece-subtitle").value;
  var subsubtitle  = document.getElementById("new-piece-subsubtitle").value;
  var dedicated_to  = document.getElementById("new-piece-dedicated").value;
  var opus         = document.getElementById("new-piece-opus").value;
  var composercode = document.getElementById("select-composer").value;
  var arrangercode = "";
  if (is_arranged) {
    arrangercode = document.getElementById("select-arranger").value;
  }
  var instruments  = document.getElementById("new-piece-instrument").value;
  var comment      = document.getElementById("new-piece-comment").value;

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

  document.getElementById("new-piece-script").value = script_command;
}

function clearScript() {
  document.getElementById("new-piece-title").value = "";
  document.getElementById("new-piece-subtitle").value = "";
  document.getElementById("new-piece-subsubtitle").value = "";
  document.getElementById("new-piece-dedicated").value = "";
  document.getElementById("new-piece-opus").value = "";
  document.getElementById("select-composer").value = "";
  document.getElementById("select-arranger").value = "";
  document.getElementById("new-piece-instrument").value = "";
  document.getElementById("new-piece-comment").value = "";
  document.getElementById("check-arranged-piece-radio1").checked = false;
  document.getElementById("check-arranged-piece-radio2").checked = true;
  is_arranged = 0;
}

function copyScript() {
  var copyText = document.getElementById("new-piece-script");
  copyText.select();
  copyText.setSelectionRange(0, 99999);
  navigator.clipboard.writeText(copyText.value);
  alert("Copied to clipboard:\n" + copyText.value);
}
