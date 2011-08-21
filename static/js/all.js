$(document).ready(function() {
    
    $.widget("custom.users_catcomplete", $.ui.autocomplete, {
        _renderMenu: function(ul, items) {
            var self = this;
            $.each(items,
                function(index, item) {
                    self._renderItem(ul, item);
                });
            }
        });
        
        var input_box = $("#search-input");
        
        // Prevent hitting Enter from doing anything
        $(input_box).live('keypress', function(e) {
            if(e.keyCode==13){
                e.preventDefault();
            }
        });

        $(input_box).users_catcomplete({
            source: function(request, response) {
                $.ajax({
                    type: "GET",
                    url: "/ajax/user_search",
                    data: {
                        "q":$(input_box).val(),
                    },
                    success: function(result) {
                        var json = $.parseJSON(result);
                        response(json);
                    },
                    error: function(jqXHR, textStatus, error) {
                        //debug.log(jqXHR);
                    }
                });
            },
            select: function(event, ui) {
                //D.log(ui.item);
                select_callback(select_callback_data, ui.item);
                $(input_box).val("");
                event.preventDefault();
                // prevents search box from being updated with the tag value..
            },
            focus: function(event, ui) {
              event.preventDefault();  
            },
        }).data("users_catcomplete")._renderItem = function(ul, user) {
            return $("<li></li>")
                   .data("item.autocomplete", user)
                   .append($(""))
                   .append($("<a class='ui-menu-item'></a>")
                   .html("<img class='search-image' src='" + user.image + "' />" + 
                         "<span class='search-result-title'>" + user.name + 
                         "</span>"))
                   .appendTo(ul);
        };
    
    
    
});