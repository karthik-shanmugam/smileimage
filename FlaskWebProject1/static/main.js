$(document).ready(function() {
    Webcam.attach( '#my_camera' );
    $("#my_camera").hide();
    autoplay_interval = "empty";



    function progress_timeout(delay, callback) {
        var i = 100;
        var counterBack = setInterval(function () {
            $('.progress-bar').addClass("active");
            i = i - 100*100/delay;
            if (paused) {
                $('.progress-bar').css('width', 100 + '%');
                $('.progress-bar').removeClass("active");
                clearInterval(counterBack);
                return;
            }
            if (i > 0) {
                $('.progress-bar').css('width', i + '%');
            } else {
                $('.progress-bar').css('width', 0 + '%');
                clearInterval(counterBack);
                callback();
            }
        }, 100);
    }

    function get_emotion(callback) {
        Webcam.snap(function(data_uri) {
            images=[];
            images.push
            post("/images/uploads", {'images': JSON.stringify([data_uri]), 'content':$('.content').attr("src")}, callback);   
        });
    }

    function cycle_content(interval) {
        $.get("content", function( data ) {
            $(".content").load(function(){

                $(".emotion-img").attr("src", "");
                progress_timeout(interval, function() {
                    get_emotion(function(emotion){
                        console.log(emotion)
                        switch (emotion) {
                            case "happiness":
                                $(".emotion-img").attr("src", "emojis/happy.png");
                                break;
                            case "sadness":
                                $(".emotion-img").attr("src", "emojis/sad.png");
                                break;
                            case "anger":
                                $(".emotion-img").attr("src", "emojis/angry.png");
                                break;
                            case "surprise":
                                $(".emotion-img").attr("src", "emojis/surprised.png");
                                break;
                            case "neutral":
                                $(".emotion-img").attr("src", "emojis/neutral.png");
                                break;
                            default:
                                $(".emotion-img").attr("src", "emojis/missing.png");
                        }
                        setTimeout(function() {
                            cycle_content(interval);
                        }, interval);    
                    });
                });
            });
            $(".content").attr("src", data);

        });       
    }


    $(".snap").click(function() {
        collect_snapshots(0, 0, 1);
    });

    $(".autoplay").click(function() {
        $(this).toggleClass("btn-success");
        $(this).toggleClass("btn-warning");
        $(this).toggleClass("play");
        $(this).find("span").toggleClass("glyphicon-play");
        $(this).find("span").toggleClass("glyphicon-pause");

        if (!$(this).hasClass("play")) {
            paused = false;
            cycle_content(4000);
        } else {
            paused = true;
        }
    });

    $(".suggest").click(function() {
        post("/suggestion", {"url": $(".suggestion").val()}, function(data) {
            if (data == "failure") {
                //alert("suggested image was invalid!");
            }
        })
    })

    function get_content() {
        $.get("content", function( data ) {
          $(".content").attr("src", data);
          collect_snapshots(1500, 2000, 2);
        });
    }


    $(".get-content").click(get_content);

    function post(path, parameters, callback) {
        var form = $('<form></form>');

        form.attr("method", "post");
        form.attr("action", path);

        $.each(parameters, function(key, value) {
            var field = $('<input></input>');

            field.attr("type", "hidden");
            field.attr("name", key);
            field.attr("value", value);

            form.append(field);
        });

        // The form needs to be a part of the document in
        // order for us to be able to submit it.
        $.ajax({
            url:path,
            type:'post',
            data:form.serialize(),
            success:callback
        });
        // $(document.body).append(form);
        // form.submit();
        console.log("submitted")
    }    
})
