docker build -t optcbx .
docker rm -f $(docker ps -aq)
docker run -p 1234:1234 \
    -e DATABASE_URL="postgres://slbsbfxmqualum:fc9c513016e9c4ee93248213a66107423e3ef856c696ad43643716e7a1a3b787@ec2-46-137-84-173.eu-west-1.compute.amazonaws.com:5432/defvulja18ng1g" \
    -e PORT=1234 \
    -v "C:/Users/GNOM/Desktop/Guillem/Personal Github/optc-character-matcher":/optc-box-exporter \
    optcbx