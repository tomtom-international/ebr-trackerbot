Test Tracker Slack Bot
======================

How to run:

`
docker build . -t test-tracker-slack-bot
`

`
docker run -e BR_URL=<br board url> -e API_URL=<api url> -e SLACK_TOKEN=<token> -e BACKEND=<memory|sqlite> -e SQLITE_FILENAME=<filename> test-tracker-slack-bot python ebr-trackerbot
`

