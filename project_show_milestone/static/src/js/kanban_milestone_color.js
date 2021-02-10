odoo.define('project_show_milestone.kanban_milestone_color', function(require){
    "use strict";

    var KanbanRecord = require('web.KanbanRecord');

    KanbanRecord.include({
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function(){
                if (self.recordData['ms_color'] && self.recordData['ms_color'] != false) {
                    //Apply the color to the record, if there is one.
                    self.$el.find('#mssymb').css("background-color" , self.recordData['ms_color'] || 'green');
                }
            });
        }
    });
});
