document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');

    searchInput.addEventListener('input', async () => {
        const query = searchInput.value.trim();
        if (query.length === 0) {
            searchResults.innerHTML = '';
            return;
        }

        try {
            const response = await fetch(`/search_users?query=${encodeURIComponent(query)}`);
            const data = await response.json();
            const users = data.users;

            // Clear previous results
            searchResults.innerHTML = '';

            if (users.length === 0) {
                searchResults.innerHTML = '<p class="p-2">No users found.</p>';
                return;
            }

            users.forEach(user => {
                const link = document.createElement('a');
                link.href = `/user/${user.username}`;
                link.textContent = user.username;
                link.classList.add('d-block', 'p-2', 'text-dark', 'text-decoration-none');
                link.addEventListener('mouseover', () => link.classList.add('bg-secondary', 'text-white'));
                link.addEventListener('mouseout', () => link.classList.remove('bg-secondary', 'text-white'));
                searchResults.appendChild(link);
            });
        } catch (error) {
            console.error('Error fetching search results:', error);
        }
    });
});
