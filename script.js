document.getElementById("fraudForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent page reload

    // Collect user input
    const amount = document.getElementById("amount").value;
    const transactionType = document.getElementById("transactionType").value;
    const location = document.getElementById("location").value;
    const timeOfDay = document.getElementById("timeOfDay").value; // 0-23 hour

    // Prepare data as JSON
    const data = {
        Amount: parseFloat(amount),
        TransactionType: transactionType,
        Location: location,
        TimeOfDay: parseInt(timeOfDay)
    };

    // Send request to backend
    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.fraud === 1) {
            document.getElementById("result").innerHTML = "🚨 Fraud Detected!";
            document.getElementById("result").style.color = "red";
        } else {
            document.getElementById("result").innerHTML = "✅ No Fraud Detected.";
            document.getElementById("result").style.color = "green";
        }
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("result").innerHTML = "Error detecting fraud!";
        document.getElementById("result").style.color = "orange";
    });
});
