document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Static activities data (replacing API fetch)
  const activities = {
    "Basketball": {
      description: "Competitive basketball team for all skill levels.",
      schedule: "Tuesdays and Thursdays, 4-6 PM",
      max_participants: 20,
      participants: ["alex.johnson@mergington.edu", "jordan.smith@mergington.edu", "casey.williams@mergington.edu", "morgan.brown@mergington.edu"]
    },
    "Soccer": {
      description: "School soccer team with training and matches.",
      schedule: "Mondays and Wednesdays, 3-5 PM",
      max_participants: 22,
      participants: ["sam.davis@mergington.edu", "taylor.martinez@mergington.edu", "riley.garcia@mergington.edu"]
    },
    "Drama Club": {
      description: "Explore acting, scriptwriting, and stage production.",
      schedule: "Fridays, 5-7 PM",
      max_participants: 15,
      participants: ["emma.anderson@mergington.edu", "noah.thompson@mergington.edu", "olivia.jackson@mergington.edu", "liam.white@mergington.edu", "sophia.harris@mergington.edu"]
    },
    "Art Club": {
      description: "Creative sessions for painting, drawing, and crafts.",
      schedule: "Wednesdays, 4-6 PM",
      max_participants: 18,
      participants: ["ava.martin@mergington.edu", "ethan.lee@mergington.edu", "isabella.perez@mergington.edu"]
    },
    "Chess Club": {
      description: "Strategic games and tournaments for chess enthusiasts.",
      schedule: "Tuesdays, 5-7 PM",
      max_participants: 12,
      participants: ["mason.clark@mergington.edu", "amelia.rodriguez@mergington.edu", "lucas.lewis@mergington.edu", "mia.walker@mergington.edu", "benjamin.hall@mergington.edu", "charlotte.allen@mergington.edu"]
    },
    "Debate Club": {
      description: "Practice public speaking and argumentation skills.",
      schedule: "Thursdays, 4-6 PM",
      max_participants: 16,
      participants: ["henry.young@mergington.edu", "harper.king@mergington.edu", "alexander.wright@mergington.edu"]
    }
  };

  // Function to load activities from static data
  function loadActivities() {
    // Clear loading message
    activitiesList.innerHTML = "";

    // Populate activities list
    Object.entries(activities).forEach(([name, details]) => {
      const activityCard = document.createElement("div");
      activityCard.className = "activity-card";

      const spotsLeft = details.max_participants - details.participants.length;
      
      // Build participants list HTML
      const participantsList = details.participants.length > 0
        ? `<ul>${details.participants.map(p => `<li>${p}</li>`).join("")}</ul>`
        : "<p><em>No participants yet</em></p>";

      activityCard.innerHTML = `
        <h4>${name}</h4>
        <p>${details.description}</p>
        <p><strong>Schedule:</strong> ${details.schedule}</p>
        <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
        <div class="participants-section">
          <strong>Current Participants:</strong>
          ${participantsList}
        </div>
      `;

      activitiesList.appendChild(activityCard);

      // Add option to select dropdown
      const option = document.createElement("option");
      option.value = name;
      option.textContent = name;
      activitySelect.appendChild(option);
    });
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  loadActivities();
});
