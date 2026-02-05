const { timeStamp } = require("console");
const http = require("http");
let counter = 0;
const server = http.createServer((req,res) => {
    res.writeHead(200,{"Conten-Type":"application/json"});
    if(req.url === "/ping"){
        
        res.end(JSON.stringify({ timeStamp: Date.now()}));
    }
    else if(req.url === "/headers"){
        res.end(JSON.stringify(req.headers, null, 2));
    }
    else if(req.url === "/count"){
        counter++;
        res.end(JSON.stringify({count:counter}));

    }
    else{
        res.writeHead(404);
        res.end("Not Found");
    }
}
);

server.listen(3000,() => {
    console.log("Server running on port 3000");
})