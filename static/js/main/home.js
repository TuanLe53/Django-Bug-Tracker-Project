function show_close(form, display_btn, close_btn) {
  display_btn.addEventListener("click", () => {
    form.style.display = "block";
  })
  close_btn.addEventListener("click", () => {
    form.style.display = "none";
  })
}
window.onload = function () {
  const project_close_btn = document.getElementById("close_form");
  const project_display_btn = document.getElementById("display_form");
  const project_form = document.getElementById("project_form");
  show_close(project_form, project_display_btn, project_close_btn);
}