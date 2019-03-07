$(document).ready(function(){
    var mot = false
    var intru = false
    var gls = false
    var lek = false
    var playing = false


    function startAlarm(){
        if((mot || intru || gls || lek) & (!playing)){
        	playing = true
            var x = document.getElementById("myAudio"); 
            x.loop = true;
            x.load();
            x.play(); 
            console.log('playing audo')
        }
    }

    function stopAlarm(){
        if (!mot && !intru && !gls && !lek){
        	playing = false
            var x = document.getElementById("myAudio"); 
            x.pause(); 
            console.log('pausing audo')
        }
    }

    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var numbers_received = [];

    //receive details from server
    socket.on('newnumber', function(msg) {
        console.log("Received number" + msg.number);
        //maintain a list of ten numbers
        if (numbers_received.length >= 10){
            numbers_received.shift()
        }            
        numbers_received.push(msg.number);
        numbers_string = '';
        for (var i = 0; i < numbers_received.length; i++){
            numbers_string = numbers_string + '<p>' + numbers_received[i].toString() + '</p>';
        }
        $('#log').html(numbers_string);
        var t = msg.number;
        console.log(t['temp']);
        document.getElementById("temp").textContent=msg.number + '°C';
        console.log('asdfasdfasdf')
    });

    socket.on('motion', function(msg) {
        console.log("Motion Detection: " + msg.motion);
        if(msg.motion == "True"){
            document.getElementById("motion").textContent='Motion Detected';
            $('#motion-card').removeClass('green')
            $('#motion-card').addClass('red')
            mot = true
            startAlarm()
        }
        else{
            document.getElementById("motion").textContent='No Motion Detected';
            $('#motion-card').removeClass('red')
            $('#motion-card').addClass('green')
            mot = false
            stopAlarm()
        }

    });


    socket.on('intruder', function(msg) {
        console.log("Intruder Detection: " + msg.intruder);
        if(msg.intruder == "True"){
            document.getElementById("intruder").textContent='Intruder Detected';
            $('#intruder-card').removeClass('green')
            $('#intruder-card').addClass('red')
            intru = true
            startAlarm()
        }
        else{
            document.getElementById("intruder").textContent='No Intruder Detected';
            $('#intruder-card').removeClass('red')
            $('#intruder-card').addClass('green')
            intru = false
            stopAlarm()
        }
    });


    socket.on('windows', function(msg) {
        console.log("Glass Break Detection: " + msg.windows);
        if(msg.windows == "True"){
            document.getElementById("windows").textContent='Window Glass Brocken';
            $('#windows-card').removeClass('green')
            $('#windows-card').addClass('red')
            gls = true
            startAlarm()
        }
        else{
            document.getElementById("windows").textContent='No Brocken Glass Detected';
            $('#windows-card').removeClass('red')
            $('#windows-card').addClass('green')
            gls = false
            stopAlarm()
        }
    });

    socket.on('leak', function(msg) {
        console.log("Leakage Detection: " + msg.leak);
        if(msg.leak == "True"){
            document.getElementById("leak").textContent='Water Leakage Detected';
            $('#leak-card').removeClass('green')
            $('#leak-card').addClass('red')
            lek = true
            startAlarm()
        }
        else{
            document.getElementById("leak").textContent='No Water Leakage Detected';
            $('#leak-card').removeClass('red')
            $('#leak-card').addClass('green')
            lek = false
            stopAlarm()
        }


    });
});

