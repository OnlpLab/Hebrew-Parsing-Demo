var fs = require('fs');
var json2csv = require('json2csv');

function writeToFile(data_to_append) {

    var newLine= "\r\n";

    var fields = ['Query', 'correctness', 'analysis'];


    var toCsv = {
        data: data_to_append,
        fields: fields,
        hasCSVColumnTitle: false
    };

    fs.stat('report.csv', function (err, stat) {
        if (err == null) {
            console.log('File exists');

            //write the actual data and end with newline
            var csv = json2csv(toCsv) + newLine;

            fs.appendFile('report.csv', csv, function (err) {
                if (err) throw err;
                console.log('The data was appended to file!');
            });
        }
        else {
            //write the headers and newline
            console.log('New file, just writing headers');
            fields= (fields + newLine);

            fs.writeFile('report.csv', fields, function (err, stat) {
                if (err) throw err;
                console.log('file saved');
            });
        }
    });

}



function report(obj, correctness, level) {
    var query = document.getElementById("id_utterance").innerHTML;
    var analysis = document.getElementById(level).innerHTML;
    var data = [{"query": query, "correctness": correctness, "reported-analysis": analysis}];
    if (correctness == 'crash') {
        alert('Thank you for your feedback!');
    }
//    writeToFile(data);
    changeSize(obj);
  }

function changeSize(obj) {
    if (obj.className == "feedback correct") {
        obj.style.fontSize = 'xx-large';
        obj.style.color = 'green';
    } else if (obj.className == "feedback incorrect") {
        obj.style.fontSize = 'xx-large';
        obj.style.color = 'red';
    }
}

