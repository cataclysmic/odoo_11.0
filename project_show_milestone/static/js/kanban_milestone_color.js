odoo.define('project_show_milestone.kanban_milestone_color', function(require){
    var core = require('web.core');
    alert(core._t('Hello World'));

    var KanbanRecord = require('web_kanban.KanbanView');
    var Model = require('web.DataModel');

    KanbanRecord.include({
        kanban_getcolor: function (variable) {
            if (this.view.fields_view.model == 'project.task') {
                return (0 % this.view.number_of_color_schemes);
            } else {
                return this._super(variable);
            }
        },
        renderElement: function () {
            this._super();
            if (this.values.ms_color) {
                //Apply the color to the record, if there is one.
                this.$el.find('.oe_kanban_card').css("background-color", this.values.ms_color.value || 'white');
            }
        }
    });

});
