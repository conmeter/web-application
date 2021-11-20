$(document).ready(
    setInterval(function (){
            var post_primary_key = $(this).attr('count_posts');
            $.ajax({
                url : "count-posts/", // the endpoint
                success : function(data) {
                    $("#count_posts").html(data['count']);
                },
    
            });
    }, 10000)
    );