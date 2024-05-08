document.addEventListener("DOMContentLoaded", function() {
    var labels = document.querySelectorAll(".radio-container label");
  
    labels.forEach(function(label) {
        label.addEventListener("click", function() {
            labels.forEach(function(lbl) {
                lbl.classList.remove("checked");
            });
            label.classList.add("checked");
        });
    });
  });