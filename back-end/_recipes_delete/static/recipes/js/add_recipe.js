document.addEventListener("DOMContentLoaded", () => {
  // Show and hide predecessor deactivation

  predecessor_select = document.getElementById("id_predecessor");
  exclusive_inheritance = document.getElementById(
    "div_id_exclusive_inheritance"
  );

  if (!predecessor_select.value) {
    exclusive_inheritance.hidden = true;
  }

  predecessor_select.addEventListener(
    "input",
    (value) => {
      if (predecessor_select.value) {
        window.location.replace(
          `/recipes/recipe/add/` + predecessor_select.value
        );
      } else {
        window.location.replace(`/recipes/recipe/add`);
      }
    },
    true
  );
});
