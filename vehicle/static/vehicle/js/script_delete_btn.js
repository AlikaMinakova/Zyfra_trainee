document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll(".delete-btn");

    deleteButtons.forEach(button => {
        button.addEventListener("click", function () {
            const confirmed = confirm("Вы уверены, что хотите удалить этот элемет?");
            if (confirmed) {
                // const row = button.closest("tr");
                // row.remove();
            }
        });
    });
});
