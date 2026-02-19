// Now we wanna create a UI Client Side to create for 


// Fix these syntax errors later
const ctx = document.getElementById('stockGraph').getContext('2d');

// Graph for the Stock
let myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: chartLabels, // From my Django connected via stock.html
        datasets: [{
            label: `${stockTicker} Price`,
            data: chartPrices, 
            borderColor: '#3b82f6',
            fill: true,
            tension: 0.1,
            backgroundColor: graph_colour(),
        }]
    },
    options: {
        responsive: true,          
        maintainAspectRatio: false, 
        scales: {
            x: {
                ticks : {
                    maxTicksLimit: 10,
                    autoSkip: true

                },
                grid: {
                    display: false

                }
            }

        },
    }
});

function graph_colour() {
    const currentPrice = chartPrices[chartPrices.length - 1];
    const previousPrice = Chart_yesterday_price;
    // Stock currentPrice should be green!
    if (currentPrice > previousPrice) return '#36ff0f';

    // If the price of the stock is same, return blue (normal colour:)
    else if (currentPrice === previousPrice) return '#7df0ff';

    // Else it should be red
    else return '#FF3131';



    
}
console.log(myChart.data.datasets[0].data, "HI");



graph_colour();

// Buttoms
const buttons = document.querySelectorAll('.interval')

function buttonUpdate() {
    buttons.forEach(btn => {
        btn.addEventListener('click', async function() {
            buttons.forEach(b => {
                b.classList.remove('bg-blue-500', 'text-white'); 
                b.classList.add('text-gray-950');
            });

            this.classList.remove( 'text-gray-950');
            this.classList.add('bg-blue-500', 'text-white');

            const interval = this.getAttribute('data-interval');
            // console.log("Fetching data for:", interval);
        const response = await fetch(`/api/json_data_api/${stockTicker}/${interval}/`);

        const data = await response.json();
    
        myChart.data.labels = data.labels;
        
        myChart.data.datasets[0].data = data.prices.map(Number);
        myChart.data.datasets[0].data = data.prices.map(Number);
        // borderColor
        
        myChart.update();



        });
    });
}
buttonUpdate();

// Graph Animation
gsap.from(ctx, {
    opacity: 0,
    y: 50,
    duration: 1.5,
    ease: 'power3.out',
})

setInterval(StockUpdate, 3000);
StockUpdate();


const PriceData = document.querySelector(".livePrice"); 

async function StockUpdate(){
    // Grab update on Stock Price by calling our urls.py that is connected with our views
    const symbolPrice = await fetch(`/api/latest-price/${stockTicker}/`);
    // Return in JSON
    const data = await symbolPrice.json();

    // Error Handling
    if (!PriceData || data === undefined) return;   
    // Parse it into a float for JS
    const newPrice = parseFloat(data.price);
    const oldPrice = parseFloat(PriceData.dataset.last || newPrice);

    PriceData.dataset.last = newPrice;
    PriceData.innerText = `$${newPrice.toFixed(2)}`; 
    // Inspired by Yahoo Finance:
    if (newPrice > oldPrice){
        PriceData.classList.add('text-green-600');
        setTimeout(() => PriceData.classList.remove('text-green-600'), 500);
    } 
    else if (newPrice < oldPrice) {
        PriceData.classList.add('text-red-600'); 
        setTimeout(() => PriceData.classList.remove('text-red-600'), 500);
    }

    



}
// Grab the Card div to create a gsap animation



const cards = document.querySelectorAll('.flexcard')


// Animation :)

gsap.from(cards, {
    opacity: 0,
    y: 100,
    duration: 1.5,
    ease: 'power3.out',
    onUpdate() {
         chart.update('none')
    }

})


// Create a function to grab the colors of the bullish indicator
const score = points

function pieGraphColor(score) {
  if (score < 20) return '#d32f2f';
  if (score < 40) return '#f57c00';
  if (score < 60) return '#fbc02d';
  if (score < 80) return '#7cb342';
  return '#2e7d32';
}


// Add centre text for bulish indicator
const centerText = {
  id: 'centerText',
  afterDraw(chart) {
    const { ctx, chartArea: { width, height } } = chart;
    ctx.save();


    ctx.font = 'bold 12px sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('Bullish Indicator', width / 2, height / 2 - 30);


    //  Muddle
    ctx.font = 'bold 26px sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.fillText(`${score}%`, width / 2, height / 2) ;

    // Subtitle 
    ctx.font = ' 14px sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.fillText(`Bullish Score`, width / 2, height / 2 + 28) ;
    ctx.restore();
  }
};




// Grab the chart for bullish indicator
const ctx_chart = document.getElementById("bullishIndicator")

