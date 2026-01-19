const canveses_port = document.querySelectorAll('.stockGraph');


canveses_port.forEach((canvas, index) => {
    const stock = portfolioStocks[index];
    console.log("This is", stock.ticker, stock.price);
    console.log(stock);
    canvas.addEventListener('click', () => {
        window.location.href = `/stock/${stock.ticker}/`;
    });

    //  I'll just add the same graph from the search.js, and configure it accordingly
    new Chart(canvas, {
        type: 'line',
       
        data: {           
            labels: stock.date.map((_, i) => i), 
            datasets: [{
                label: stock.ticker,
                data:  stock.price,       
                borderColor: colour_graph(),
                backgroundColor: colour_graph(),
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            plugins: {
                legend: { display: false }      
            },

        }
    });

    // Grab this script from stock.js
    function colour_graph() {
    // Stock currentPrice should be green!
    if (stock.current_price > stock.yesterday_price) return '#36ff0f';

    // If the price of the stock is same, return blue (normal colour:)
    else if (stock.current_price === stock.yesterday_price) return '#7df0ff';

    // Else it should be red
    else return '#FF3131';

    }



    


});


// Reminder, our json is here: portfolioStocks


const ctx = document.getElementById('portfolioGraph');
const masterLabels = portfolioStocks[0].date;
console.log(masterLabels)
// Now we should make an array for the stocks, manipulate them using foreach and multiply each indexes by the quantity.
let ValuePortfolio = new Array(masterLabels.length).fill(0);

// Iterate through the stock/ticker price and we should be able to grab their associated quantity and prices
portfolioStocks.forEach(stock => {
    const quantity = stock.quantity;
    const priceHistory = stock.price;
    // In order to manipulate the stock ticker data and ensure we multiply with its assocaited index, we must iterate through priceHistory
    priceHistory.forEach((stockPrice, index) => {
        if (index < ValuePortfolio.length) {
            ValuePortfolio[index] += parseFloat(stockPrice) * quantity;
        }
    });
});





console.log(ValuePortfolio);
console.log("CTX:", ctx);


const mainPortfolioChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: masterLabels, 
        datasets: [{
            label: 'Portfolio Value',
            data: ValuePortfolio, 
            borderColor: '#3b82f6',
            fill: true,
            tension: 0.1,
            backgroundColor: 'rgba(59, 130, 246, 0.2)',
            pointRadius: 0
        }]
    },
    options: {
        responsive: true,           
        maintainAspectRatio: false, 
        scales: {
            x: {
                ticks: {
                    maxTicksLimit: 10,
                    autoSkip: true
                },
                grid: {
                    display: false
                }
            },
            y: {
                beginAtZero: false, 
                ticks: {
                    callback: function(value) {
                        return '$' + value.toLocaleString();
                    }
                }
            }
        },
        plugins: {
            legend: { display: false }
        }
    }
});


// We grab the buttons: We can use our stock.js and apply it accordingly!


const buttons = document.querySelectorAll('.interval')

function buttonUpdate() {
    buttons.forEach(btn => {
        btn.addEventListener('click', async function() {
            buttons.forEach(b => {
                b.classList.remove('text-white'); 
                b.classList.add('text-gray-950');
            });

            this.classList.remove('text-gray-950');
            this.classList.add('text-white');

            const interval = this.getAttribute('data-interval');

            let period;
            if (interval === '1D') { period = '1d'; step}
            else if (interval === '1W') { period = '5d'; }
            else if (interval === '1M') { period = '1mo';  }
            else if (interval === '1Y') { period = '1y';}
            // console.log("Fetching data for:", interval);
        const response = portfolioStocks.map(stock => 
                    fetch(`/api/json_data_api/${stock.ticker}/${period}/`).then(res => res.json())
                );

        const data = await Promise.all(response);

        const newLabels = data[0].labels;
    
        let newPortfolioValues = new Array(newLabels.length).fill(0);
        
        data.forEach((stock, stockIndex) => {
            const qty = portfolioStocks[stockIndex].quantity;
            stock.price.forEach((prices, i) => {
                if (i < newPortfolioValues.length) {
                    newPortfolioValues[i] += parseFloat(prices) * qty;
                }

            })
        });
        mainPortfolioChart.data.labels = newLabels;
        mainPortfolioChart.data.datasets[0].data = newPortfolioValues;
        mainPortfolioChart.update();



        });
    });
}
buttonUpdate();