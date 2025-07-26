document.getElementById("bundle-form").addEventListener("submit", function (e) {
    e.preventDefault();
    const form = new FormData(this);

    fetch("/run", {
        method: "POST",
        body: form
    })
    .then(res => res.json())
    .then(data => {
        const div = document.getElementById("result");
        div.innerHTML = `
            <h3>Bundle Result</h3>
            <p><strong>Bundle Size:</strong> ${data.bundle_size}</p>
            <p><strong>Total Cost:</strong> ₹${data.total_cost}</p>
            <p><strong>Total Weight:</strong> ${data.total_weight} kg</p>
            <p><strong>Total Value:</strong> ${data.total_value}</p>
            <p><strong>Fitness Score:</strong> ${data.fitness_score}</p>
            <h4>Selected Products:</h4>
            <ul>${data.products.map(p => `<li>${p}</li>`).join("")}</ul>
        `;
    });
});
