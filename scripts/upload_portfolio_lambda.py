import boto3
import StringIO
import zipfile
import mimetypes


def lambda_handler(event, context):

    sns =boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:367134135555:DeployportfolioTopic')

    try:
        s3 = boto3.resource('s3')

        portfolio_bucket = s3.Bucket('portfolio.passout.cloud')
        build_bucket = s3.Bucket('portfoliobuild.passout.cloud')

        portfolio_zip = StringIO.StringIO()
        build_bucket.download_fileobj('Portfoliobuild.zip', portfolio_zip)

        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj, nm,
                ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')

        print "Job Done Tiger!"
        topic.publish(Subject="Successful Portfolio Deployment", Message="Portfolio delployed successfully Tiger!")
    except:
        topic.publish(Subject="Portfolio Deployment Failed", Message="Portfolio delployment failure")
        raise

    return 'Hello from Lambda'
