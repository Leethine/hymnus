var is_arranged = 0;

function setArranged() {
  is_arranged = 1;
  document.getElementById("check-is-not-arranged-piece").checked = false;
}

function setNotArranged() {
  is_arranged = 0;
  document.getElementById("select-arranger").value = "";
  document.getElementById("check-is-arranged-piece").checked = false;
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

function autoCorrectInput() {
  document.getElementById("new-piece-title").className  = "form-control";
  document.getElementById("select-arranger").className  = "form-control";
  document.getElementById("select-composer").className  = "form-control";
  document.getElementById("new-piece-script").className = "form-control";

  var title         = document.getElementById("new-piece-title").value;
  var subtitle      = document.getElementById("new-piece-subtitle").value;
  var subsubtitle   = document.getElementById("new-piece-subsubtitle").value;
  var dedicated_to  = document.getElementById("new-piece-dedicated").value;
  var opus          = document.getElementById("new-piece-opus").value;
  var year          = document.getElementById("new-piece-year").value;
  var composercode  = document.getElementById("select-composer").value;
  var arranger_name = document.getElementById("arranger-name").value;
  var instruments   = document.getElementById("new-piece-instrument").value;
  var comment       = document.getElementById("new-piece-comment").value;
  
  var err_msg = "";

  title         = prettifyText(title);
  subtitle      = prettifyText(subtitle);
  subsubtitle   = prettifyText(subsubtitle);
  dedicated_to  = prettifyText(dedicated_to);
  opus          = prettifyText(opus);
  year          = prettifyText(year);
  arranger_name = prettifyText(arranger_name);
  instruments   = prettifyText(instruments);
  comment       = prettifyText(comment);

  var arrangercode = "";
  if (is_arranged) {
    arrangercode = document.getElementById("select-arranger").value;
  }
  if (is_arranged && (! arrangercode && ! arranger_name)) {
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

  if (err_msg) {
    document.getElementById("new-piece-script").value = err_msg;
    document.getElementById("new-piece-script").className = "form-control is-invalid";
  }
  else {
    document.getElementById("new-piece-script").value = "OK";
    document.getElementById("submit-button-successful").className = "btn btn-success";
    document.getElementById("submit-button-successful").disabled = false;
    document.getElementById("new-piece-script").className = "form-control is-valid";
    document.getElementById("new-piece-title").className  = "form-control";
    document.getElementById("select-arranger").className  = "form-control";
    document.getElementById("select-composer").className  = "form-control";
  }

  document.getElementById("new-piece-title").value = title;
  document.getElementById("new-piece-subtitle").value = subtitle;
  document.getElementById("new-piece-subsubtitle").value = subsubtitle;
  document.getElementById("new-piece-dedicated").value = dedicated_to;

  document.getElementById("arranger-name").value = arranger_name;
  document.getElementById("new-piece-opus").value = opus;
  document.getElementById("new-piece-instrument").value = instruments;
  document.getElementById("new-piece-comment").value = comment;
}

function clearInput() {
  document.getElementById("submit-button-successful").class = "btn btn-secondary";
  document.getElementById("submit-button-successful").disabled = true;
  document.getElementById("new-piece-script").value = "";

  document.getElementById("new-piece-title").value = "";
  document.getElementById("new-piece-subtitle").value = "";
  document.getElementById("new-piece-subsubtitle").value = "";
  document.getElementById("new-piece-dedicated").value = "";
  document.getElementById("new-piece-opus").value = "";
  document.getElementById("new-piece-year").value = "";
  document.getElementById("select-composer").value = "";
  document.getElementById("select-arranger").value = "";
  document.getElementById("arranger-name").value = "";
  document.getElementById("new-piece-instrument").value = "";
  document.getElementById("new-piece-comment").value = "";
  document.getElementById("check-is-arranged-piece").checked = false;
  document.getElementById("check-is-not-arranged-piece").checked = true;

  is_arranged = 0;
  document.getElementById("select-arranger").value = "";
  document.getElementById("select-composer").value = "";

  document.getElementById("new-piece-title").className = "form-control";
  document.getElementById("select-arranger").className = "form-control";
  document.getElementById("select-composer").className = "form-control";

  document.getElementById("new-piece-script").className = "form-control";
}
