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

function prettifyNames(strval) {
  // Uppercase the first letter of each word
  var s = strval.replace(/ +/g, " ");
  s = s.trim();
  var splitStr = s.toLowerCase().split(' ');
  var newSplitStr = [];
  for (var elem of splitStr) {
    // Ignore spaces and empty string
    if (elem && elem != "") {
      var cleanstr = elem.replace(/ /g,'');
      cleanstr = cleanstr.charAt(0).toUpperCase() + cleanstr.substring(1);
      newSplitStr.push(cleanstr);
    }
  }
  return newSplitStr.join(' '); 
}

function getComposerCode(strfullname) {
  var s = strfullname.toLowerCase().to_ascii();
  var splitStr = s.split(' ');
  var newSplitStr = [];
  for (var elem of splitStr) {
    if (elem && elem != "") {
      newSplitStr.push(elem);
    }
  }
  var familyname = newSplitStr[newSplitStr.length-1];
  var firstnames = [];
  for (var elem of newSplitStr.slice(0,-1)) {
    firstnames.push(elem.charAt(0));
  }
  return familyname + "_" + firstnames.join('_');
}

function generateScript() {
  var err_msg = "";
  var firstname = document.getElementById("new-composer-firstname").value;
  var lastname = document.getElementById("new-composer-lastname").value;
  var fullname = document.getElementById("new-composer-fullname").value;
  var bornyear = document.getElementById("new-composer-bornyear").value;
  var diedyear = document.getElementById("new-composer-diedyear").value;

  // Check and prettify name
  if (fullname) {
    fullname = prettifyNames(fullname);
    firstname = prettifyNames(firstname);
    lastname = prettifyNames(lastname);
    firstname = autoCompleteFirstName(firstname, fullname);
    lastname = autoCompleteLastName(lastname, fullname);
  }
  else {
    err_msg = "Name cannot be empty!"
  }
  
  // Check year
  var MIN_YEAR = 0;
  var MAX_YEAR = 3333;
  var bornyear_int = -9999;
  var diedyear_int = -9999;
  bornyear = bornyear.replace(/ /g,'');
  diedyear = diedyear.replace(/ /g,'');
  if (parseInt(bornyear)) {
    bornyear_int = parseInt(bornyear);
  }
  if (parseInt(diedyear)) {
    diedyear_int = parseInt(diedyear);
  }

  if (bornyear_int > MIN_YEAR && bornyear_int < MAX_YEAR &&
    diedyear_int > MIN_YEAR && diedyear_int < MAX_YEAR) {
  }
  else if (bornyear_int > MIN_YEAR && bornyear_int < MAX_YEAR && diedyear == "?") {
    diedyear_int = -1;
  }
  else if (diedyear_int > MIN_YEAR && diedyear_int < MAX_YEAR && bornyear == "?") {
    bornyear_int = -1;
  }
  else {
    err_msg = "Invalid BornYear/DiedYear";
  }
  if (bornyear == "?") {
    bornyear = "-1";
  }
  if (diedyear == "?") {
    diedyear = "-1";
  }

  var script = "script/new-composer.sh "
  + " \"" + firstname + "\" " 
  + " \"" + lastname  + "\" "
  + " \""  + fullname  + "\" "
  + bornyear + "  "
  + diedyear + "  "
  + getComposerCode(fullname);

  // Persist input text
  document.getElementById("new-composer-firstname").value = firstname;
  document.getElementById("new-composer-lastname").value = lastname;
  document.getElementById("new-composer-fullname").value = fullname;
  document.getElementById("new-composer-bornyear").value = bornyear;
  document.getElementById("new-composer-diedyear").value = diedyear;

  if (err_msg) {
    document.getElementById("new-composer-script").className = "form-control is-invalid";
    document.getElementById("new-composer-script").value = err_msg;
  }
  else {
    document.getElementById("new-composer-script").className = "form-control is-valid";
    document.getElementById("new-composer-script").value = script;
  }
}

function autoCompleteFirstName(firstname, fullname) {
  if (firstname) {
  }
  else {
    var splitStr = fullname.split(' ');
    if (splitStr.length > 1) {
      return splitStr.slice(0, -1).join(' ');
    }
  }
  return firstname;
}

function autoCompleteLastName(lastname, fullname) {
  if (lastname) {
  }
  else {
    var splitStr = fullname.split(' ');
    if (splitStr.length >= 1) {
      return splitStr[splitStr.length-1];
    }
  }
  return lastname;
}

function checkInput(first, last, full, born, died) {
  return 1;
}

function clearScript() {
  document.getElementById("new-composer-script").value = "";
  document.getElementById("new-composer-firstname").value = "";
  document.getElementById("new-composer-lastname").value = "";
  document.getElementById("new-composer-fullname").value = "";
  document.getElementById("new-composer-bornyear").value = "";
  document.getElementById("new-composer-diedyear").value = "";

  document.getElementById("new-composer-script").className = "form-control";
}

function copyScript() {
  var copyText = document.getElementById("new-composer-script");
  copyText.select();
  copyText.setSelectionRange(0, 99999);
  navigator.clipboard.writeText(copyText.value);
  alert("Copied to clipboard:\n" + copyText.value);
}
