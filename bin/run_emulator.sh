#!/bin/sh

export $(grep -v '^#' .env.local | xargs)

functions-framework --target chatgpt_slackbot --debug
