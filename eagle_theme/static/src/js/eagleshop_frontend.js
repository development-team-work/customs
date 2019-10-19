eagle.define('eagle_theme.eagleshop_frontend_js', function(require) {
    'use strict';

    var animation = require('website.content.snippets.animation');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var _t = core._t;

    function getTimeRemaining(formated_date) {
        var t = Date.parse(formated_date) - Date.parse(new Date());
        var seconds = Math.floor((t / 1000) % 60);
        var minutes = Math.floor((t / 1000 / 60) % 60);
        var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
        var days = Math.floor(t / (1000 * 60 * 60 * 24));
        return {
            'total': t,
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds
        };
    }

    function initializeClock(id, endtime) {
        var clock = $(id)
        var test = getTimeRemaining(endtime);
        if (test.total > 0) {
            var timeinterval = setInterval(function() {
                var t = getTimeRemaining(endtime);
                clock.find('.days').text(t.days);
                clock.find('.hours').text(t.hours);
                clock.find('.minutes').text(t.minutes);
                clock.find('.seconds').text(t.seconds);
                if (t.total <= 0) {
                    clearInterval(timeinterval);
                }
            }, 1000);

        }
    }

    animation.registry.eagle_theme_blog_custom_snippet = animation.Class.extend({
        selector: ".eagleshop_blog_slider",
        start: function() {
            var self = this;
            if (this.editableMode) {
                var $blog_snip = $('#wrapwrap').find('#eagle_theme_custom_blog_snippet');
                var blog_name = _t("Blog Slider")
                
                _.each($blog_snip, function (single){
                    $(single).empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="fancy">' + blog_name + '</h3>\
                                                    </div>\
                                                </div>')
                });
            }
            if (!this.editableMode) {
                var slider_type = self.$target.attr('data-blog-slider-type');
                $.get("/eagle_theme/blog_get_dynamic_slider", {
                    'slider-type': self.$target.attr('data-blog-slider-type') || '',
                }).then(function(data) {
                    if (data) {
                        self.$target.empty();
                        self.$target.append(data);
                        $(".eagleshop_blog_slider").removeClass('o_hidden');
                        ajax.jsonRpc('/eagle_theme/blog_image_effect_config', 'call', {
                            'slider_type': slider_type
                        }).done(function(res) {
                            $('div#' + res.s_id).owlCarousel({
                                margin: 10,
                                responsiveClass: true,
                                items: res.counts,
                                loop: true,
                                autoplay: res.auto_rotate,
                                autoplayTimeout:res.auto_play_time,
                                autoplayHoverPause:true,
                                navigation: true,
                                responsive: {
                                    0: {
                                        items: 1,
                                    },
                                    420: {
                                        items: 2,
                                    },
                                    768: {
                                        items: res.counts,
                                    },
                                    1000: {
                                        items: res.counts,
                                    },
                                    1500: {
                                        items: res.counts,
                                    }
                                },
                            });
                        });
                    }
                });
            }
        }
    });

    animation.registry.s_eagle_theme_client_slider_snippet = animation.Class.extend({
        selector: ".our-client-slider",
        start: function() {
            var self = this;
            if (this.editableMode) {
                var $client_slider = $('#wrapwrap').find('#eagle_theme_custom_client_slider');
                var client_name = _t("Client Slider")

                _.each($client_slider, function (single){
                    $(single).empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="fancy">' + client_name + '</h3>\
                                                    </div>\
                                                </div>')
                });
            }
            if (!this.editableMode) {
                $.get("/eagle_theme/get_clients_dynamically_slider", {}).done(function(data) {
                    if (data) {
                        self.$target.empty();
                        self.$target.append(data);
                        $('div#eagleshop-client-slider').owlCarousel({
                            loop: false,
                            margin: 10,
                            responsiveClass: true,
                            nav: false,
                            responsive: {
                                0: {
                                    items: 1,
                                },
                                420: {
                                    items: 2,
                                },
                                768: {
                                    items: 4,
                                },
                                1000: {
                                    items: 6,
                                },
                                1500: {
                                    items: 6,
                                }
                            }
                        });
                    }
                });
            }
        }
    });

    animation.registry.eagle_theme_multi_cat_custom_snippet = animation.Class.extend({
        selector: ".oe_multi_category_slider",
        start: function() {
            var self = this;
            if (this.editableMode) {
                var $cat_custom = $('#wrapwrap').find('#eagle_theme_custom_multi_product_tab_slider');
                var name = _t("Multi Product Tabs Slider")

                _.each($cat_custom, function (single){
                    $(single).empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="fancy">' + name + '</h3>\
                                                    </div>\
                                                </div>')
                });
            }
            if (!this.editableMode) {
                var slider_type = self.$target.attr('data-multi-cat-slider-type');
                $.get("/eagle_theme/product_multi_get_dynamic_slider", {
                    'slider-type': slider_type || '',
                }).then(function(data) {
                    if (data) {
                        self.$target.empty();
                        self.$target.append(data);
                        $(".oe_multi_category_slider").removeClass('o_hidden');
                    }
                });
            }
        }
    });

    animation.registry.eagle_theme_coming_soon_mode_one = animation.Class.extend({
        selector: ".biztech_coming_soon_mode_one",
        start: function() {
            var self = this;
            if (this.editableMode) {
                var $comming_soon_1 = $('#wrapwrap').find('.biztech_coming_soon_mode_one');
                var comming_soon_1_name = _t("Coming Soon Feature 1")
                
                _.each($comming_soon_1, function (single){
                    $(single).empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="fancy">' + comming_soon_1_name + '</h3>\
                                                    </div>\
                                                </div>')
                });
            }
            if (!this.editableMode) {
                var formated_date
                var exit_date = self.$target.attr('data-blog-updated-date-time')
                $.get("/biztech_comming_soon/soon_data", {}).then(function(data) {
                    self.$target.empty().append(data);
                })

                var $divcount = self.$target
                var x = initializeClock($divcount, exit_date)

            }
        }
    });

    animation.registry.eagle_theme_coming_soon_mode_two = animation.Class.extend({
        selector: ".biztech_coming_soon_mode_two",
        start: function() {
            var self = this;
             if (this.editableMode) {
                var $comming_soon_2 = $('#wrapwrap').find('.biztech_coming_soon_mode_two');
                var comming_soon_2_name = _t("Coming Soon Feature 2")
                
                _.each($comming_soon_2, function (single){
                    $(single).empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="fancy">' + comming_soon_2_name + '</h3>\
                                                    </div>\
                                                </div>')
                });
            }
            if (!this.editableMode) {
                var formated_date
                var maintwo_date = self.$target.attr('data-cm2-updated-date-time')
                $.get("/biztech_comming_soon_two/two_soon_data", {}).then(function(data) {
                    self.$target.empty().append(data);
                })


                var $divcount_maintwo = self.$target
                var main2 = initializeClock($divcount_maintwo, maintwo_date)

            }
        }
    });

    animation.registry.eagle_theme_category_slider = animation.Class.extend({
        selector: ".oe_cat_slider",
        start: function() {
            var self = this;
            if (this.editableMode) {
                var $cate_slider = $('#wrapwrap').find('#eagle_theme_custom_category_slider');
                var cat_name = _t("Category Slider")
                _.each($cate_slider, function (single){
                    $(single).empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="fancy">' + cat_name + '</h3>\
                                                    </div>\
                                                </div>')
                });
            }
            if (!this.editableMode) {
                var slider_id = self.$target.attr('data-cat-slider-id');
                $.get("/eagle_theme/category_get_dynamic_slider", {
                    'slider-id': self.$target.attr('data-cat-slider-id') || '',
                }).then(function(data) {
                    if (data) {
                        self.$target.empty();
                        self.$target.append(data);
                        $(".oe_cat_slider").removeClass('o_hidden');

                        ajax.jsonRpc('/eagle_theme/category_image_effect_config', 'call', {
                            'slider_id': slider_id
                        }).done(function(res) {
                            $('div#' + res.s_id).owlCarousel({
                                margin: 10,
                                responsiveClass: true,
                                items: res.counts,
                                loop: true,
                                autoplay: res.auto_rotate,
                                autoplayTimeout:res.auto_play_time,
                                autoplayHoverPause:true,
                                responsive: {
                                    0: {
                                        items: 1,
                                    },
                                    420: {
                                        items: 2,
                                    },
                                    768: {
                                        items: 3,
                                    },
                                    1000: {
                                        items: res.counts,
                                    },
                                    1500: {
                                        items: res.counts,
                                    },
                                },
                            });
                        });
                    }
                });
            }
        }
    });

    animation.registry.eagle_theme_product_slider = animation.Class.extend({

        selector: ".oe_prod_slider",
        start: function() {
            var self = this;
            if (this.editableMode) {
                var $prod_slider = $('#wrapwrap').find('#eagle_theme_custom_product_slider');
                var prod_name = _t("Products Slider")
                
                _.each($prod_slider, function (single){
                    $(single).empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="fancy">' + prod_name + '</h3>\
                                                    </div>\
                                                </div>')
                });
            }
            if (!this.editableMode) {
                var slider_id = self.$target.attr('data-prod-slider-id');
                $.get("/eagle_theme/product_get_dynamic_slider", {
                    'slider-id': self.$target.attr('data-prod-slider-id') || '',
                }).then(function(data) {
                    if (data) {
                        self.$target.empty();
                        self.$target.append(data);
                        $(".oe_prod_slider").removeClass('o_hidden');

                        ajax.jsonRpc('/eagle_theme/product_image_effect_config', 'call', {
                            'slider_id': slider_id
                        }).done(function(res) {
                            $('div#' + res.s_id).owlCarousel({
                                margin: 10,
                                responsiveClass: true,
                                items: res.counts,
                                loop: true,
                                autoplay: res.auto_rotate,
                                autoplayTimeout:res.auto_play_time,
                                autoplayHoverPause:true,
                                responsive: {
                                    0: {
                                        items: 1,
                                    },
                                    420: {
                                        items: 2,
                                    },
                                    768: {
                                        items: 3,
                                    },
                                    1000: {
                                        items: res.counts,
                                    },
                                    1500: {
                                        items: res.counts,
                                    },
                                },
                            });
                        });
                    }
                });
            }
        }
    });

    animation.registry.eagle_theme_featured_product_slider = animation.Class.extend({

        selector: ".oe_featured_prod_slider",
        start: function() {
            var self = this;
            if (this.editableMode) {
                var $feat_prod_slider = $('#wrapwrap').find('#theme_carfito_custom_featured_product_theme');
                var fea_prod_name = _t("Featured Products Slider")

                _.each($feat_prod_slider, function (single){
                    $(single).empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="fancy">' + fea_prod_name + '</h3>\
                                                    </div>\
                                                </div>')
                });
            }
            if (!this.editableMode) {
                var slider_id = self.$target.attr('data-featured_prod-slider-id');
                $.get("/eagle_theme/featured_product_get_dynamic_slider", {
                    'slider-id': self.$target.attr('data-featured-prod-slider-id') || '',
                }).then(function(data) {
                    if (data) {
                        self.$target.empty();
                        self.$target.append(data);
                        $(".oe_featured_prod_slider").removeClass('o_hidden');
                    }
                });
            }
        }
    });

    animation.registry.biztech_new_theme_fact_sheet_jsselector = animation.Class.extend({
        selector: ".biztech_fact_sheet",
        start: function() {
            var self = this;
            if (this.editableMode) {
                var $skill_selector = $('#wrapwrap').find('.s_eagle_theme_facts_sheet');
                var skill_name = _t("Fact Sheet")

                _.each($skill_selector, function (single){
                    $(single).empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="fancy">' + skill_name + '</h3>\
                                                    </div>\
                                                </div>')
                });
            }
            if (!this.editableMode) {
                var years = self.$target.attr('data-fact-number-1')
                var clients = self.$target.attr('data-fact-number-2')
                var projects = self.$target.attr('data-fact-number-3')
                var awords = self.$target.attr('data-fact-number-4')
                var total = 0;
                var i;
                for (i = 1; i <= 4; i++) {
                    if (parseInt(self.$target.attr('data-fact-number-' + i)) > 0) {
                        total = total + 1
                    }
                }
                $.get('/biztech_fact_model_data/fact_data', {}).then(function(data) {
                    self.$target.empty().append(data);
                    if (parseInt(years) > 0) {
                        self.$target.find("span#custom_business").html(years)
                        self.$target.find("p#custom_label_business").html(self.$target.attr('data-fact-name-1'))
                        self.$target.find("i#business_icon").attr('class', self.$target.attr('data-fact-icon-1'))
                    }
                    if (parseInt(clients) > 0) {
                        self.$target.find("span#custom_Clients").html(clients)
                        self.$target.find("p#custom_label_Clients").html(self.$target.attr('data-fact-name-2'))
                        self.$target.find("i#client_icon").attr('class', self.$target.attr('data-fact-icon-2'))
                    }
                    if (parseInt(projects) > 0) {
                        self.$target.find("span#custom_Projects").html(projects)
                        self.$target.find("p#custom_label_Projects").html(self.$target.attr('data-fact-name-3'))
                        self.$target.find("i#project_icon").attr('class', self.$target.attr('data-fact-icon-3'))
                    }
                    if (parseInt(awords) > 0) {
                        self.$target.find("span#custom_Awards").html(awords)
                        self.$target.find("p#custom_label_Awards").html(self.$target.attr('data-fact-name-4'))
                        self.$target.find("i#awards_icon").attr('class', self.$target.attr('data-fact-icon-4'))
                    }

                    for (i = 1; i <= 4; i++) {
                        if (total == 1 & parseInt(self.$target.find("div#counter-inner-content-" + i + " span").html()) > 0) {
                            self.$target.find("div#counter-inner-content-" + i).removeClass("o_hidden")
                            self.$target.find("div#counter-inner-content-" + i).attr('class', "col-sm-12 counter-inner-content")
                        }
                        if (total == 2 & parseInt(self.$target.find("div#counter-inner-content-" + i + " span").html()) > 0) {
                            self.$target.find("div#counter-inner-content-" + i).removeClass("o_hidden")
                            self.$target.find("div#counter-inner-content-" + i).attr('class', "col-sm-6 counter-inner-content")
                        }
                        if (total == 3 & parseInt(self.$target.find("div#counter-inner-content-" + i + " span").html()) > 0) {
                            self.$target.find("div#counter-inner-content-" + i).removeClass("o_hidden")
                            self.$target.find("div#counter-inner-content-" + i).attr('class', "col-sm-4 counter-inner-content")
                        }
                        if (total == 4 & parseInt(self.$target.find("div#counter-inner-content-" + i + " span").html()) > 0) {
                            self.$target.find("div#counter-inner-content-" + i).removeClass("o_hidden")
                            self.$target.find("div#counter-inner-content-" + i).attr('class', "col-sm-3 counter-inner-content")
                        }
                    }
                    var $counter = $(self.$target.find('.counter'))
                    $counter.counterUp({
                        delay: 10,
                        time: 1000
                    });
                });
            }
        }
    });

    animation.registry.biztech_new_theme_skill_jsselector = animation.Class.extend({
        selector: ".biztech_new_theme_skill",
        start: function() {
            var self = this;
            if (this.editableMode) {
                var $skill_selector = $('#wrapwrap').find('.s_eagle_theme_skills');
                var skill_name = _t("Skill")

                _.each($skill_selector, function (single){
                    $(single).empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="fancy">' + skill_name + '</h3>\
                                                    </div>\
                                                </div>')
                });
            }
            if (!this.editableMode) {
                var total = 0;
                var i;
                for (i = 1; i <= 4; i++) {
                    if (parseInt(self.$target.attr('data-skill-number-' + i)) > 0) {
                        total = total + 1
                    }
                }
                $.get('/biztech_skill_model_data/skill_data', {}).then(function(data) {
                    self.$target.empty().append(data);
                    if (parseInt(self.$target.attr('data-skill-number-1')) > 0) {
                        self.$target.find("div.skill_graph_1").html(self.$target.attr('data-skill-number-1'))
                        self.$target.find("span#skill1").html("<h4>" + self.$target.attr('data-skill-name-1') + "</h4>")
                    }
                    if (parseInt(self.$target.attr('data-skill-number-2')) > 0) {
                        self.$target.find("div.skill_graph_2").html(self.$target.attr('data-skill-number-2'))
                        self.$target.find("span#skill2").html("<h4>" + self.$target.attr('data-skill-name-2') + "</h4>")
                    }
                    if (parseInt(self.$target.attr('data-skill-number-3')) > 0) {

                        self.$target.find("div.skill_graph_3").html(self.$target.attr('data-skill-number-3'))
                        self.$target.find("span#skill3").html("<h4>" + self.$target.attr('data-skill-name-3') + "</h4>")

                    }
                    if (parseInt(self.$target.attr('data-skill-number-4')) > 0) {

                        self.$target.find("div.skill_graph_4").html(self.$target.attr('data-skill-number-4'))
                        self.$target.find("span#skill4").html("<h4>" + self.$target.attr('data-skill-name-4') + "</h4>")
                    }

                    for (i = 1; i <= 4; i++) {
                        if (total == 1 & parseInt(self.$target.find("div#skill-inner-content-" + i + " div.custom_percentage").html()) > 0) {
                            self.$target.find("div#skill-inner-content-" + i).removeClass("o_hidden")
                            self.$target.find("div#skill-inner-content-" + i).attr('class', "col-md-12 counter-inner-content")
                        }
                        if (total == 2 & parseInt(self.$target.find("div#skill-inner-content-" + i + " div.custom_percentage").html()) > 0) {
                            self.$target.find("div#skill-inner-content-" + i).removeClass("o_hidden")
                            self.$target.find("div#skill-inner-content-" + i).attr('class', "col-md-6 counter-inner-content")
                        }
                        if (total == 3 & parseInt(self.$target.find("div#skill-inner-content-" + i + " div.custom_percentage").html()) > 0) {
                            self.$target.find("div#skill-inner-content-" + i).removeClass("o_hidden")
                            self.$target.find("div#skill-inner-content-" + i).attr('class', "col-md-4 counter-inner-content")
                        }
                        if (total == 4 & parseInt(self.$target.find("div#skill-inner-content-" + i + " div.custom_percentage").html()) > 0) {
                            self.$target.find("div#skill-inner-content-" + i).removeClass("o_hidden")
                            self.$target.find("div#skill-inner-content-" + i).attr('class', "col-md-3 counter-inner-content")
                        }
                    }

                    var waypoints = self.$target.find('#skill-counter').waypoint({
                        offset: '75%',
                        triggerOnce: true,
                        handler: function(direction) {
                            self.$target.find('#skill_graph_1').circleGraphic({
                                'color': '#3a424c'
                            });
                            self.$target.find('#skill_graph_2').circleGraphic({
                                'color': '#3a424c'
                            });
                            self.$target.find('#skill_graph_3').circleGraphic({
                                'color': '#3a424c'
                            });
                            self.$target.find('#skill_graph_4').circleGraphic({
                                'color': '#3a424c'
                            });
                        },
                    })
                });
            }
        }
    });

    animation.registry.s_biztech_new_theme_team_two = animation.Class.extend({
        selector: ".team",
        start: function() {
            var self = this;
            if (this.editableMode) {
                var $team_two = $('#wrapwrap').find('#eagle_theme_custom_second_team');
                
                _.each($team_two, function (single){
                    $(single).empty().append('<div class="block-title" contentEditable="false">\
                        <h3 class="fancy">Team 2</h3>\
                    </div>');
                });
            }
            if (!this.editableMode) {
                $.get("/biztech_emp_data/employee_data", {}).then(function(data) {
                    self.$target.empty();
                    self.$target.append(data);
                })
            }
        }
    });

    animation.registry.s_biztech_new_theme_team_one = animation.Class.extend({
        selector: ".column-3-team",
        start: function() {
            var self = this;
            if (this.editableMode) {
                var $team_one = $('#wrapwrap').find('#eagle_theme_custom_colthree_team');

                _.each($team_one, function (single){
                    $(single).empty().append('<div class="block-title" contentEditable="false">\
                        <h3 class="fancy">Team 1</h3>\
                    </div>');
                });
            }
            if (!this.editableMode) {
                $.get("/biztech_emp_data_one/employee_data", {}).then(function(data) {
                    self.$target.empty();
                    self.$target.append(data);
                })
            }
        }
    });

    animation.registry.s_biztech_new_theme_team_three = animation.Class.extend({
        selector: ".new-1-column-team",
        start: function() {
            var self = this;
            if (this.editableMode) {
                var $team_three = $('#wrapwrap').find('#eagle_theme_three_custom_team');

                _.each($team_three, function (single){
                    $(single).empty().append('<div class="block-title" contentEditable="false">\
                        <h3 class="fancy" style="color:white;">Team 3</h3>\
                    </div>');
                });
            }
            if (!this.editableMode) {
                $.get("/biztech_emp_data_three/employee_data", {}).then(function(data) {
                    self.$target.empty();
                    self.$target.append(data);
                    $('div#our_team_3').owlCarousel({
                        center: true,
                        items: 2,
                        loop: true,
                        margin: 10,
                        responsive: {
                            0: {
                                items: 1,
                            },
                            1000: {
                                items: 2,
                            }
                        }
                    });

                })
            }
        }
    });

    animation.registry.eagle_theme_news1_js = animation.Class.extend({
        selector: ".eagleshop_newsone_slider",
        start: function() {
            var self = this;
            if (this.editableMode) {
                var $news1 = $('#wrapwrap').find('#eagle_theme_custom_news1');

                _.each($news1, function (single){
                    $(single).empty().append('<div class="block-title" contentEditable="false">\
                        <h3 class="fancy">News1</h3>\
                    </div>');
                });
            }
            if (!this.editableMode) {
                var slider_type = self.$target.attr('data-newsone-slider-type');
                $.get("/eagle_theme/newsone_get_dynamic_slider", {
                    'slider-type': self.$target.attr('data-newsone-slider-type') || '',
                }).then(function(data) {
                    if (data) {
                        self.$target.empty();
                        self.$target.append(data);
                        $(".eagleshop_newsone_slider").removeClass('o_hidden');
                    }
                });
            }
        }
    });


    animation.registry.eagle_theme_news2_js = animation.Class.extend({
        selector: ".eagleshop_newstwo_slider",
        start: function() {
            var self = this;
            if (this.editableMode) {
                var $news2 = $('#wrapwrap').find('#eagle_theme_custom_second_news');
                var news_two_name = _t("News 2")

                _.each($news2, function (single){
                    $(single).empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="fancy">' + news_two_name + '</h3>\
                                                    </div>\
                                                </div>')
                });
            }
            if (!this.editableMode) {
                var slider_type = self.$target.attr('data-newstwo-slider-type');
                $.get("/eagle_theme/newstwo_get_dynamic_slider", {
                    'slider-type': self.$target.attr('data-newstwo-slider-type') || '',
                }).then(function(data) {
                    if (data) {
                        self.$target.empty();
                        self.$target.append(data);
                        $(".eagleshop_newstwo_slider").removeClass('o_hidden');
                    }
                });
            }
        }
    });

    animation.registry.eagle_theme_hardware_blog_snippet = animation.Class.extend({
        selector: ".eagle_theme_new_blog",
        start: function() {
            var self = this;
            if (this.editableMode) {
                var $blog_snipet = $('#wrapwrap').find('#eagle_theme_hardware_blog_inner_containt');

                _.each($blog_snipet, function (single){
                    $(single).empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="fancy">News3</h3>\
                                                    </div>\
                                                </div>')
                });

            }
            if (!this.editableMode) {
                var slider_type = self.$target.attr('data-hardware-newblog-slider-type');
                $.get("/eagle_theme/theme_new_hardware_blog", {
                    'slider-type': self.$target.attr('data-hardware-newblog-slider-type') || '',
                }).then(function(data) {
                    if (data) {
                        self.$target.empty();
                        self.$target.append(data);
                        $(".eagle_theme_new_blog").removeClass('o_hidden');
                    }
                });
            }
        }
    });

    animation.registry.s_eagle_theme_events = animation.Class.extend({
        selector: ".event_category",
        start: function() {
            var self = this;
            if (this.editableMode) {
                var $events= $('#wrapwrap').find('#eagle_theme_custom_event_category');
                
                _.each($events, function (single){
                    $(single).empty().append('<div class="block-title" contentEditable="false">' +
                        '<h3>Events</h3>' +
                        '</div>');
                });

            }
            if (!this.editableMode) {
                $.get("/eagle_theme/event_slider/get_data", {}).then(function(data) {
                    if (data) {
                        self.$target.empty();
                        self.$target.append(data);
                    }
                });
                var tabs = self.$target.find('.nav-tabs');
                var panes = self.$target.find('.tab-content');
                tabs.find('> li[role="presentation"] > a').first().addClass('active show');
                panes.find('> div[role="tabpanel"]:first').addClass('active show');

            }
        }
    });



});
