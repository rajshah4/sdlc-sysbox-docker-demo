const list = document.querySelector("#results");
const message = document.querySelector("#message");

function dollars(cents) {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(cents / 100);
}

async function loadPets() {
  const response = await fetch("/api/pets");
  const pets = await response.json();
  const query = document.querySelector("#query").value.trim().toLowerCase();
  const species = document.querySelector("#species").value;
  list.innerHTML = "";

  const matches = pets.filter((pet) =>
    pet.status === "available"
      && pet.name.toLowerCase().includes(query)
      && (species === "" || pet.species === species));

  if (matches.length === 0) {
    list.innerHTML = '<li class="empty">No available pets match this search.</li>';
    return;
  }

  for (const pet of matches) {
    const item = document.createElement("li");
    item.className = "pet";
    item.dataset.petId = pet.id;
    item.innerHTML = `
      <div><strong>${pet.name}</strong><span>${pet.species}</span></div>
      <b>${dollars(pet.adoption_fee_cents)}</b>
      <button class="adopt" data-pet-id="${pet.id}" data-pet-name="${pet.name}">Adopt</button>`;
    list.appendChild(item);
  }
}

async function adopt(petId, petName) {
  message.textContent = `Submitting adoption for ${petName}…`;
  const response = await fetch("/api/adoptions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ pet_id: petId, adopter_email: "demo@example.com" }),
  });
  if (!response.ok) {
    const body = await response.json();
    message.textContent = body.detail || "Adoption could not be completed.";
    return;
  }
  message.textContent = `${petName}'s adoption request was accepted.`;
  await loadPets();
}

document.querySelector("#search-button").addEventListener("click", loadPets);
list.addEventListener("click", (event) => {
  const button = event.target.closest("button.adopt");
  if (button) adopt(button.dataset.petId, button.dataset.petName);
});
loadPets();
