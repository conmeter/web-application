$(document).ready(
        $('#otp_form').submit( function (f) {
            f.preventDefault();
            var otp = document.getElementById('otp').value
            $.ajax({
                url : "votp/",
                type: "POST",
                data: {
                    otp : otp
                },
                success : function(data) {
                    var msg = jQuery.parseJSON(data);
                    if(msg.Message == 'Success')
                    {
                   return true;
                }
                    else
                    {alert("Wrong OTP");
                return false;
                }
                },
                error: function (data) {
                    return false;
                } 
    
            });
    })
},
    
    );