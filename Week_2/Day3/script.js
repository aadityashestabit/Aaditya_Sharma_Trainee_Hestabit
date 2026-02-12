const questionButtons = document.querySelectorAll(".faq-question");

questionButtons.forEach((button) => {
  button.addEventListener("click", () => {

    const currentCard = button.closest(".faq-card");

    // Close other open cards
    document.querySelectorAll(".faq-card").forEach((card) => {
      if (card !== currentCard) {
        card.classList.remove("open");
        card.querySelector(".toggle-symbol").textContent = "+";
      }
    });

    // Toggle current card
    currentCard.classList.toggle("open");

    const symbol = button.querySelector(".toggle-symbol");
    symbol.textContent = currentCard.classList.contains("open") ? "-" : "+";

  });
});
