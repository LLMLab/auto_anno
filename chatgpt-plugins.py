import json

import quart
import quart_cors
from quart import request
from utils.anno.cls.text_classification import text_classification
from utils.anno.ner.entity_extract import extract_named_entities

# Note: Setting CORS to allow chat.openapi.com is only required when running a localhost plugin
app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")


@app.post("/classification/<string:username>")
async def classification(username):
    request = await quart.request.get_json(force=True)
    text = request["text"]
    types = request["types"]
    result = text_classification(text, types)
    return quart.Response(response=json.dumps(result), status=200)


@app.post("/entityextract/<string:username>")
async def entityextract(username):
    request = await quart.request.get_json(force=True)
    text = request["text"]
    types = request["types"]
    result = extract_named_entities(text, types)
    return quart.Response(response=json.dumps(result), status=200)


@app.get("/.well-known/logo.png")
async def plugin_logo():
    filename = './.well-known/logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/.well-known/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("./.well-known/openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)


if __name__ == "__main__":
    main()