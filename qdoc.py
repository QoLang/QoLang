#!/usr/bin/python3
import sys
import runpy

template = """<!DOCTYPE html>
<html>
<title>QoLang Docs</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://www.w3schools.com/w3css/4/w3.css" rel="stylesheet">
<link href="https://prismjs.com/plugins/line-numbers/prism-line-numbers.css" rel="stylesheet" />
<link href="https://prismjs.com/plugins/toolbar/prism-toolbar.css" rel="stylesheet" />
<link href="/style/prism-apprentice/prism-apprentice.css" rel="stylesheet" />
<link href="/style/prism-apprentice/prism-apprentice.css" rel="stylesheet" />
<link href="https://qolang.camroku.tech/style/index.css" rel="stylesheet" />
<link href="https://qolang.camroku.tech/style/apprentice.css" rel="stylesheet" />
<body class="">
<!-- Page Content -->
<div class="w3-container border-bottom mid head">
  <h1><img src="https://qolang.camroku.tech/images/qolang.png" width="32"/> The Qo Programming Language Documentation</h1>
</div>
<div class="sidebar">
<!--NAV-->
</div>
<div class="w3-container" style="margin-left: 200px;">
<!--CONTENTS-->
</div>
<script>
if (window.location.hash && document.getElementById(window.location.hash.substring(1) + "Tab")) {
  document.getElementById(window.location.hash.substring(1) + "Tab").click();
}

if (window.location.hash && window.location.hash.startsWith("#docs.")) {
  var i, x, tablinks;
  x = document.getElementsByClassName("section");
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("side");
  for (i = 0; i < x.length; i++) {
    tablinks[i].className = tablinks[i].className.replace("side-active", "");
  }
  document.getElementById("docs." + window.location.hash.split(".")[1]).style.display = "block";
  document.getElementById("docs." + window.location.hash.split(".")[1] + "Tab").className += " side-active";
  document.getElementById(window.location.hash.substr(1)).scrollIntoView();
}

function chTab(evt, tab) {
  var i, x, tablinks;
  x = document.getElementsByClassName("section");
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("side");
  for (i = 0; i < x.length; i++) {
    tablinks[i].className = tablinks[i].className.replace("side-active", "");
  }
  document.getElementById(tab).style.display = "block";
  evt.currentTarget.className += " side-active";
  history.pushState({}, "", "#" + tab);
}
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.28.0/prism.min.js"></script>
<script src="https://prismjs.com/plugins/toolbar/prism-toolbar.js"></script>
<script src="https://prismjs.com/plugins/line-numbers/prism-line-numbers.js"></script>
<script src="https://prismjs.com/plugins/normalize-whitespace/prism-normalize-whitespace.js"></script>
<script src="https://prismjs.com/plugins/show-language/prism-show-language.js"></script>
<script src="/scripts/qo-prism/qo-prism.js"></script>
</body>
</html>"""

out = ""
nav = ""

first = True

for file in sys.argv[1:]:
    vis = "block" if first else "none"
    acv = " side-active" if first else ""
    first = False
    out += f"<div id=\"docs.{file[:-3]}\" class=\"w3-panel section\" style=\"display:{vis}\">"
    nav += f"<button class=\"side{acv}\" onclick=\"chTab(event,'docs.{file[:-3]}')\" id=\"docs.{file[:-3]}Tab\">{file[:-3]}</button>"
    contents = runpy.run_path(file)
    if "__doc__" in contents:
        out += contents["__doc__"]
    else:
        out += "No description for this library."
    out += "<h1>Table of Contents</h1><ul>"
    added = []
    for fpy, fqo in contents["qolang_export"].items():
        if contents[fpy].__doc__ in added:
            continue
        added.append(contents[fpy].__doc__)
        out += f"<li><a href=\"#docs.{file[:-3]}.{fqo}\"><code class=\"language-qo\">{contents[fpy].__doc__.splitlines()[1].strip()}</code></a></li>"
    out += "</ul><h1>Documentation</h1>"
    added = []
    for fpy, fqo in contents["qolang_export"].items():
        if contents[fpy].__doc__ in added:
            continue
        added.append(contents[fpy].__doc__)
        out += f"<div><h3 id=\"docs.{file[:-3]}.{fqo}\"><a href=\"#docs.{file[:-3]}.{fqo}\"><code class=\"language-qo\">{contents[fpy].__doc__.splitlines()[1].strip()}</code></a></h3>{'<br/>'.join(contents[fpy].__doc__.splitlines()[2:])}</div>"
    out += "</div>"

print(template.replace("<!--NAV-->", nav).replace("<!--CONTENTS-->", out))
