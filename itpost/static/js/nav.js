const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const closeMobileMenuBtn = document.getElementById('close-mobile-menu');
const mobileMenu = document.getElementById('mobile-menu');

mobileMenuBtn.addEventListener('click', () => {
    mobileMenu.classList.add('open');
});

closeMobileMenuBtn.addEventListener('click', () => {
    mobileMenu.classList.remove('open');
});


mobileMenu.addEventListener('click', (e) => {
    if (e.target.classList.contains('bg-gray-900')) {
        mobileMenu.classList.remove('open');
    }
});


const profileBtn = document.getElementById('profile-btn');
const profileDropdown = document.getElementById('profile-dropdown');

profileBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    profileDropdown.classList.toggle('open');
});


document.addEventListener('click', () => {
    profileDropdown.classList.remove('open');
});

profileDropdown.addEventListener('click', (e) => {
    e.stopPropagation();
});