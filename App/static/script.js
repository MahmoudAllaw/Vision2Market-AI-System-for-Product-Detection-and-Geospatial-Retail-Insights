document.getElementById("uploadForm").addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(this);

    const response = await fetch("/detect", { method: "POST", body: formData });
    const result = await response.json();

    if (result.error) {
        alert(result.error);
        return;
    }

    const product = result.product;
    const data = result.data;

    document.getElementById("productTitle").textContent = `Detected Product: ${product}`;
    const listContainer = document.getElementById("productList");
    listContainer.innerHTML = "";

    let map = L.map("map").setView([25.276987, 55.296249], 10);
    L.tileLayer("https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: "© OpenStreetMap contributors"
    }).addTo(map);

    const bounds = [];

    data.forEach(item => {
        const listItem = document.createElement("div");
        listItem.classList.add("list-item");

        listItem.innerHTML = `
            <div class="item-row">
                <span class="market">${item.Market || "Unknown"}</span>
                <span class="price">${item.Price}</span>
            </div>
            <div class="desc">${item.Description || ""}</div>
            ${item.URL ? `<div class="link"><a href="${item.URL}" target="_blank">View Source</a></div>` : ""}
        `;
        listContainer.appendChild(listItem);

        if (item.Latitude && item.Longitude) {
            const marker = L.marker([item.Latitude, item.Longitude])
                .addTo(map)
                .bindPopup(`<b>${item.Market}</b><br>${item.Price}`);
            bounds.push([item.Latitude, item.Longitude]);
        }
    });

    if (bounds.length > 0) {
        map.fitBounds(bounds, { padding: [30, 30] });
    }
});
