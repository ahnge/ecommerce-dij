const updateCartBtns = document.querySelectorAll(".update-cart");

updateCartBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    const productId = btn.dataset.productId;
    const action = btn.dataset.action;

    console.log(`user : ${user}`);
    if (user === "AnonymousUser") {
      console.log("User is not loggin");
    } else {
      updateItem(productId, action);
    }
  });
});

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
    console.log("i ran");
    location.reload();
  });
};
