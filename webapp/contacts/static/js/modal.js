// ============================================
// Modal Management for Add and Modify Buttons
// ============================================
const userModal = document.getElementById("userModal");

if (userModal) {
  userModal.addEventListener('show.bs.modal', event => {
    // Extract info from data-bs-* attributes
    const form = userModal.querySelector('#userForm');
    const submitBtn = userModal.querySelector('#submitButton');
    const title = userModal.querySelector('#modalTitle');

    // Button that triggered the modal
    const button = event.relatedTarget;

    if (button.id == "modifyButton") {
        // Modal called by Modify Button set on a specific user
        form.first_name.value = button.getAttribute('data-bs-firstname');
        form.last_name.value = button.getAttribute('data-bs-lastname');
        form.address.value = button.getAttribute('data-bs-address') || "";
        form.phone_number.value = button.getAttribute('data-bs-phone') || "";

        title.textContent = "Modify Contact";
        submitBtn.textContent = 'Modify';
        submitBtn.setAttribute('formaction', button.getAttribute('data-url'));
    } 
    else {
        // Modal called by Add Button -> reset the form
        form.reset();
        
        title.textContent = "Add Contact"
        submitBtn.textContent = "Add";
        submitBtn.setAttribute('formaction', button.getAttribute('data-url'));
    }
  });
}