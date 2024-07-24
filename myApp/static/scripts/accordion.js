document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.accordion-button');

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const content = button.nextElementSibling;
            const icon = button.querySelector('.accordion-icon');

            // Close all other accordion items
            document.querySelectorAll('.accordion-content').forEach(el => {
                if (el !== content) el.style.display = 'none';
            });
            document.querySelectorAll('.accordion-icon').forEach(el => {
                if (el !== icon) el.textContent = '+';
            });

            // Toggle the clicked accordion item
            if (content.style.display === 'block') {
                content.style.display = 'none';
                icon.textContent = '+';
            } else {
                content.style.display = 'block';
                icon.textContent = '-';
            }
        });
    });
});
