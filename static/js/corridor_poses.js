var doc_pose=null;
$(document).ready(function(){
$("#click").click(function(){
    console.log("click");
    $("#div-popup").hide(1000);
    $("#click").hide(1000);
    $("#load").hide(1000);

  });
});
function myfunction(pose){
    doc_pose=pose
    //var pose=document.getElementById("pose").innerHTML;
    $.ajax({
        url: '/corridor_poses/sendpose',
        type: 'POST',
        data: pose,
        success: function(response) {
            //window.location ="/";
            document.getElementById("h").innerHTML="Going to "+pose;
            $("#div-popup").show(1000);
            $("#load").show(1000);
            console.log(response);
        },
        error: function(error) {
            console.log(error);
        }

    })
    console.log(pose);
}


var ros = new ROSLIB.Ros({
    url : 'ws://192.168.0.107:9090'
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
        document.getElementById("h").innerHTML="Reached at "+doc_pose;
        $("#load").hide(1000);
        $("#click").show(1000);
    }
    
  });


  