const chart = new Chart(ctx_chart, {
    type: "doughnut",
    plugins: [centerText],
    data: {                                  
        datasets: [{
            data: [0.001, 99.999],
            backgroundColor: [pieGraphColor(score), "#eeeeee"],
            borderWidth: 0
        }]
    },
});


let animation_score = {v: 0}

gsap.to(animation_score, {
    v: score,
    duration: 1.5,
    ease: 'power3.out',
    onUpdate(){
        const v = Math.max(animation_score.v, 0.0001);

        chart.data.datasets[0].data = [v, 100 - v];
        chart.data.datasets[0].backgroundColor = [pieGraphColor(v), '#222831'];

        chart.update('none');
    }
})

// Breakdown. We would use onUpdate() on our chart.js for doughnut and we shuld have our value empty first, so data is [0,100] and append the score on [0] index. Data[0, 100 - score]



// Grab the div class for the sales buttons, etc.




const buy_button = document.getElementById('buy-button');
const sell_button = document.getElementById('sell-button');
const text_changer = document.getElementById('text-changer');
const input_changer = document.getElementById('input-changer');
const button_execute_order = document.getElementById('button-execute');
const form_execution = document.getElementById('form_execute');
const strong_changer_total = document.getElementById('strong-changer-total');
const execute = document.getElementById('button-execute');

const max_button = document.getElementById('button-max');


// If the button is clicked, we want to also grab the url for the stockOrders which will be worked on early (so we're gonna add that feature later)
buy_button.addEventListener('click', async (e) => {
    e.preventDefault();
    text_changer.innerHTML =  `Buy some ${stockTicker}`;
    input_changer.placeholder = `Buy some ${stockTicker}`;
    button_execute_order.innerHTML = `BUY`;

    // Do the logic of buttons
    buy_button.classList.replace('bg-blue-700', 'bg-blue-400');
    sell_button.classList.replace('bg-blue-400', 'bg-blue-700');
    // const order =  fetch(`trade/<str:ticker>/<str:order_type>/`)

    form_execution.action = `/trade/${stockTicker}/BUY/`;
    strong_changer_total.innerHTML = 'Total Cost: '
})


sell_button.addEventListener('click', (e) => {
    e.preventDefault();
    text_changer.innerHTML =  `Sell some ${stockTicker}`;
    input_changer.placeholder = `Sell some ${stockTicker}`;

    // Do the logic of buttons
    sell_button.classList.replace('bg-blue-700', 'bg-blue-400');
    buy_button.classList.replace('bg-blue-400', 'bg-blue-700');
    button_execute_order.innerHTML = `SELL`;
    form_execution.action = `/trade/${stockTicker}/SELL/`;
    strong_changer_total.innerHTML = 'Total Value: '



})


max_button.addEventListener('click', async () => {
    const res = await fetch(`/api/latest-price/${stockTicker}/`);
    const data = await res.json();
    const price = parseFloat(data.price);
    // Formula for how many shares a user can buy max: (Floor(User_capital / price) * 10000) / 10000

    if (button_execute_order.innerText === 'BUY') {
        const maxShares =
            Math.floor((user_capital / price) * 10000) / 10000;

        input_changer.value = maxShares;
        sharesInput.innerText =
            `Total Cost: $${(maxShares * price).toFixed(2)}`;
    }
    // This one is fairly easy, as we can just use how many shares the user has as the max shares they can sell.
    if (button_execute_order.innerText === 'SELL') {
        input_changer.value = shares;
        sharesInput.innerText =
            `Total Value: $${(shares * price).toFixed(2)}`;
    }
});

// So what we wanna do is add a confirmation using swal js package, and also notification after it.


// https://sweetalert2.github.io/ REMINDER
form_execution.addEventListener('submit', function(e) {
    e.preventDefault();
    //  Grab Button: Are you sure you wanna `${action}` `${amount}` of stock?



    const action = button_execute_order.innerText
    const amount =  input_changer.value || input_changer.innerText;

    // Mandatory for confirmation.
    Swal.fire({
    title: 'Confirm Order',
    text: `Are you sure you want to ${action} ${amount} shares of ${stockTicker}?`,
    showDenyButton: true,
    confirmButtonText: 'Yes, execute the order',
    denyButtonText: `No, please don't excute the order`,
    customClass: {
        actions: 'my-actions',
        confirmButton: 'order-1',
        denyButton: 'order-1',
    },
    }).then((result) => {
    if (result.isConfirmed) {
        sessionStorage.setItem('orderStatus', 'success'); 
        sessionStorage.setItem('orderMessage', `Successfully executed ${action} ${amount} of ${stockTicker}!`);
        form_execution.submit(); 
        sessionStorage.setItem('lastAmount', amount);

    } else if (result.isDenied) {
        Swal.fire('Order cancelled', '', 'info');
    }
    })

})

