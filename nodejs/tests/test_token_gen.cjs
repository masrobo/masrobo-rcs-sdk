const jwt = require('jsonwebtoken');
var app_id = 'p6rnL8yjUaT3ZLlL';
var app_key = '7649102d0ce1f5528aad7f6f9a4388cd';
var token = jwt.sign({ app_id, app_key }, app_key);

console.log(token);
