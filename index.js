var server_addr = "100.72.143.10" // IP address of your Raspberry PI
var server_port = 65432          // The port used by the server

function client(input){
    const net = require('net');
    var input = document.getElementById("myName").value;

    const client = net.createConnection({ port: server_port, host: server_addr },()=>{
        console.log('connected to server!')
        client.write(`${input}\r\n`);
    });

    client.on('data', (data) => {
        const response = data.toString().trim()
        if(response === "done"){
            document.getElementById("move_status").innerHTML = "Car status: " + data;
            client.end();
            client.destroy();
        }
        else if(response === "moving"){
            document.getElementById("move_status").innerHTML = "Car status: " + data;
        }
        else if(response === "left" || response === "right" || response === "center" ){
            document.getElementById("turn_status").innerHTML = "Steering " + data;
        }
        else{
            document.getElementById("sensor_distance").innerHTML = "Obstacle distance: " + data;
        }
        console.log(data.toString());
    });

    client.on('end', () => {
        console.log('disconnected from sever');
    });
}

function greeting(){
    var name = document.getElementById("myName").value;
    document.getElementById("last_move").innerHTML = "Last Move: " + name;
    //to_server(name);
    client(name);
}