// Fetch the data for the buttons later, and put it inside the eventlistener :)

// Fetched from the form_execution data
document.addEventListener('DOMContentLoaded' , async () =>{

    const status = sessionStorage.getItem('orderStatus');
    const message = sessionStorage.getItem('orderMessage');
    const amount = sessionStorage.getItem('lastAmount');
        //  We don't need to fetch the data for the current price everytime. Therefore we don't need to have it as async function because of this situation.

    const data_stock = await fetch(`/api/latest-price/${stockTicker}/`);
    const response =await  data_stock.json();
    
    const currentPrice = parseFloat(response.price);
    
    const current_value = (currentPrice * amount);
    // If the current value is lower than the user's capital, it will do a rejection

    if( current_value > user_capital) {
            Swal.fire({
            icon: status, // 'success', 'info', 'warning', 'error', 'question'
            title: 'Not Enough Cpaital',
            text:  `You don't have enough capital to buy ${stockTicker}!`,
            timer: 3000, 
            showConfirmButton: false,
            position: 'top-end', 
            toast: true
        });
        sessionStorage.clear();
            return;
        

    }

    if (status && message) {
        Swal.fire({
            icon: status, // 'success', 'info', 'warning', 'error', 'question'
            title: 'Notification',
            text: message,
            timer: 3000, 
            showConfirmButton: false,
            position: 'top-end', 
            toast: true
        });
        
        // Clear the storage immediately after showing the alert
        sessionStorage.removeItem('orderStatus');
        sessionStorage.removeItem('orderMessage');
        sessionStorage.removeItem('lastAmount');
    }
    
    //  We don't need to fetch the data for the current price everytime. Therefore we don't need to have it as async function because


});


const sharesInput = document.getElementById('total-cost');

// We want to have a dynamic UI by adding a input event so we can have user know how much it will cost for them to buy the stock
input_changer.addEventListener('input', async() => {
    const res = await fetch(`/api/latest-price/${stockTicker}/`);
    const data = await res.json();
    cachedPrice = parseFloat(data.price);


    const shares = parseFloat(input_changer.value);
    if (!shares || shares <= 0) {
        sharesInput.innerText = " Total Cost: $0.00";
        return;
    }
    const total = shares * cachedPrice;
    sharesInput.innerText = `Total Cost: $${total}`;
});

const totalReturn = document.getElementById('total-return')

async function grab_current_value(){
        // #  ROI = [(Current Value / Average Cost) - 1] x 100%


// # Current value = Current_price * Shares owned
// Fetch current price
    const data = await fetch(`/api/latest-price/${stockTicker}/`)

    const response = await data.json();

    const currentPrice = parseFloat(response.price);
    // Placeholder for if statement
    
    const current_value = (currentPrice * shares) 

    const totalCost = average_cost * shares

    console.log(currentPrice)

    const return_on_investment =  ((current_value / totalCost) - 1) * 100;

    console.log(return_on_investment)
    const colour = return_on_investment < 0 ? "#FF0000" : "#00FF00";

    totalReturn.innerHTML = `
         <strong>Total Return:</strong>
         <span style="color:${colour}">
         ${return_on_investment.toFixed(2)}%
         </span>
    `



};

setInterval(grab_current_value, 10000);

grab_current_value();



// I am creating a CAPM data for visualization


const capm_chart = document.getElementById('capmGraph');





const centerTextCAPM = {
  id: 'centerText',
  afterDraw(chart) {
    const { ctx, chartArea: { width, height } } = chart;
    ctx.save();


    ctx.font = 'bold 12px sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('Risk Indicator', width / 2, height / 2 - 30);


    //  Muddle
    ctx.font = 'bold 26px sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.fillText(`${scoreOfCapm}%`, width / 2, height / 2) ;

    // Subtitle 
    ctx.font = ' 14px sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.fillText(`Risk Score`, width / 2, height / 2 + 28) ;
    ctx.restore();
  }
};


// Reverse the logic, and change the colour of the pie graph, because ofc, lower risk the safter the investment is :)
function pieGraphColortwo(score) {
  if (score < 20) return '#2e7d32';
  if (score < 40) return '#7cb342'; 
  if (score < 60) return '#fbc02d';
  if (score < 80) return '#f57c00';
  return '#d32f2f';                 
}

// Copy the same logic from the other doughnut chart

const capm = new Chart(capm_chart, {
    type: "doughnut",
    plugins: [centerTextCAPM],
    data: {                                  
        datasets: [{
            data: [scoreOfCapm, 100 - scoreOfCapm],
            backgroundColor: [pieGraphColortwo(scoreOfCapm), "#222831"],
            borderWidth: 0
        }]
    },
});