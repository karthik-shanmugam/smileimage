$(document).ready(function() {
    Webcam.attach( '#my_camera' );
    $("#my_camera").hide();
    autoplay_interval = "empty";

    function collect_snapshots(delay, interval, frames) {
        $(".emotion-img").attr("src", "");
        images = [];
        // for (i = 0; i < frames; i++) { 
        //     setTimeout(function(){
        //         console.log("snap!!!");
        //         Webcam.snap(function(data_uri) {images.push(data_uri);});
        //     }, delay + (interval/frames)*i);
        // }
        $("#cd").cooldown({
          tickFrequency:      50,        // Frequency of ticks (milliseconds), not recommended <50, affects
                                         // countdown (and arc in non-Chrome browsers)
          arcWidth:           10,        // Arc stroke width
          arcColor:           "#27ae60", // Arc stroke color
          arcBackgroundColor: "#d7d8d9", // Arc stroke unfinished color
          toFixed:            1,         // Number of decimal places to show in countdown
          introDuration:      0,       // Duration of spinning intro (milliseconds), set to 0 to disable
          countdownCss:       {          // Object of CSS attributes (passed to jQuery's css() function)
                                width: "100%",
                                height: "100%",
                                margin: 0,
                                padding: 0,
                                textAlign: "center",
                                fontSize: "16px"
                              },
          completeFn:         function(){
                console.log("snap!!!");Webcam.snap(function(data_uri) {images.push(data_uri);});
                post("/images/uploads", {'images': JSON.stringify(images), 'content':$('.content').attr("src")}, function(data){
                    console.log(data);
                    switch (data) {
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
                });   
                },       // Callback function called when cooldown expires
          countdownFn:        null       // Can be used to override how the countdown is displayed, is passed
                                         // the remaining time in seconds
        }).start(delay/1000.0);
        // setTimeout(function() {
        //     post("/images/uploads", {'images': JSON.stringify(images), 'content':$('.content').attr("src")}, function(data){
        //         console.log(data);
        //         switch (data) {
        //             case "happiness":
        //                 $(".emotion-img").attr("src", "emojis/happy.png");
        //                 break;
        //             case "sadness":
        //                 $(".emotion-img").attr("src", "emojis/sad.png");
        //                 break;
        //             case "anger":
        //                 $(".emotion-img").attr("src", "emojis/angry.png");
        //                 break;
        //             case "surprise":
        //                 $(".emotion-img").attr("src", "emojis/surprised.png");
        //                 break;
        //             case "neutral":
        //                 $(".emotion-img").attr("src", "emojis/neutral.png");
        //                 break;
        //             default:
        //                 $(".emotion-img").attr("src", "emojis/missing.png");
        //         }
        //     });            
        // }, delay+interval+200);
  
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
            autoplay_interval = setInterval(get_content, 8000);
            get_content();
        } else {
            if (autoplay_interval != "empty") {
                clearInterval(autoplay_interval);
            }
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
