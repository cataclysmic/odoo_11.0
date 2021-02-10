odoo.define('html_field_in_tree_view.html_field_in_tree_view', function (require) {
"use strict";
var html_formats = require('web.formats');
var Treeview = require('web.ListView');

Treeview.Column.include({
    _format: function (row_data, options) {
        return html_formats.format_value(row_data[this.id].value, this, options.value_if_empty);
    }
});

});
