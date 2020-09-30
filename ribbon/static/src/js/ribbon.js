odoo.define('ribbon.main',
    function (require) {
     const AbstractAction = require('web.AbstractAction');
     const core = require('web.core');
     const OurAction = AbstractAction.extend({
      template: "hello_world.ClientAction",
      info: "this message comes from the JS",
      msg: "this message developed from the JS",
      });
     core.action_registry.add('ribbon.action', OurAction);}

             );

function myFunction() {
 var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("button1").innerHTML = this.responseText;
    }
  };
  xhttp.open("GET", "ribbon_response?model="+document.getElementById("model").value + "&id="+document.getElementById("id").value, true);
  xhttp.send();

}
function bpChanged() {
 var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("button1").innerHTML = this.responseText;
    }
  };
  xhttp.open("post", "ribbon_response, true);
  xhttp.send(model="+document.getElementById("model").value + "&id="+document.getElementById("id").value);

}