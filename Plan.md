# Basic Plan

Here's the deal

## URL Structure
domain/api/command
domain/web/command

## Description
Each command results in the output of a json object. That object has text for Siri to speak, and also a dictionary of the relevant data.

If you call the API path then just the JSON is returned and the Siri shortcut will be written to parse it.
If you call the web path, then a page will be built that has the text in a blurb and then the data in a table.

Should work for basically any command now or later.

See `sample.json` for how everything is supposed to look.