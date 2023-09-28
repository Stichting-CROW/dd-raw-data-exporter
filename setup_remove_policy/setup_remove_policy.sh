export AWS_PROFILE=do

aws s3api put-bucket-lifecycle-configuration \
    --bucket dashboarddeelmobiliteit \
    --endpoint https://ams3.digitaloceanspaces.com \
    --lifecycle-configuration file://remove_policy.json

aws s3api get-bucket-lifecycle-configuration \
    --bucket dashboarddeelmobiliteit \
    --endpoint https://ams3.digitaloceanspaces.com