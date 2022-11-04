const updateCartBtns = document.querySelectorAll(".update-cart");

updateCartBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    const productId = btn.dataset.productId;
    const action = btn.dataset.action;

    console.log(`user : ${user}`);
    if (user === "AnonymousUser") {
      updateCookieItem(productId, action);
    } else {
      updateItem(productId, action);
    }
  });
});

const updateCookieItem = (productId, action) => {
  console.log("Adding cookie..");
  if (action == "add") {
    if (cart[productId] == undefined) {
      cart[productId] = { quantity: 1 };
    } else {
      cart[productId].quantity += 1;
    }
  }
  if (action == "remove") {
    cart[productId].quantity -= 1;
    if (cart[productId].quantity <= 0) {
      delete cart[productId];
    }
  }
  setCookie("cart", JSON.stringify(cart), 10);
  console.log(cart);
  location.reload();
};

const updateItem = (productId, action) => {
  url = "/update_item/";
  const postData = async (url, data = {}) => {
    const res = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify(data),
    });
    return res.json();
  };
  postData(url, { productId, action }).then((data) => {
    console.log(data);
    location.reload();
  });
};
