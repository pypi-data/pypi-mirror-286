"""Global options for streamlit pages"""

CSS = """
    <style>
    .head-h2 {
        text-align: left;
        margin-top: -2em;
        font-family: sans-serif;
        font-weight: normal;
        font-size: 24px;
    }
    .para-p1 {
        text-align: left;
        margin-top: -1em;
        font-family: sans-serif;
        font-weight: normal;
        font-size: 16px;
    }
    .profile-card {
        margin-top: -1em;
        margin-bottom: 1em;
        # margin: 10px;
        background: LightYellow;
        box-shadow: inset 2px 2px 5px 0px #dddddd;
        height: 100px;
        width: 750px;
        overflow: auto;
        padding: 5px 5px;
        font-family: tahoma;
        # font-family: Lucida Console;
        font-weight: 500;
        font-size: 13px;
        color: MediumBlue;
        border: 1px solid #aaa;
    }
    .profile-card ul li {
        list-style-type:disc;
        margin-left: 30px;
        padding-left:20px
        font-family: tahoma;
        font-weight: 500;
        font-size: 13px;
        color: MediumBlue;
    }
    .profile-card li:before {
        content: "";
        margin-left: -0.5rem;
    }
    .output-card-1 {
        margin-top: 0.5em;
        margin-bottom: 0.5em;
        # margin: 10px;
        background: LightYellow;
        box-shadow: inset 2px 2px 5px 0px #dddddd;
        height: 70px;
        width: 500px;
        overflow: auto;
        padding: 10px 10px;
        font-family: tahoma;
        font-weight: 500;
        font-size: 13px;
    }
    div[class*="stRadio"]>label>div[data-testid="stMarkdownContainer"]>p {
        font-family: sans-serif;
        font-weight: normal;
        font-size: 20px;
        color: DodgerBlue;
    }
    [role=radiogroup] {
        margin-top: -1.5em;
        gap: 5px;
        padding: 25px;
    }
    div[class*="stSelect"]>label>div[data-testid="stMarkdownContainer"]>p {
        font-family: sans-serif;
        font-weight: normal;
        font-size: 16px;
        color: DodgerBlue;
    }
    div[class*="stTextArea"] label {
        font-size: 20px !important;
        color: black;
    }
    div[class*="stTextInput"] label {
        font-size: 20px !important;
        color: black;
    }
    </style>
    """

# Static table display style
static_table_style = {
    "th_props": [
        ('font-family', 'sans-serif'),
        ('font-weight', 'normal'),
        ('font-size', '16px'),
        ('text-align', 'left'),
        ('font-weight', 'bold'),
        ('color', '#6d6d6d'),
        ('background-color', 'LightCyan')
    ],  # table header
    "td_props": [
        ('font-family', 'sans-serif'),
        ('font-weight', 'normal'),
        ('font-size', '14px'),
        # ('font-weight', 'bold')
    ]  # table data
}
