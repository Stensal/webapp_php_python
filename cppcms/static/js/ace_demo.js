var demo_editor = ace.edit("ace_demo_code_editor");
init();

function init() {
    /* init the ace_demo_code_editor */
    demo_editor.setTheme("ace/theme/xcode");
    demo_editor.session.setMode("ace/mode/c_cpp");
    demo_editor.setOptions({highlightActiveLine: true});

    /* init a sample code */
    var demo_editor_init = new XMLHttpRequest();
    demo_editor_init.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            demo_editor.setValue(this.responseText);
            demo_editor.resize(true);
            demo_editor.gotoLine(5, 15, true);
        }
    };
    demo_editor_init.open("GET", "/static/foo.js", true);
    demo_editor_init.send();
}

function get_code() {
    return demo_editor.getValue();
}

function runAceCode() {}
