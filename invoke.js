const AWS = require("aws-sdk")
AWS.config.update({
    region: 'us-east-1' 
});

const TABLE_NAME = "Rules2022Dec14";
const RULES_ENGINE = 'dynamo-test';
const BIOMARKER_PATH = 'actual_biomarkers.json';
const lambda = new AWS.Lambda();
const S3 = new AWS.S3();
const fs = require('fs')

async function invokeRulesEngine(paramFile){
    var res = await lambda.invoke({
        FunctionName: RULES_ENGINE,
        Payload: JSON.stringify({
            tableName: TABLE_NAME,
            biomarkers: paramFile
        }),
        InvocationType: "RequestResponse",
    }).promise();
    return res;
}

let actual_biomarkers = fs.readFileSync(BIOMARKER_PATH);

let actual = JSON.parse(actual_biomarkers);
var output = {}

async function iterateFiles(){
    for(var key in actual){
        output[key] = {'biomarkers' : {}, 'response': {}};

        for(var biomarker in actual[key].biomarkers){
            output[key]['biomarkers'][biomarker] = actual[key]['biomarkers'][biomarker];
        }

        var response = await invokeRulesEngine(actual[key]['biomarkers']);
        output[key]['response'] = response;
    }
    console.log(output);
    fs.writeFile('output.json', JSON.stringify(output, null, 4), 'utf8', function (err) {
        if (err) {
            return console.log(err);
        } 
        console.log("The file was saved!");
    });
}

iterateFiles();