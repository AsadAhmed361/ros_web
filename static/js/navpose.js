
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
    $("body").css('background-color','#bb0b30');
    $("#disinfection").show(1000);
    var disinfection = false;
let req_min=5;
let req_sec=00;
var cd = new Date();
var countDownDate = new Date(String(cd.getMonth()+1)+" "+String(cd.getDate())+", "+String(cd.getFullYear())+" "+String(cd.getHours())+":"+String(cd.getMinutes()+req_min)+":"+String(req_sec)+":00").getTime();
let elem = document.getElementById("greenBar");
let stepValue = 0; 
var per= null;
var count = null;
var x = setInterval(function() {

  // Get today's date and time
  var now = new Date().getTime();
  
  // Find the distance between now and the count down date
  var distance = countDownDate - now;
  var timePer=(distance/now*100)*10000000;
  
  if(timePer>100){
    per=2;
  }
  else{
    per = parseInt(Math.abs(timePer-100));
  }
  console.log(per);
  stepValue=per;
   elem.style.width = (per ) + "%";
      //elem.innerHTML = (stepValue ) + "%";
      
  // Time calculations for days, hours, minutes and seconds
  //var days = Math.floor(distance / (1000 * 60 * 60 * 24));
  //var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);
    
  // Output the result in an element with id="demo"
  if(minutes<10){
    document.getElementById("demoo").innerHTML = "0"+minutes + ":" + seconds ;
  }
  if(seconds<10){
    document.getElementById("demoo").innerHTML = minutes + ":" + "0"+seconds ;
  }
  if((minutes<10)&&(seconds<10)){
    document.getElementById("demoo").innerHTML = "0"+minutes + ":" + "0"+seconds ;
  }
  count = count+1;
    
  // If the count down is over, write some text 
  if (distance < 0) {
    clearInterval(x);
    count = count/60;
    $("body").css('background-color','#00cb80');
    $("#disinfection").hide(1000);
    $("#dis_fin").show(1000);
    document.getElementById("demo").innerHTML = "Time spend disinfection: "+ String(count)+" Sminutes";
  }
}, 1000);
  });

});


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


  
