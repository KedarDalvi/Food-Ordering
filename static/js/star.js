const ratings = {
  star2 : 2.8,
  hotel_b : 3.3,
  hotel_c : 1.9,
  hotel_d : 4.3,
  hotel_e : 4.74
};

// total number of stars
const starTotal = 5;

for(const rating in ratings) {  
  const starPercentage = (ratings[rating] / starTotal) * 100;
  const starPercentageRounded = `${(Math.round(starPercentage / 10) * 10)}%`;
  document.querySelector(`.${rating} .stars-inner`).style.width = starPercentageRounded; 
}