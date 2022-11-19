document.addEventListener("DOMContentLoaded", () => {

    // Show and hide predecessor deactivation 

    predecessor_select = document.getElementById('id_predecessor')
    exclusive_predecessor = document.getElementById('div_id_exclusive_predecessor')
    exclusive_predecessor.hidden = true

    predecessor_select.addEventListener('input', (value) => {
        console.log(value)
        if (predecessor_select.value) {
            exclusive_predecessor.hidden = false
        } else {
            exclusive_predecessor.hidden = true
        }
    }, true);


})
