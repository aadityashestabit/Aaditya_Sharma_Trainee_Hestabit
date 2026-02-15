const container = document.getElementById("productsContainer");
const searchInput = document.getElementById("searchInput");
const sortBtn = document.getElementById("sortBtn");

let allProducts = [];
let currentProducts = [];

async function fetchProducts() {
  const res = await fetch("https://dummyjson.com/products?limit=20");
  const data = await res.json();

  allProducts = data.products;
  currentProducts = [...allProducts];

  renderProducts(currentProducts);
}

function renderProducts(products) {
  container.innerHTML = "";

  products.forEach((product) => {
    const card = document.createElement("div");
    card.classList.add("product-card");

    card.innerHTML = `
      <div class="product-img">
        <img src="${product.thumbnail}" alt="${product.title}">
      </div>
      <div class="product-info">
        <h3>${product.title}</h3>
        <div class="rating">★★★★★</div>
        <div class="price">$${product.price}</div>
      </div>
    `;

    container.appendChild(card);
  });
}

searchInput.addEventListener("input", () => {
  const searchTerm = searchInput.value.toLowerCase();

  currentProducts = allProducts.filter((product) =>
    product.title.toLowerCase().includes(searchTerm),
  );

  renderProducts(currentProducts);
});

sortBtn.addEventListener("click", () => {
  currentProducts.sort((a, b) => b.price - a.price);
  renderProducts(currentProducts);
});

fetchProducts();
