
$(document).ready(function(){
  $("#display_btn").click(function(){
    $("#u").show(1000);
    $("#start_disinfection").hide(1000);
    $("#one-blue-heading").css('color','#137dbb');
    $("#two-blue-heading").css('color','black');
    $("#three-blue-heading").css('color','#137dbb');
    $("#four-blue-heading").css('color','#137dbb');

  });
  $("#four-blue-heading").click(function(){
    $("#u").hide(1000);
    $("#div-done-btn").hide(1000);
    $("#start_disinfection").show(1000);
    $("#one-blue-heading").css('color','#137dbb');
    $("#two-blue-heading").css('color','#137dbb');
    $("#three-blue-heading").css('color','#137dbb');
    $("#four-blue-heading").css('color','#black');

  });

  $("#start_disinfection").click(function(){
    $("#sterlization").hide(1000);
    $("body").css('backdround-color','red');
  
  });

});


  var ros = new ROSLIB.Ros({
    url : 'ws://192.168.0.125:9090'
  });

  ros.on('connection', function() {
    console.log('Connected to websocket server.');
  });

  ros.on('error', function(error) {
    console.log('Error connecting to websocket server: ', error);
  });

  ros.on('close', function() {
    console.log('Connection to websocket server closed.');
  });

  

  // Subscribing to a Topic
  // ----------------------

  var listener = new ROSLIB.Topic({
    ros : ros,
    name : '/chatter',
    messageType : 'std_msgs/String'
  });

  listener.subscribe(function(message) {
    console.log(message.data);
    //listener.unsubscribe();
	if(message.data=="Reached"){
        $.ajax({
            url: '/reached',
            
            success: function(response) {
                console.log(response);
                

                //console.log(response);
                document.getElementById("sterlization").style.display="block";
                document.getElementById("nav_pose_nav").style.zIndex="999";
                document.getElementById("main").style.display="block";
                document.getElementById("main").style.zIndex="999";

                document.getElementById("nav_pose_nav").style.display="none";
                document.getElementById("nav_pose_nav").style.zIndex="-999";
                document.getElementById("main").style.display="none";
                document.getElementById("main").style.zIndex="-999";
            },
            error: function(error) {
                console.log(error);
            }
    
        });
      
    }
    if(message.data=="start"){
      document.getElementById("one-blue-heading").style.color="#137dbb";
      document.getElementById("two-blue-heading").style.color="#137dbb";
      document.getElementById("three-blue-heading").style.color="black";
      document.getElementById("four-blue-heading").style.color="#137dbb";
    }
  });


  
