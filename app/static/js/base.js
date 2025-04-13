// Profile dropdrown
function openProfile() {
  document.getElementById("user-profile-dropdown").classList.toggle("hidden");
}

document.addEventListener("mousedown", function(event) {
  const profileBtn = document.querySelector('.profile-btn');
  const dropdown = document.getElementById("user-profile-dropdown");
  if (!profileBtn.contains(event.target)) {
    dropdown.classList.add("hidden");
  }
});

// Shop dropdown
function openShop() {
  document.getElementById("dropdownNavbar").classList.toggle("hidden")
}
document.addEventListener("mousedown", function(event) {
  const shopBtn = document.querySelector('button[onclick="openShop()"]');
  const dropdown = document.getElementById("dropdownNavbar");
  if (!shopBtn.contains(event.target) && !dropdown.contains(event.target)) {
    dropdown.classList.add("hidden");
  }
});


let slideIndex = 0;
showSlides();

function showSlides() {
  let i;
  let slides = document.getElementsByClassName("img-slide");

  for (i = 0; i < slides.length; i++) {
    slides[i].classList.remove("opacity-100");
    slides[i].classList.add("opacity-0");
  }
  slideIndex++;
  if (slideIndex > slides.length) {
    slideIndex = 1;
  }

  slides[slideIndex-1].classList.remove("opacity-0");
  slides[slideIndex-1].classList.add("opacity-100");
  setTimeout(showSlides, 3000);
}



// carousel slide
// document.addEventListener("DOMContentLoaded", function() {
//   const items = document.querySelectorAll('[data-carousel-item]');
//   let currentIndex = 0;

//   function showImg(index) {
//     items.forEach((item, i) => {
//       item.classList.add('hidden');
//       if (i == index) {
//         item.classList.remove('hidden');
//       }
//     });
//   }

//   function nextImg() {
//     currentIndex = (currentIndex + 1) % items.length;
//     showImg(currentIndex);
//   }

//   function prevImg() {
//     currentIndex = (currentIndex - 1 + items.length) % items.length;
//     showImg(currentIndex);
//   }

//   document.querySelector('[data-carousel-next]').addEventListener('click', nextImg);
//   document.querySelector('[data-carousel-prev]').addEventListener('click', prevImg);

//   showImg(currentIndex);

// });


// เพิ่ม ลบ สินค้า

$('.increment-button').click(function() {
  var id = $(this).attr('itemid').toString();
  var qan = this.parentNode.children[1]

  console.log('item id = ', id)
  $.ajax({
    type: "GET",
    url: "/increaseitem",
    data: {
      item_id: id
    },
    success:function(data) {
      console.log("data = ", data);
      qan.innerText = data.quantity
      document.getElementById("amount").innerText = data.amount
      document.getElementById("total_amount").innerText = data.total_amount
      document.getElementById("total_saving").innerText = data.total_saving
    }
  })
})

$('.decrement-button').click(function() {
  var id = $(this).attr('itemid').toString();
  var qan = this.parentNode.children[1]
  currentqan = parseInt(qan.innerText)

  if (currentqan == '1') {
    return;
  }


  console.log('item id = ', id)
  $.ajax({
    type: "GET",
    url: "/decreaseitem",
    data: {
      item_id: id
    },
    success:function(data) {
      console.log("data = ", data);
      qan.innerText = data.quantity
      document.getElementById("amount").innerText = data.amount
      document.getElementById("total_amount").innerText = data.total_amount
      document.getElementById("total_saving").innerText = data.total_saving
    }
  })
})

$('.remove-button').click(function() {
  var id = $(this).attr('itemid').toString();
  var qan = this
  $.ajax({
    type: "GET",
    url: "/removeitem",
    data: {
      item_id: id
    },
    success:function(data) {
      console.log("data = ", data);
      document.getElementById("amount").innerText = data.amount
      document.getElementById("total_amount").innerText = data.total_amount
      document.getElementById("total_saving").innerText = data.total_saving
      qan.parentNode.parentNode.parentNode.parentNode.remove()
    }
  })
})


$('.add-wishlist').click(function() {
  var id = $(this).attr("item_id").toString();
  $.ajax({
    type:"GET",
    url:"/addwishlist",
    data:{
      item_id:id
    },
    success:function(data) {
      window.location.href = `http://127.0.0.1:8000/item-details/${id}`
    }
  })
})

$('.remove-wishlist').click(function() {
  var id = $(this).attr("item_id").toString();
  $.ajax({
    type:"GET",
    url:"/removewishlist",
    data:{
      item_id:id
    },
    success:function(data) {
      window.location.href = `http://127.0.0.1:8000/item-details/${id}`
    }
  })
})