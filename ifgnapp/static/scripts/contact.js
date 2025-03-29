
// Mobile menu toggle
// document.querySelector('.menu-toggle').addEventListener('click', function() {
//     document.querySelector('.nav-links').classList.toggle('active');
//     document.querySelector('.hamburger').classList.toggle('active');
// });

// Form validation
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Simple validation
        let valid = true;
        const requiredFields = contactForm.querySelectorAll('[required]');
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                valid = false;
                field.classList.add('error');
            } else {
                field.classList.remove('error');
            }
        });
        
        // Email validation
        const emailField = document.getElementById('email');
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (emailField && !emailPattern.test(emailField.value)) {
            valid = false;
            emailField.classList.add('error');
        }
        
        if (valid) {
            // In a real implementation, you would send the form data to a server
            alert('Thank you for your message! We will get back to you soon.');
            contactForm.reset();
        } else {
            alert('Please fill in all required fields correctly.');
        }
    });
}

// FAQ accordion functionality
const faqItems = document.querySelectorAll('.faq-item');

faqItems.forEach(item => {
    const question = item.querySelector('.faq-question');
    
    question.addEventListener('click', () => {
        // Close all other FAQ items
        faqItems.forEach(otherItem => {
            if (otherItem !== item && otherItem.classList.contains('active')) {
                otherItem.classList.remove('active');
            }
        });
        
        // Toggle current FAQ item
        item.classList.toggle('active');
    });
});
