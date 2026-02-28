let currentOrder = {
    meal: null,
    special: null,
    dalPrice: 10,
    rotiCost: 0,
    specialPrice: 0,
    total: 0,
    lunchPlates: 1
};

let rotiQuantity = 0;
let rotiPricePerPiece = 5;
let lunchPlatePrice = 50;

// 🕒 Update time status
function updateTimeStatus() {
    const now = new Date();
    const hour = now.getHours();
    const timeStatus = document.getElementById('timeStatus');
    const lunchStatus = document.getElementById('lunchStatus');
    const dinnerStatus = document.getElementById('dinnerStatus');
    const lunchMenu = document.getElementById('lunchMenu');
    const dinnerMenu = document.getElementById('dinnerMenu');

    // Lunch time (9 AM - 11 AM)
    if (hour >= 9 && hour < 11) {
        timeStatus.innerHTML = '✅ Lunch Time is OPEN';
        timeStatus.className = 'time-status open-message';
        lunchStatus.innerHTML = '<div class="open-message">🍛 Lunch ordering is now OPEN!</div>';
        lunchMenu.style.display = 'block';
    } else {
        lunchStatus.innerHTML = '<div class="closed-message">⛔ Lunch ordering is CLOSED<br>Available only between 9:00 AM - 11:00 AM</div>';
        lunchMenu.style.display = 'none';
    }

    // Dinner time (6 PM - 8 PM)
    if (hour >= 18 && hour < 20) {
        timeStatus.innerHTML = '✅ Dinner Time is OPEN';
        timeStatus.className = 'time-status open-message';
        dinnerStatus.innerHTML = '<div class="open-message">🌙 Dinner ordering is now OPEN!</div>';
        dinnerMenu.style.display = 'block';
    } else {
        dinnerStatus.innerHTML = '<div class="closed-message">⛔ Dinner ordering is CLOSED<br>Available only between 6:00 PM - 8:00 PM</div>';
        dinnerMenu.style.display = 'none';
    }

    // Default closed status
    if ((hour < 9 || hour >= 11) && (hour < 18 || hour >= 20)) {
        timeStatus.innerHTML = '⏰ Currently CLOSED - Next: ' + (hour < 9 ? 'Lunch at 9:00 AM' : 'Dinner at 6:00 PM');
        timeStatus.className = 'time-status closed-message';
    }
}

// 🍽️ Update Lunch Quantity
function updateLunchQuantity() {
    currentOrder.meal = 'lunch';
    currentOrder.lunchPlates = parseInt(document.getElementById('lunchQuantity').value) || 1;
    showSummary();
}

// 🍞 Update Roti Price (Dinner)
function updateRotiPrice() {
    currentOrder.meal = 'dinner';
    rotiQuantity = parseInt(document.getElementById('rotiQuantity').value) || 0;
    currentOrder.rotiCost = rotiQuantity * rotiPricePerPiece;
    showSummary();
}

// 🌟 Select Special Item
function selectSpecial(itemName, price, mealType) {
    currentOrder.meal = mealType;
    currentOrder.special = itemName;
    currentOrder.specialPrice = price;
    showSummary();
}

// 📋 Show Order Summary
function showSummary() {
    let summaryContent = "";
    let total = 0;

    if (currentOrder.meal === 'lunch') {
        // 🍛 Lunch: plate × 50
        const plates = currentOrder.lunchPlates || 1;
        const basePrice = plates * lunchPlatePrice;
        total = basePrice + (currentOrder.specialPrice || 0);

        summaryContent = `
            <p><strong>Lunch Plates:</strong> ${plates} x ₹${lunchPlatePrice} = ₹${basePrice}</p>
        `;

        if (currentOrder.special) {
            summaryContent += `<p><strong>Special Item:</strong> ${currentOrder.special} (+₹${currentOrder.specialPrice})</p>`;
        }

    } else if (currentOrder.meal === 'dinner') {
        // 🌙 Dinner: Dal + Roti
        const rotiCost = rotiQuantity * rotiPricePerPiece;
        const dalPrice = currentOrder.dalPrice;

        total = dalPrice + rotiCost + (currentOrder.specialPrice || 0);

        summaryContent = `
            <p><strong>Dal:</strong> ₹${dalPrice}</p>
            <p><strong>Roti:</strong> ${rotiQuantity} x ₹${rotiPricePerPiece} = ₹${rotiCost}</p>
        `;

        if (currentOrder.special) {
            summaryContent += `<p><strong>Special Item:</strong> ${currentOrder.special} (+₹${currentOrder.specialPrice})</p>`;
        }
    }

    summaryContent += `
        <hr style="margin: 1rem 0; border: none; height: 2px; background: rgba(255,255,255,0.3);">
        <p style="font-size: 1.2rem;"><strong>Total: ₹${total}</strong></p>
    `;

    currentOrder.total = total;

    document.getElementById('summaryContent').innerHTML = summaryContent;
    document.getElementById('orderSummary').style.display = 'block';
    document.getElementById('orderSummary').scrollIntoView({ behavior: 'smooth' });
}

// 🚀 Confirm Order
function confirmOrder() {
    const name = document.getElementById('customerName').value;
    const phone = document.getElementById('customerPhone').value;
    const address = document.getElementById('customerAddress').value;

    if (!name || !phone || !address) {
        alert('⚠️ Please fill in all your details before confirming the order!');
        return;
    }

    if (!currentOrder.meal) {
        alert('⚠️ Please select a meal first!');
        return;
    }

    // Simulate order confirmation
    alert(`🎉 Order Confirmed!

Customer: ${name}
Phone: ${phone}
Address: ${address}
// chicken curry
Order Details:
- Meal Type: ${currentOrder.meal.charAt(0).toUpperCase() + currentOrder.meal.slice(1)}
- Total Amount: ₹${currentOrder.total}

Thank you for choosing Rik Tiffin House! 
Your delicious meal will be prepared and delivered soon! 🚚`);

    // Reset form
    document.getElementById('orderForm').reset();
    document.getElementById('orderSummary').style.display = 'none';
    currentOrder = { meal: null, special: null, dalPrice: 10, rotiCost: 0, specialPrice: 0, total: 0, lunchPlates: 1 };
    rotiQuantity = 0;
}

// Initial call
updateTimeStatus();
setInterval(updateTimeStatus, 60000);

// Smooth scrolling for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});