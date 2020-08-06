let cake_list = document.querySelector(".list-group");

// FUNCTIONALITY FOR DELETE BUTTONS:
const delete_buttons = document.querySelectorAll(".delete-cupcake");

for (button of delete_buttons) {
  button.addEventListener("click", deleteCupcake);
}

async function deleteCupcake() {
  const id = this.dataset.id;
  await axios.delete(`/api/cupcakes/${id}`);
  this.parentElement.remove();
}

// FUNCTIONALITY FOR HANDLING FORM:
const new_cake_button = document.querySelector(".add-cupcake");

new_cake_button.addEventListener("click", appendCupcake);

async function addCupcake() {
  event.preventDefault();
  const formData = new FormData(new_cake_form);

  const flavor = formData.get("flavor");
  const size = formData.get("size");
  const rating = formData.get("rating");
  const image = formData.get("image");

  const JSONObj = {
    flavor: flavor,
    size: size,
    rating: rating,
    image: image,
  };

  const response = await axios.post("/api/cupcakes", JSONObj);
  return response
}

async function appendCupcake() {
    const response = await addCupcake();
    
    const cake = response.data.cupcake;

    const new_li = document.createElement('li');
    new_li.classList.add('list-group-item');
    new_li.innerText = `${cake.flavor} `;

    const remove_button = document.createElement('button');
    remove_button.innerText = 'X';
    remove_button.dataset.id = cake.id;
    remove_button.addEventListener("click", deleteCupcake);

    new_li.append(remove_button);
    cake_list.append(new_li);
}