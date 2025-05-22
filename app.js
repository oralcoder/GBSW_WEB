const express = require('express');
const app = express();


app.get('/', function(req, res) {
	res.send('Root 페이지입니다.');
});

app.get('/test', function(req, res) {
	res.send('test 페이지입니다.');
});

const PORT = 8080;
app.listen(PORT, function() {
    console.log('Listening on port: ', PORT);
});