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


function createComposerMenu() {
  document.getElementById("select-composer").innerHTML = "";
  var options = ""
  for (var composer of composerlistdata) {
    var composercode = composer["code"];
    var composername = composer["fullname_ascii"];
    options += "<option "  + "value=" + "\""
            + composercode + "\">" + composername + "</option>";
  }
  document.getElementById("select-composer").innerHTML = options;
}

function createArrangerMenu() {
  document.getElementById("select-arranger").innerHTML = "";
  var options = ""
  for (var composer of composerlistdata) {
    var composercode = composer["code"];
    var composername = composer["fullname_ascii"];
    options += "<option "  + "value=" + "\""
            + composercode + "\">" + composername + "</option>";
  }
  document.getElementById("select-arranger").innerHTML = options;
}

function generateScript() {
  var firstname = document.getElementById("new-composer-firstname").value;
  var lastname = document.getElementById("new-composer-lastname").value;
  var fullname = document.getElementById("new-composer-fullname").value;
  var bornyear = document.getElementById("new-composer-bornyear").value;
  var diedyear = document.getElementById("new-composer-diedyear").value;

  var scriptStr = "script/new-composer.sh "
  + " \" " + titleCase(firstname) + " \" " 
  + " \" " + titleCase(lastname)  + " \" "
  + " \""  + titleCase(fullname)  + " \" "
  + bornyear + "  "
  + diedyear + "  "
  + getComposerCode(fullname);
  ;

  document.getElementById("new-composer-script").value = "";
  document.getElementById("new-composer-script").value += scriptStr;

  document.getElementById("new-composer-firstname").value = firstname;
  document.getElementById("new-composer-lastname").value = lastname;
  document.getElementById("new-composer-fullname").value = fullname;
  document.getElementById("new-composer-bornyear").value = bornyear;
  document.getElementById("new-composer-diedyear").value = diedyear;
}
function clearScript() {
  document.getElementById("new-composer-script").value = "";
  document.getElementById("new-composer-firstname").value = "";
  document.getElementById("new-composer-lastname").value = "";
  document.getElementById("new-composer-fullname").value = "";
  document.getElementById("new-composer-bornyear").value = "";
  document.getElementById("new-composer-diedyear").value = "";
}

function copyScript() {
  var copyText = document.getElementById("new-composer-script");
  copyText.select();
  copyText.setSelectionRange(0, 99999);
  navigator.clipboard.writeText(copyText.value);
  alert("Copied to clipboard: " + copyText.value);
}
