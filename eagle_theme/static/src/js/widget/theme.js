eagle.define('website.theme_custom', function (require) {
'use strict';

var Theme = require('website.theme');
var ColorpickerDialog = require('web.colorpicker');

Theme.include({
    xmlDependencies: (Theme.prototype.xmlDependencies || [])
        .concat(['/eagle_theme/static/src/xml/website_editor.xml']),
    events: {
        'change [data-xmlid], [data-enable], [data-disable]': '_onChange',
        'click .checked [data-xmlid], .checked [data-enable], .checked [data-disable]': '_onChange',
        'click .o_theme_customize_color': '_onColorClick',
    },
    _onColorClick: function (ev) {

        var self = this;
        var $color = $(ev.currentTarget);
        var colorName = $color.data('color');
        console.log("before  $color",colorName);
        var colorType = $color.data('colorType');
        var colorpicker = new ColorpickerDialog(this, {
            defaultColor: $color.find('.o_color_preview').css('background-color'),
        });
        colorpicker.on('colorpicker:saved', this, function (ev) {
            ev.stopPropagation();
            // TODO improve to be more efficient
                var colors = {};
                colors[colorName] = ev.data.cssColor;
                if (colorName === 'alpha') {
                    colors['beta'] = 'null';
                    colors['gamma'] = 'null';
                    colors['delta'] = 'null';
                    colors['epsilon'] = 'null';
                }
                _.each(colors, function (colorValue, colorName) {
                console.log('colorName',colorName);
                if(colorName === 'eagleshop_primary'){
		            var updatedFileContent = "$theme:" + colorValue + ";";
		            var baseURL = '/eagle_theme/static/src/scss/colors/color_picker.scss';
                     		self._rpc({
								route: '/web_editor/get_assets_editor_resources',
								params: {
								    key: 'website.layout',
								    get_views: false,
								    get_scss: true,
								    bundles: false,
								    bundles_restriction: [],
								},
							}).then(function (data){
                                var updatedFileContent = "$theme:" + colorValue + ";";

							    self._rpc({
								    route: '/web_editor/save_scss',
								    params: {
								        url: '/eagle_theme/static/src/scss/colors/color_picker.scss',
								        bundle_xmlid: 'web.assets_frontend',
                                        content: updatedFileContent,
								    },
								}).then(function (d){
								window.location.reload();
								});
							self.$('#' + $color.closest('.o_theme_customize_color_previews').data('depends')).click();
                    	});

	            }
                // if(colorName === 'eagleshop_secondary'){
                //     var updatedFileContent = "$theme_secondary:" + colorValue + ";";
                //     var baseURL = '/eagle_theme/static/src/scss/colors/color_picker.scss';
                //             self._rpc({
                //                 route: '/web_editor/get_assets_editor_resources',
                //                 params: {
                //                     key: 'website.layout',
                //                     get_views: false,
                //                     get_scss: true,
                //                     bundles: false,
                //                     bundles_restriction: [],
                //                 },
                //             }).then(function (data){
                //                 var updatedFileContent = "$theme_secondary:" + colorValue + ";";

                //                 self._rpc({
                //                     route: '/web_editor/save_scss',
                //                     params: {
                //                         url: '/eagle_theme/static/src/scss/colors/color_picker.scss',
                //                         bundle_xmlid: 'web.assets_frontend',
                //                         content: updatedFileContent,
                //                     },
                //                 }).then(function (d){
                //                 window.location.reload();
                //                 });
                //             self.$('#' + $color.closest('.o_theme_customize_color_previews').data('depends')).click();
                //         });

                // }
                if(colorName === 'eagleshop_secondary'){
                    var updatedFileContent = "$theme2nd:" + colorValue + ";";
                    var baseURL = '/eagle_theme/static/src/scss/colors/color_picker_sec.scss';
                            self._rpc({
                                route: '/web_editor/get_assets_editor_resources',
                                params: {
                                    key: 'website.layout',
                                    get_views: false,
                                    get_scss: true,
                                    bundles: false,
                                    bundles_restriction: [],
                                },
                            }).then(function (data){
                                var updatedFileContent = "$theme2nd:" + colorValue + ";";

                                self._rpc({
                                    route: '/web_editor/save_secondary_scss',
                                    params: {
                                        url: '/eagle_theme/static/src/scss/colors/color_picker_sec.scss',
                                        bundle_xmlid: 'web.assets_frontend',
                                        content: updatedFileContent,
                                    },
                                }).then(function (d){
                                window.location.reload();
                                });
                            self.$('#' + $color.closest('.o_theme_customize_color_previews').data('depends')).click();
                        });

                }
		            
                })

        });
        colorpicker.open();
    },
});

});								
