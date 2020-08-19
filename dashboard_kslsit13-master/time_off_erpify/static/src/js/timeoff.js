odoo.define('time_off_erpify.timeoff_to_leave', ['hr_holidays.dashboard.view_custo', 'web.core'], function (require) {
    'use strict';

    var core = require('web.core');
    var timeoff = require('hr_holidays.dashboard.view_custo');

    console.log(timeoff)

    var _t = core._t;
    var QWeb = core.qweb;

    timeoff.TimeOffCalendarController.include({
        renderButtons: function ($node) {
            this._super.apply(this, arguments);

            $(QWeb.render('hr_holidays.dashboard.calendar.button', {
                time_off: _t('New Leave Request'),
                request: _t('New Allocation Request'),
            })).appendTo(this.$buttons);

            if ($node) {
                this.$buttons.appendTo($node);
            } else {
                this.$('.o_calendar_buttons').replaceWith(this.$buttons);
            }
        },
    });
});

