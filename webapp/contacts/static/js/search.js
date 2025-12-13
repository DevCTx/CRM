// ============================================
// Search Management for Search Bar and Button
// ============================================
const searchForm = document.getElementById('searchForm');
const searchInput = searchForm?.querySelector('input');

if (searchForm && searchInput) {

    // Avoid a reload
    searchForm.addEventListener('submit', event => {
        event.preventDefault();
    });

    // Real Time Filtering
    searchInput.addEventListener('input', () => {
        const query = searchInput.value.toLowerCase().trim();
        const accordionItems = document.querySelectorAll('.accordion-item');

        accordionItems.forEach(item => {
            // Get the user data
            const name = item.querySelector('#user_full_name').textContent.toLowerCase();
            const address = item.querySelector('#user_address')?.textContent.toLowerCase() || '';
            const phone = item.querySelector('#user_phone_number')?.textContent.toLowerCase() || '';

            item.style.display = (name.includes(query) || address.includes(query) || phone.includes(query)) ? '' : 'none';
        });
    });
}