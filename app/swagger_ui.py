"""Custom Swagger UI with CDN resources"""
from flask import Blueprint, render_template_string

swagger_bp = Blueprint('swagger_ui', __name__, url_prefix='/swagger')


SWAGGER_UI_HTML = '''
<!DOCTYPE html>
<html>
  <head>
    <title>Ingredient & Recipe API - Swagger UI</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui.css">
    <style>
      html {
        box-sizing: border-box;
        overflow: -moz-scrollbars-vertical;
        overflow-y: scroll;
      }
      *, *:before, *:after {
        box-sizing: inherit;
      }
      body {
        margin: 0;
        background: #fafafa;
      }
      .topbar {
        background-color: #1a73e8;
        padding: 10px 20px;
        color: white;
        text-align: center;
      }
      .topbar h1 {
        margin: 0;
        font-size: 24px;
      }
    </style>
  </head>
  <body>
    <div class="topbar">
      <h1>🍳 Ingredient & Recipe API</h1>
    </div>
    <div id="swagger-ui"></div>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-bundle.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-standalone-preset.js"></script>
    <script>
      window.onload = function() {
        const ui = SwaggerUIBundle({
          url: "/apispec.json",
          dom_id: '#swagger-ui',
          deepLinking: true,
          presets: [
            SwaggerUIBundle.presets.apis,
            SwaggerUIStandalonePreset
          ],
          plugins: [
            SwaggerUIBundle.plugins.DownloadUrl
          ],
          layout: "StandaloneLayout",
          defaultModelsExpandDepth: 1,
          defaultModelExpandDepth: 1,
          supportedSubmitMethods: ["get", "post", "put", "delete", "patch", "head", "options"]
        })
        window.ui = ui
      }
    </script>
  </body>
</html>
'''


@swagger_bp.route('/', methods=['GET'])
def swagger_ui():
    """Serve Swagger UI with CDN resources"""
    return render_template_string(SWAGGER_UI_HTML)
