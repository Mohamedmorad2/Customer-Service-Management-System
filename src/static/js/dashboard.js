// Doughnut Chart (Already added)
var ctxDoughnut = document.getElementById('doughnutChart').getContext('2d');
var doughnutChart = new Chart(ctxDoughnut, {
    type: 'doughnut',
    data: {
        labels: ['Expenses', 'Orders', 'Customers', 'Reviews'],
        datasets: [{
            data: [5000, 150, 120, 50],
            backgroundColor: ['#4a90e2', '#f5a623', '#2ecc71', '#8e44ad']
        }]
    },
    options: {
        responsive: true
    }
});

// Line Chart (Already added)
var ctxLine = document.getElementById('lineChart').getContext('2d');
var lineChart = new Chart(ctxLine, {
    type: 'line',
    data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [{
            label: 'Revenue',
            data: [3000, 3500, 4000, 4500, 5000, 5500, 6000],
            borderColor: '#4a90e2',
            fill: false,
            borderWidth: 2,
            pointBackgroundColor: '#4a90e2'
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: false
            }
        }
    }
});

// New Bar Chart (Sales vs Purchases)
var ctxBar = document.getElementById('barChart').getContext('2d');
var barChart = new Chart(ctxBar, {
    type: 'bar',
    data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [
            {
                label: 'Sales',
                data: [5000, 4000, 4500, 6000, 7000, 6500, 8000],
                backgroundColor: '#4a90e2'
            },
            {
                label: 'Purchases',
                data: [3000, 3500, 4000, 3000, 5000, 4500, 5000],
                backgroundColor: '#f5a623'
            }
        ]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
