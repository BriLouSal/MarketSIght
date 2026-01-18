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
