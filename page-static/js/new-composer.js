function prettifyNames(strval) {
  // Uppercase the first letter of each word
  var splitStr = strval.toLowerCase().split(' ');
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
  var splitStr = strfullname.toLowerCase().split(' ');
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
  var firstname = document.getElementById("new-composer-firstname").value;
  var lastname = document.getElementById("new-composer-lastname").value;
  var fullname = document.getElementById("new-composer-fullname").value;
  var bornyear = document.getElementById("new-composer-bornyear").value;
  var diedyear = document.getElementById("new-composer-diedyear").value;

  var scriptStr = "script/new-composer.sh "
  + " \"" + prettifyNames(firstname) + "\" " 
  + " \"" + prettifyNames(lastname)  + "\" "
  + " \""  + prettifyNames(fullname)  + "\" "
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
  alert("Copied to clipboard:\n" + copyText.value);
}
