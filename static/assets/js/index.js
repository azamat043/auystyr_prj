// <!-- Initialize Swiper -->
  let swiper = new Swiper(".mySwiper", {
    slidesPerView: 1,
    spaceBetween: 0,
    slidesPerGroup: 1,
    loop: true,
    loopFillGroupWithBlank: true,
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    breakpoints: {
      // when window width is >= 640px
      900: {
          slidesPerView: 3,
          spaceBetween: 155,
          slidesPerGroup: 3,
          slideToClickedSlide: true,
      },
      700: {
        slidesPerView: 2,
        spaceBetween: 0,
        slidesPerGroup: 1,
        slideToClickedSlide: true,
      }
  }
  });
  
