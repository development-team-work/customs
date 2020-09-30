//this is a demo file to learn javascript for odoo
odoo.define('<Module_name>.main',
    function (require) {
     const AbstractAction = require('web.AbstractAction');
     const core = require('web.core');
     const OurAction = AbstractAction.extend({
      template: "hello_world.ClientAction",
      info: "this message comes from the JS",
      msg: "this message developed from the JS",
      });
             core.action_registry.add('ribbon.action', OurAction);});