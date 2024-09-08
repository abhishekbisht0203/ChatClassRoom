from pygments.formatters import HtmlFormatter

# Create a formatter with the desired style
formatter = HtmlFormatter(style='default', full=True, cssclass='codehilite')

# Write the CSS to a file
with open('styles.css', 'w') as f:
    f.write(formatter.get_style_defs('.codehilite'))
    
    # Add custom styles for the code box and line breaks
    f.write('''
    .codehilite {
        background-color: #f5f5f5;
        border: 1px solid #ddd;
        padding: 10px;
        overflow: auto;
        white-space: pre-wrap; /* Line breaks */
        border-radius: 5px; /* Rounded corners */
    }
    .codehilite pre {
        margin: 0;
    }
    .codehilite code {
        display: block;
    }
    ''')
