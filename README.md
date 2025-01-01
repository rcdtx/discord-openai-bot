# discord-openai-bot
Discord bot using the OpenAI api for chatGPT prompts in discord channel.


Build instructions
```
docker build --platform linux/amd64 -t <docker image name>:latest .

docker tag <docker image name>:latest <ECRrepositoryUri>:latest

docker push <ECRrepositoryUri>:latest
```

Create lambda function
```
aws lambda create-function \
--function-name chatgpt-bot \
--package-type Image \
--code ImageUri=<ECRrepositoryUri>:latest \
--role <lambda role>
```

To update lambda code after rebuilding container:
```
aws lambda update-function-code --function-name chatgpt-bot --image-uri <ECRrepositoryUri>:latest
```
