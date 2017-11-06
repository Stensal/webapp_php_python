the directory structure:
- static  (css and js)
- templates (cppcms html templates, the template language reference: http://cppcms.com/wikipp/en/page/cppcms_1x_templates)
  home.tmpl (the demo page)

We can see html pages in browser by the tool 'browsersync', please follow these steps:
- install Nodejs
- install browsersync (npm install -g browser-sync)
- run this command under the dictionary webapp_php\cppcms (browser-sync start --server --files "**")
- open in broswer: http://localhost:3000/static/html/
If anything is unclear, please refer to https://browsersync.io/
