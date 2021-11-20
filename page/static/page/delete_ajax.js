$(document).ready(
function delete_post(){
    $('a[id^=itemDel]').on("click", function (e) {
        e.preventDefault();
    if (confirm('are you sure you want to remove this post?')==true){
        var post_primary_key = $(this).attr('id');
        var id = post_primary_key.slice(7);
        $.ajax({
            url : "/feed/post/"+post_primary_key+"/", // the endpoint
            success : function(data) {
                // hide the post
                $("#cnt_p").text(parseInt($("#cnt_p").text()) - 1);
              $('.post'+id).hide(); // hide the post on success
              console.log("post deletion successful");
            },

        });
    } 
    else {
        return false;
    }
})
}
);
