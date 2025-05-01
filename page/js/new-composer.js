function titleCase(strval) {
  var splitStr = strval.toLowerCase().split(' ');
  for (var i = 0; i < splitStr.length; i++) {
      splitStr[i] = splitStr[i].charAt(0).toUpperCase() + splitStr[i].substring(1);     
  }
  return splitStr.join(' '); 
}

function getComposerCode(strfullname) {
  var splitStr = strfullname.toLowerCase().split(' ');
  var newSplitStr = [splitStr[splitStr.length-1]];
  for (var i = 0; i < splitStr.length-1; i++) {
    newSplitStr.push(splitStr[i].charAt(0));
  }
  return newSplitStr.join('_');
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
