// --- Check if user is logged in ---
const token = localStorage.getItem("token");
console.log("JWT TOKEN:", token);
if (!token) {
    window.location.href = "index.html";
}

// --- Logout ---
const logoutBtn = document.getElementById("logoutBtn");
logoutBtn.addEventListener("click", () => {
    localStorage.removeItem("token");
    window.location.href = "index.html";
});

// --- Elements ---
const transactionForm = document.getElementById("transactionForm");
const transactionList = document.getElementById("transactionList");

// --- Load transactions on page load ---
window.addEventListener("DOMContentLoaded", fetchTransactions);

// --- Add Transaction ---
transactionForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const amount = parseFloat(document.getElementById("amount").value);
    const category = document.getElementById("category").value.trim();
    const description = document.getElementById("description").value;

     // --- Validation ---
    if (isNaN(amount) || category === "") {
        alert("Please enter a valid amount and category.");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/api/transactions", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer" + token
            },
            body: JSON.stringify({
                amount: parseFloat(amount),
                category: category,
                description: description
            })
        });

        const resData = await response.json(); // <--- log everything
        console.log("Transaction response:", response.status, resData);

        if (!response.ok) {
            throw new Error(resData.error || "Failed to add transaction");
        }

        transactionForm.reset();
        fetchTransactions(); // Refresh the list
    } catch (error) {
        console.error(error);
        alert("Error adding transaction: " + error.message);
    }
});

// --- Fetch and display transactions ---
async function fetchTransactions() {
    transactionList.innerHTML = "";

    try {
        const response = await fetch("http://127.0.0.1:5000/api/transactions", {
            method: "GET",
            headers: {
                "Authorization": "Bearer " + token,
                "Content-Type": "application/json"
        }
    });

        if (!response.ok) throw new Error("Failed to fetch transactions");

        const data = await response.json();

        if (data.length === 0) {
            transactionList.innerHTML = "<li>No transactions yet.</li>";
            return;
        }

        data.forEach(tx => {
            const li = document.createElement("li");
            li.textContent = 
            `${tx.amount >= 0 ? "+" : ""}${tx.amount} | ${tx.category} | ${tx.description || ""}| ${tx.date}`;
            transactionList.appendChild(li);
        });
    } catch (error) {
        console.error(error);
        transactionList.innerHTML = "<li>Error loading transactions.</li>";
    }
}