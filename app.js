const API_URL = "https://my-simpleai-ordas.vercel.app";
const API_KEY = "my_secret_landmark_key";

const FETCH_OPTIONS = {
    headers: { "x-api-key": API_KEY }
};

// BUILD A FULL IMAGE URL 
function getImageUrl(icon) {
    if (!icon || icon.trim() === "") return "";
    if (icon.startsWith("http")) return icon; 

    
    if (icon.includes("images/")) {
        
        return icon.startsWith("/") ? icon.substring(1) : icon;
    } else {
        
        const cleanIcon = icon.startsWith("/") ? icon.substring(1) : icon;
        return `images/${cleanIcon}`;
    }
}

// GET ALL LANDMARKS
async function loadLandmarks() {
    const landmarkList = document.getElementById("landmarkList");
    landmarkList.innerHTML = `
        <div class="loading-state">
            <div class="spinner"></div>
            <p>Loading landmarks...</p>
        </div>
    `;

    try {
        const response = await fetch(`${API_URL}/landmarks`, FETCH_OPTIONS);
        const data = await response.json();
        displayLandmarks(data.landmarks);
    }
    catch (error) {
        console.error(error);
        landmarkList.innerHTML = "Unable to connect to the API.";
    }
}

// DISPLAY LANDMARKS 
function displayLandmarks(landmarks) {
    const landmarkList = document.getElementById("landmarkList");
    landmarkList.innerHTML = "";

    
    if (landmarks.length === 0) {
        landmarkList.innerHTML = `<p class="no-results">No landmarks found. Try a different search.</p>`;
        return;
    }

    landmarks.forEach((landmark, index) => {
        const card = document.createElement("div");
        card.className = "landmark-card";
        
        card.style.animationDelay = `${index * 0.05}s`;

        
        const hasIcon = landmark.icon && landmark.icon.trim() !== "";
        const iconHTML = hasIcon
            ? `<img src="${getImageUrl(landmark.icon)}" alt="${landmark.title}" class="landmark-icon" onerror="this.outerHTML='<div class=\\'landmark-icon no-image\\'></div>'">`
            : `<div class="landmark-icon no-image"></div>`;

        card.innerHTML = `
            ${iconHTML}
            <div class="card-info">
                <h3>${landmark.title}</h3>
                <div class="landmark-location">${landmark.country} • ${landmark.region}</div>
                <span class="type-badge">${landmark.site_type}</span>
                <p><strong>Rating:</strong> ${landmark.visitor_rating}</p>
                <p><strong>Fee:</strong> ${landmark.entry_fee}</p>
                <button onclick="viewLandmark(${landmark.id})"> View Details </button>
            </div>
        `;
        landmarkList.appendChild(card);
    });
}

// GET ONE LANDMARK 
async function viewLandmark(id) {
    try {
        const response = await fetch(`${API_URL}/landmarks/${id}`, FETCH_OPTIONS);
        const landmark = await response.json();

        const modalBody = document.getElementById("modalBody");

        // 
        const hasIcon = landmark.icon && landmark.icon.trim() !== "";
        const heroHTML = hasIcon
            ? `
                <div class="modal-hero" style="background-image: url('${getImageUrl(landmark.icon)}');">
                    <div class="modal-hero-overlay"></div>
                    <div class="modal-hero-text">
                        <h2>${landmark.title}</h2>
                        <p>${landmark.country} | ${landmark.region}</p>
                    </div>
                </div>
            `
            : `
                <div class="modal-hero no-image"></div>
                <h2 style="margin: 15px 0 0 0; color: #1f1f1f;">${landmark.title}</h2>
                <p style="color: #555; margin-top: 5px;">${landmark.country} | ${landmark.region}</p>
            `;

        modalBody.innerHTML = `
            ${heroHTML}
            <div class="modal-grid">
                <div class="modal-item"><strong>Established:</strong> ${landmark.established_year}</div>
                <div class="modal-item"><strong>Type:</strong> ${landmark.site_type}</div>
                <div class="modal-item"><strong>Rating:</strong> ${landmark.visitor_rating}</div>
                <div class="modal-item"><strong>Visitors/Yr:</strong> ${landmark.annual_visitors}</div>
                <div class="modal-item"><strong>Entry Fee:</strong> ${landmark.entry_fee}</div>
                <div class="modal-item"><strong>Architects:</strong> ${landmark.notable_architects}</div>
                <div class="modal-item"><strong>Governing Body:</strong> ${landmark.governing_body}</div>
                <div class="modal-item"><strong>Protection:</strong> ${landmark.protection_status}</div>
                
                <div class="modal-desc">
                    <strong>Description:</strong><br>
                    ${landmark.description}
                </div>
            </div>
        `;

        // Show the modal
        document.getElementById("landmarkModal").classList.add("show");
    }
    catch (error) {
        console.error(error);
        alert("Unable to retrieve landmark.");
    }
}

// CLOSE MODAL FUNCTION
function closeModal() {
    document.getElementById("landmarkModal").classList.remove("show");
}

// CLOSE MODAL WHEN CLICKING OUTSIDE THE BOX
window.onclick = function(event) {
    const modal = document.getElementById("landmarkModal");
    if (event.target === modal) {
        closeModal();
    }
};

// SEARCH
async function searchLandmarks() {
    const query = document.getElementById("searchInput").value;
    if (!query) {
        loadLandmarks();
        return;
    }
    try {
        const response = await fetch(`${API_URL}/landmarks/search?q=${encodeURIComponent(query)}`, FETCH_OPTIONS);
        const data = await response.json();
        displayLandmarks(data.results);
    }
    catch (error) {
        console.error(error);
        alert("Search failed.");
    }
}

// SEARCH ON ENTER KEY
document.getElementById("searchInput").addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        searchLandmarks();
    }
});

loadLandmarks();