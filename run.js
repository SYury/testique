var lang = null
var problem = null
var src = null

function testCode() {
    var exec = require('child_process').exec;
    var str = 'python3 test.py --submit ' + lang + ' ' + problem + ' --file ' + src + ' --out .testres';
    exec(str, function (error, stdOut, stdErr) {if(error){console.log(error);}});
}

var connect = require('connect');
var fs = require('fs'),
    path = require('path');
var url = require('url');
var qs = require('querystring');
var formidable = require('formidable');
    util = require('util');
    fs = require('fs');
connect().use(function (req, res, next) {
      var query;
      var url_parts = url.parse(req.url, true);
      query = url_parts.query;
      console.log(url_parts.pathname);
      if (req.method == 'GET') {
        switch (url_parts.pathname) {
            case '/test':
            testCode();
            res.end();
            break;
            default:
            if(url_parts.pathname == '/'){url_parts.pathname = '/main.html';}
            res.writeHeader(200, {"Content-Type": "text/html"});
            filePath = path.join(__dirname, url_parts.pathname);
            fs.readFile(filePath, {encoding: 'utf-8'}, function(err,data){res.write(data); res.end();});
            break;
          }
        }
      if (req.method == 'POST') {
        switch (url_parts.pathname) {
            case '/setlng':
            var body = '';
            req.on('data', function(data){body += data;});
            req.on('end', function(){var vals = qs.parse(body); lang = vals['item'];});
            res.end();
            break;
            case '/setprob':
            var body = '';
            req.on('data', function(data){body += data;});
            req.on('end', function(){var vals = qs.parse(body); problem = vals['item'];});
            res.end();
            break;
            case '/setsrc':
            var body = '';
            req.on('data', function(data){body += data;});
            req.on('end', function(){var vals = qs.parse(body); src = vals['item'];});
            res.end();
            break;
            case '/uploadsrc':
            var form = new formidable.IncomingForm();
            form.uploadDir = __dirname;
            form.parse(req, function(err, fields, files) {
                var oldpath = files.files.path;
                var newpath = __dirname + "/" + src; 
                console.log(newpath);
                fs.rename(oldpath, newpath, function (err) { if (err) throw err; });
            });
            res.end();
            break;
          }
        }
    }).listen(8080);
