/*
Purpose: Delete any network interface in VPC which are created by Lambda function and not in use. 
Reference: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/EC2.html#describeNetworkInterfaces-property

Others: Useful related CLI commands
    aws ec2 describe-vpcs --vpc-ids vpc-d704f9b0
    aws ec2 describe-subnets --filters "Name=vpc-id,Values=vpc-d704f9b0"
    aws ec2 describe-network-interfaces > eni.txt
*/

// Load the AWS SDK for Node.js
var AWS = require('aws-sdk');
// Set the region 
AWS.config.update({region: 'ap-southeast-1'});
// Create EC2 service object
var ec2 = new AWS.EC2();

var vpc_id = 'vpc-xxxxxxxx';

var params = {
    VpcIds: [
        vpc_id,
    ]
};
ec2.describeVpcs(params, function(err, data) {
    if (err) console.log(err, err.stack); // an error occurred
    else     console.log(data);           // successful response
});

var params = {
    DryRun: false,
    Filters: [
      {
        Name: 'vpc-id',
        Values: [
          vpc_id,
        ]
      },
    ],
  };
ec2.describeNetworkInterfaces(params, function(err, data) {
    if (err) console.log(err, err.stack); // an error occurred
    else {
        count = 0;
        eni_list = data['NetworkInterfaces'];
        console.log(eni_list.length);
        for(let i=0, len = eni_list.length; i < len; i++) {
            let obj = eni_list[i];
            if (obj["Description"].indexOf('AWS Lambda VPC ENI')>-1){
                count++;
                var params = {
                    DryRun: false,
                    NetworkInterfaceId: obj['NetworkInterfaceId']
                };
                ec2.deleteNetworkInterface(params, function(err, data) {
                     if (err) console.log(err, err.stack); // an error occurred
                     else     console.log(data);           // successful response
                });
            }
        }
        console.log(count)
    }
});

