$(document).ready(function() {
    $(document).ajaxSend(function(event, xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        function sameOrigin(url) {
            // url could be relative or scheme relative or absolute
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.
                !(/^(\/\/|http:|https:).*/.test(url));
        }
        function safeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });
    
    var bunkee_id = null;
    var bunkee_name = null;

    var input_box = $("#search-input");
    
    if(input_box.length > 0){
    
    
    
        $.widget("custom.users_catcomplete", $.ui.autocomplete, {
            _renderMenu: function(ul, items) {
                var self = this;
                $.each(items,
                    function(index, item) {
                        self._renderItem(ul, item);
                    });
                }
        });
        
        $(input_box).users_catcomplete({
            source: function(request, response) {
                $.ajax({
                    type: "GET",
                    url: "/ajax/user_search",
                    data: {
                        "q": request.term,
                    },
                    success: function(result) {
                        var json = $.parseJSON(result);
                        response(json);
                    }
                });
            },
            select: function(event, ui){
                D.log(event);
                D.log(ui);
                $(input_box).val(ui.item.name);
                bunkee_id = ui.item.pk;
                bunkee_name = ui.item.name;
                return false;
            }
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
    
    }
    
    function bunk(id, name){
        $.ajax({
            type: "POST",
            url: "/ajax/bunk",
            data: {
                bunkee: id
            },
            dataType: 'JSON',
            success: function(result){
                if(result.status == 'ok'){
                    alert('Great! You bunked ' + name);
                    $(input_box).val('');
                    window.location.reload();
                    
                }
            }, 
            error: function(result){
                D.log("Fail");
                D.log(result);
            }
        });
    }
    
    $('#profile-bunk').click(function(e){
       e.preventDefault();
       D.log($('#user-name').html());
       bunk($(this).attr('data-id'), $.trim($('#user-name').html()));
    });
    
    
    $('#bunk-button').click(function(e){
        e.preventDefault();     
        if(!bunkee_id) return;
        bunk(bunkee_id, bunkee_name);
    });
    
});