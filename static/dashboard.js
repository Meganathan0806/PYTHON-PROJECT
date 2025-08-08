
// Show and hide category dropdown
function showCategorySelect() {
    document.getElementById('categorySelect').style.display = 'block';
}

// Show only selected category
function showCategory(category) {
    document.querySelectorAll(".items").forEach(el => el.style.display = "none");
    const section = document.getElementById(category);
    if (section) section.style.display = "flex";
}
     











// Show home (hide all category sections)
function goHome() {
    document.querySelectorAll(".items").forEach(el => el.style.display = "none");
}

// Redirect to cart page
function showCartPage() {
    window.location.href = "/cart";
}

function addToCart(name, price, image) {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    const index = cart.findIndex(item => item.name === name);
    if (index !== -1) {
        cart[index].quantity += 1;
    } else {
        cart.push({ name, price, image, quantity: 1 });
    }

    localStorage.setItem("cart", JSON.stringify(cart));
    updateCartCount();
    alert(`${name} added to cart!`);
}

function updateCartCount() {
    const cart = JSON.parse(localStorage.getItem("cart")) || [];
    const cartCount = document.getElementById("cartCount");
    if (cartCount) {
        cartCount.textContent = cart.length;
    }
}










// Buy now - redirect to success page (simulating payment)
function buyNow(name, price) {
    const order = { name, price, quantity: 1 };
    localStorage.setItem("buyNowItem", JSON.stringify(order));
    window.location.href = "/success"; // You can create a /success route to handle this
}

document.addEventListener("DOMContentLoaded", () => {
    const slides = document.querySelectorAll(".slides img");
    let currentIndex = 0;

    function showSlide(index) {
        slides.forEach((img, i) => {
            img.classList.remove("active");
            if (i === index) {
                img.classList.add("active");
            }
        });
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % slides.length;
        showSlide(currentIndex);
    }

    showSlide(currentIndex);
    setInterval(nextSlide, 2000); // Change every 2 seconds
});









// Update cart count from localStorage
function updateCartCount() {
    const cart = JSON.parse(localStorage.getItem("cart")) || [];
    let count = 0;
    cart.forEach(item => count += item.quantity);
    document.getElementById("cartCount").innerText = count;
}

// Run on page load
window.onload = function () {
    goHome(); // Hide all items initially
    updateCartCount();
};

