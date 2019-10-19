eagle.define('eagleshop_custom_js', function(require) {
    'use strict';

    var ajax = require('web.ajax');

    // header fix
    $(window).scroll(function() {
        if ($(window).scrollTop() >= 146) {
            $('body').addClass('header-fixed');
        } else {
            $('body').removeClass('header-fixed');
        }
    });

    $(document).ready(function($) {

        $('.header-middle, div#wrap, footer').click(function() {
            $('div.only-list').find('#mobile_ul').addClass('o_hidden');
        });

        $("a#mobile").click(function() {
            if ($('#top_menu_collapse').hasClass('show')) {
                $('#top_menu_collapse').removeClass('show');
            }
            if (!$("ul#mobile_ul").hasClass('o_hidden')) {
                $('ul#mobile_ul').addClass('o_hidden');
            }
            else {
                $('ul#mobile_ul').removeClass('o_hidden');
            }
        });

        $('.navbar-toggler').click(function() {
            if (!$('ul#mobile_ul').hasClass('o_hidden')) {
                $('ul#mobile_ul').addClass('o_hidden');
            }
        });

        // level-1 
        $('ul#mobile_ul li.ca-sub').click(function(e) {
            e.stopPropagation();
            if ($(this).children('ul').hasClass('o_hidden') == true){
                $(this).children('ul').removeClass('o_hidden');
                
                $(this).addClass('ca-open');
            }else{
                $(this).find('ul.level-2, ul.level-3, ul.level-4').addClass('o_hidden');
                $(this).find('li.ca-open').removeClass('ca-open');
                $(this).removeClass('ca-open');
            }
        });

        // // level-2 
        $('ul#mobile_ul li.ca-sub1').click(function(e) {
            e.stopPropagation();
            if ($(this).children('ul').hasClass('o_hidden') == true){
                $(this).children('ul').removeClass('o_hidden');
                
                $(this).addClass('ca-open')
            }else{
                $(this).find('ul.level-3, ul.level-4').addClass('o_hidden')
                $(this).find('li.ca-open').removeClass('ca-open');
                $(this).removeClass('ca-open');
            }
        });

        // // level-3 
        $('ul#mobile_ul li.ca-sub2').click(function(e) {
            e.stopPropagation();
            if ($(this).children('ul').hasClass('o_hidden') == true){
                $(this).children('ul').removeClass('o_hidden');
                
                $(this).addClass('ca-open')
            }else{
                $(this).find('ul.level-4').addClass('o_hidden')
                $(this).find('li.ca-open').removeClass('ca-open')
                $(this).removeClass('ca-open');
            }
        });


        $('a[data-action=customize_theme]').click(function() {
            setTimeout(function(){
                if ($('.modal-body').hasClass('eagleshop-theme') == true) {
                    $('.modal-body').parent().parent().addClass('only-eagleshop-theme')
                    $('.modal-body').parent().addClass('only-eagleshop-theme')
                }
            }, 200);
        });
        $("ul.o_menu_sections > li.content").addClass("custom_padding_topmenu_content");
        // browser window scroll (in pixels) after which the "back to top" link is shown
        var offset = 300,
            //browser window scroll (in pixels) after which the "back to top" link opacity is reduced
            offset_opacity = 1200,
            //duration of the top scrolling animation (in ms)
            scroll_top_duration = 700,
            //grab the "back to top" link
            $back_to_top = $('.cd-top');

        //hide or show the "back to top" link
        $(window).scroll(function() {
            ($(this).scrollTop() > offset) ? $back_to_top.addClass('cd-is-visible'): $back_to_top.removeClass('cd-is-visible cd-fade-out');
            if ($(this).scrollTop() > offset_opacity) {
                $back_to_top.addClass('cd-fade-out');
            }
        });

        //smooth scroll to top
        $back_to_top.on('click', function(event) {
            event.preventDefault();
            $('body,html').animate({scrollTop: 0}, scroll_top_duration);
        });

        //mobile touch
        $(".carousel").carousel();
        //Cutom tabs
        if ($('.king-tabs').length > 0) {
            $(window).load(function() {
                var currentTab = $(".king-tabs .nav.nav-tabs li a.active").attr("name"),
                    tabsImageAnimation = $(".king-tabs-top").find("[data-tab='" + currentTab + "']").attr("data-tab-animation-effect");
                
                
                $(".king-tabs-top").find("[data-tab='" + currentTab + "']").addClass("current-img show " + tabsImageAnimation + " animated");

                $('.king-tabs .nav.nav-tabs li a').on('click', function(event) {
                    var currentTab = $(this).attr("name"),
                        tabsImageAnimation = $(".king-tabs-top").find("[data-tab='" + currentTab + "']").attr("data-tab-animation-effect");
                    $(".current-img").removeClass("current-img show " + tabsImageAnimation + " animated");
                    $(".king-tabs-top").find("[data-tab='" + currentTab + "']").addClass("current-img show " + tabsImageAnimation + " animated");
                });
                // $('#myCollapse .card a').on('click', function(event) {           
                //     var currentTab = $(this).attr("name"),
                //     tabsImageAnimation = $("#myCollapse .card .collapse").find("[data-tab='" + currentTab + "']");
                //     console.log("current tabs",currentTab );
                //     $("#myCollapse .card .collapse").removeClass("show");
                //     tabsImageAnimation.addClass("collapse show")
                // });
            });
        }

        // Fix edit bar when logined
        if ($('nav#oe_main_menu_navbar').length) {
            $('header').css({'top': '34px'});
        }
        if (!$('nav#oe_main_menu_navbar').length) {
            $('header').css({'top': '0'});
        }

        $('.counter').counterUp({
            delay: 10,
            time: 1000
        });

        // Grid/List switching code
        $(".oe_website_sale .shift_list_view").click(function(e) {
            $(".oe_website_sale .shift_grid_view").removeClass('active');
            $(this).addClass('active');
            $('#products_grid').addClass("list-view-box");
            $('.oe_website_sale .oe_subdescription').addClass('o_hidden');
            localStorage.setItem("product_view", "list");
        });

        $(".oe_website_sale .shift_grid_view").click(function(e) {
            $(".oe_website_sale .shift_list_view").removeClass('active');
            $(this).addClass('active');
            $('#products_grid').removeClass("list-view-box");
            $('.oe_website_sale .oe_subdescription').removeClass('o_hidden');
            localStorage.setItem("product_view", "grid");
        });

        if (localStorage.getItem("product_view") == 'list') {
            $(".oe_website_sale .shift_grid_view").removeClass('active');
            $(".oe_website_sale .shift_list_view").addClass('active');
            $('.oe_website_sale .oe_subdescription').addClass('o_hidden');
            $('#products_grid').addClass("list-view-box");
        }

        if (localStorage.getItem("product_view") == 'grid') {
            $(".oe_website_sale .shift_list_view").removeClass('active');
            $(".oe_website_sale .shift_grid_view").addClass('active');
            $('.oe_website_sale .oe_subdescription').removeClass('o_hidden');
            $('#products_grid').removeClass("list-view-box");
        }

        // Grid/List switching code ends
        // Switched to review section
        $('p.review').click(function() {
            $('body').animate({
                scrollTop: $(this).offset().top
            }, 1800);
            $('ul#description_reviews_tabs > li > a').removeClass('active');
            $('div#description_reviews_tabs_contents > div').removeClass('active');
            $('ul#description_reviews_tabs > li:nth-child(2) > a').addClass('active');
            $('div#description_reviews_tabs_contents > div:nth-child(2)').addClass('active');
        });

        // recommended_products_slider
        $('div#recommended_products_slider').owlCarousel({
            margin: 10,
            responsiveClass: true,
            items: 4,
            // loop: true,
            autoPlay: 7000,
            stopOnHover: true,
            navigation: true,
            responsive: {
                0: {
                    items: 1,
                },
                500: {
                    items: 2,
                },
                700: {
                    items: 3,
                },
                1000: {
                    items: 4,
                },
                1500: {
                    items: 4,
                }
            }
        });

        // Multi image gallery
        var api;
        ajax.jsonRpc('/eagle_theme/eagleshop_multi_image_effect_config', 'call', {})
            .done(function(res) {
                var dynamic_data = {}
                dynamic_data['gallery_images_preload_type'] = 'all'
                dynamic_data['slider_enable_text_panel'] = false
                dynamic_data['gallery_skin'] = "alexis"

                dynamic_data['gallery_height'] = 800
                dynamic_data['gallery_min_height'] = 500

                if (res.theme_panel_position != false) {
                    dynamic_data['theme_panel_position'] = res.theme_panel_position
                }

                if (res.interval_play != false) {
                    dynamic_data['gallery_play_interval'] = res.interval_play
                }

                if (res.color_opt_thumbnail != false && res.color_opt_thumbnail != 'default') {
                    dynamic_data['thumb_image_overlay_effect'] = true
                    if (res.color_opt_thumbnail == 'b_n_w') {}
                    if (res.color_opt_thumbnail == 'blur') {
                        dynamic_data['thumb_image_overlay_type'] = "blur"
                    }
                    if (res.color_opt_thumbnail == 'sepia') {
                        dynamic_data['thumb_image_overlay_type'] = "sepia"
                    }
                }

                if (res.enable_disable_text == true) {
                    dynamic_data['slider_enable_text_panel'] = true
                }

                if (res.change_thumbnail_size == true) {
                    dynamic_data['thumb_height'] = res.thumb_height
                    dynamic_data['thumb_width'] = res.thumb_width
                }

                if (res.no_extra_options == false) {
                    dynamic_data['slider_enable_arrows'] = false
                    dynamic_data['slider_enable_progress_indicator'] = false
                    dynamic_data['slider_enable_play_button'] = false
                    dynamic_data['slider_enable_fullscreen_button'] = false
                    dynamic_data['slider_enable_zoom_panel'] = false
                    dynamic_data['slider_enable_text_panel'] = false
                    dynamic_data['strippanel_enable_handle'] = false
                    dynamic_data['gridpanel_enable_handle'] = false
                    dynamic_data['theme_panel_position'] = 'bottom'
                    dynamic_data['thumb_image_overlay_effect'] = false
                }

                api = $('#gallery').unitegallery(dynamic_data);
                api.on("item_change", function(num, data) {
                    if (data['index'] == 0) {
                        update_gallery_product_image();
                    }
                });

                if (api != undefined && $('#gallery').length != 0){
                    setTimeout(function(){
                        update_gallery_product_image()
                    }, 500);
                }
            });

       

        function update_gallery_product_image() {
            var $container = $('.oe_website_sale').find('.ug-slide-wrapper');
            var $img = $container.find('img');
            var $product_container = $('.oe_website_sale').find('.js_product').first();
            var p_id = parseInt($product_container.find('input.product_id').first().val());

            if (p_id > 0) {
                $img.each(function(e_img) {
                    if ($(this).attr("src").startsWith('/web/image/biztech.product.images/') == false) {
                        $(this).attr("src", "/web/image/product.product/" + p_id + "/image");
                    }
                });
            } else {
                var spare_link = api.getItem(0).urlThumb;
                $img.each(function(e_img) {
                    if ($(this).attr("src").startsWith('/web/image/biztech.product.images/') == false) {
                        $(this).attr("src", spare_link);
                    }
                });
            }
        }
         function update_gallery_product_variant_image(event_source, product_id) {
            var $imgs = $(event_source).closest('.oe_website_sale').find('.ug-slide-wrapper');
            var $img = $imgs.find('img');
            var total_img = api.getNumItems()
            if (total_img != undefined) {
                api.selectItem(0);
            }
            var $stay;
            $img.each(function(e) {
                if ($(this).attr("src").startsWith('/web/image/biztech.product.images/') == false) {
                    if ($(this).attr("src").match('/flip_image') == null) {
                        $(this).attr("src", "/web/image/product.product/" + product_id + "/image");
                        $("img.product_detail_img").attr("src", "/web/image/product.product/" + product_id + "/image");
                        $stay = $(this).parent().parent();
                        $(this).css({
                            'width': 'initial',
                            'height': 'initial'
                        });
                        api.resetZoom();
                        api.zoomIn();
                    }
                }
            });
        }
        $('.oe_website_sale').on('change', '[data-attribute_exclusions]', function(ev) {
            var self = this
            setTimeout(function() {
                var product_id = $('input.product_id').val();
                if (product_id) {
                    update_gallery_product_variant_image(self, product_id);
                }
            }, 500)
        });

        $('.oe_website_sale').each(function() {
            var oe_website_sale = this;
            var clickwatch = (function() {
                var timer = 0;
                return function(callback, ms) {
                    clearTimeout(timer);
                    timer = setTimeout(callback, ms);
                };
            })();

            $(oe_website_sale).on("change", ".oe_cart input.js_quantity[data-product-id]", function() {
                
                var $input = $(this);
                if ($input.data('update_change')) {
                    return;
                }
                var value = parseInt($input.val(), 10);
                var $dom = $(this).closest('tr');
                var $dom_optional = $dom.nextUntil(':not(.optional_product.info)');
                var line_id = parseInt($input.data('line-id'), 10);
                var product_id = parseInt($input.data('product-id'), 10);
                var product_ids = [product_id];
                clickwatch(function() {
                    $dom_optional.each(function() {
                        $(this).find('.js_quantity').text(value);
                        product_ids.push($(this).find('span[data-product-id]').data('product-id'));
                    });
                    $input.data('update_change', true);
                    var $q1 = $(".eagle_theme_cart_quantity");
                    if (value) {
                        $q1.parent().parent().removeClass("o_hidden");
                    } else {
                        $q1.parent().parent().find('.eagle_theme_cart_quantity').html(0)
                        $('a[href^="/shop/checkout"]').addClass("o_hidden")
                    }
                    ajax.jsonRpc("/shop/cart/update_json", 'call', {
                        'line_id': line_id,
                        'product_id': parseInt($input.data('product-id'), 10),
                        'set_qty': value
                    }).then(function(data) {
                        $input.data('update_change', false);
                        if (value !== parseInt($input.val(), 10)) {
                            $input.trigger('change');
                            return;
                        }
                        if (data.cart_quantity == undefined) {
                            data['cart_quantity'] = 0;
                            window.location.reload();
                        }
                        var $q1 = $(".eagle_theme_cart_quantity");
                        $q1.hide();

                        var startTime = new Date().getTime();
                        var my_hover_total = setInterval(function(){
                            if(new Date().getTime() - startTime > 1000){
                                clearInterval(my_hover_total);
                                $q1.html(data.cart_quantity).fadeIn(500);
                                return;
                            }
                            $("#eagleshop_hover_total").empty().html(data['hover_total']);
                            $(".js_cart_lines").first().before(data['website_sale.cart_lines']).end().remove();
                        }, 100);

                        my_hover_total;

                    });
                }, 100);
            });

            $(oe_website_sale).on('click', '.o_wish_add', function() {
                setTimeout(function(){
                    window.location.reload();
                }, 500)
            });
        });

        // Price slider code start
        var minval = $("input#m1").attr('value'),
            maxval = $('input#m2').attr('value'),
            minrange = $('input#ra1').attr('value'),
            maxrange = $('input#ra2').attr('value'),
            website_currency = $('input#king_pro_website_currency').attr('value');

        if (!minval) {
            minval = 0;
        }
        if (!maxval) {
            maxval = maxrange;
        }
        if (!minrange) {
            minrange = 0;

        }
        if (!maxrange) {
            maxrange = 2000;
        }

        $("div#priceslider").ionRangeSlider({
            keyboard: true,
            min: parseInt(minrange),
            max: parseInt(maxrange),
            type: 'double',
            from: minval,
            to: maxval,
            step: 1,
            prefix: website_currency,
            grid: true,
            onFinish: function(data) {
                $("input[name='min1']").attr('value', parseInt(data.from));
                $("input[name='max1']").attr('value', parseInt(data.to));
                $("div#priceslider").closest("form").submit();
            },
        });
        // Price slider code ends
        $("a#clear").on('click', function() {
            var url = window.location.href.split("?");
            var lival = $(this).closest("li").attr('id');

            ajax.jsonRpc("/theme_carfito/removeattribute", 'call', {
                'attr_remove': lival
            }).then(function(data) {
                if (data == true) {
                    window.location.href = url[0];
                }
            });
        });

    });

    //Equal height
    $(window).load(function() {
        equal_height_all();
    });

    function equal_height_all() {
        function resetHeight() {
            var maxHeight = 0;
            jQuery(".f-block h4").height("auto").each(function() {
                maxHeight = $(this).height() > maxHeight ? $(this).height() : maxHeight;
            }).height(maxHeight);
        }
        resetHeight();
        jQuery(window).resize(function() {
            resetHeight();
        });
    }
})