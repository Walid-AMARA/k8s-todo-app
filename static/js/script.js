// Add any client-side JavaScript functionality here
document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in animation to todo items
    const listItems = document.querySelectorAll('.list-group-item');
    listItems.forEach((item, index) => {
        item.style.opacity = '0';
        setTimeout(() => {
            item.style.transition = 'opacity 0.3s ease';
            item.style.opacity = '1';
        }, index * 100);
    });
    
    // Confirm delete
    const deleteButtons = document.querySelectorAll('a[href^="/delete/"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this todo?')) {
                e.preventDefault();
            }
        });
    });
});