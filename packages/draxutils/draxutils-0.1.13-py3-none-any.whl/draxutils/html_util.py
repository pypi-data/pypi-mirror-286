def generate_html_wrapper(body):
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Responsive Layout</title>
    <style>
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        td {{
            border: 1px solid #ddd;
            padding: 8px;
        }}
        img {{
            max-width: 100%;
            height: auto;
            display: block;
        }}
    </style>
</head>
<body>
{body}
</body>
</html>
"""
    return html_template