/**
 * This code performs a sort of media query
 * to resize the markdown editor textarea
 * when the screen reaches certain transition
 * points.
 */

function resizeMarkdownEditor() {
  markdownEditorTextArea = document.getElementById("flask-pagedown-content");
  windowHeight = window.innerHeight;
  console.log(windowHeight);
  if (windowHeight >= 650 && markdownEditorTextArea.rows !== 20) {
    markdownEditorTextArea.rows = 20
  } else if (windowHeight < 650 && markdownEditorTextArea.rows !== 10) {
    markdownEditorTextArea.rows = 10
  }
}

window.addEventListener('resize', resizeMarkdownEditor);
