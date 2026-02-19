const input = document.getElementById('stockSearch');
const autocomplete = document.querySelector('.autocomplete');

// autocomplete feature
input.addEventListener('input', async () => {

    const query = input.value;

    if (query.length < 1) {
        autocomplete.classList.add('hidden');
        autocomplete.innerHTML = '';
        return;
    }
    // Get the URL for my stock
    const response = await fetch(`/api/autocomplete/${query}/`);
    const data = await response.json();
    // Check if it works. This is crucial for error fixes
    console.log(data);  
    // Ignore if the input size is less than 1

    if (data.results && data.results.length > 0) {

        autocomplete.classList.remove('hidden');
        // Create the Stock autocomplete system
        autocomplete.innerHTML = data.results.map(stock => `

            <div 
                class="px-4 py-2 flex justify-between items-center cursor-pointer 
                       hover:bg-blue-800/40 transition"
                onclick="window.location.href='/stock/${stock.symbol}/'">

                <div>
                    <div class="text-white font-semibold text-sm">
                        ${stock.symbol ?? ''}
                    </div>

                    <div class="text-slate-400 text-xs truncate max-w-xs">
                        ${stock.name ?? ''}
                    </div>
                </div>

                <div class="text-slate-300 text-xs">
                    ${stock.exchange ?? ''}
                </div>

            </div>

        `).join('');

    } else {
        autocomplete.classList.add('hidden');
        autocomplete.innerHTML = '';
    }
});
const canvases = document.querySelectorAll('.gainerGraph');


canvases.forEach((canvas, index) => {


    canvas.addEventListener('click', () => {
        window.location.href = `/stock/${ticker[index]}/`;
    });

    // Create chart for each stock
    new Chart(canvas, {
        type: 'line',
       
        data: {           
            labels: percentage[index].map((_, i) => i), 
            datasets: [{
                label: ticker[index],
                data:  percentage[index],       
                borderColor: '#4fc51c',
                backgroundColor: '#166534',
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
});


// Daily losers
const canvases_loser = document.querySelectorAll('.loserGraph');

canvases_loser.forEach((canvases_loser, index) => {


    canvases_loser.addEventListener('click', () => {
        window.location.href = `/stock/${loser_ticker[index]}/`;
    });

    // Create chart for each stock
    new Chart(canvases_loser, {
        type: 'line',
       
        data: {           
            labels: loser_percentage[index].map((_, i) => i), 
            datasets: [{
                label: loser_ticker[index],
                data:  loser_percentage[index],       
                borderColor: '#DC2626',
                backgroundColor: '#DC2626',
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
});
