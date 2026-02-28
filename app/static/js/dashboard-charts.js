/* LabResta Sync — Dashboard trend charts (Chart.js) */

(function () {
    'use strict';

    var matchesChart = null;
    var syncsChart = null;

    function fetchChartData(days) {
        days = days || 14;
        fetch('/dashboard/chart-data?days=' + days)
            .then(function (r) { return r.json(); })
            .then(function (data) {
                renderMatchesChart(data);
                renderSyncsChart(data);
            })
            .catch(function (err) {
                console.error('Chart data fetch error:', err);
            });
    }

    function renderMatchesChart(data) {
        var ctx = document.getElementById('matchesChart');
        if (!ctx) return;

        if (matchesChart) {
            matchesChart.data.labels = data.labels;
            matchesChart.data.datasets[0].data = data.matches;
            matchesChart.update();
            return;
        }

        matchesChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Матчи за день',
                    data: data.matches,
                    borderColor: '#0d6efd',
                    backgroundColor: 'rgba(13, 110, 253, 0.1)',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 3,
                    pointHoverRadius: 5
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { precision: 0 }
                    }
                }
            }
        });
    }

    function renderSyncsChart(data) {
        var ctx = document.getElementById('syncsChart');
        if (!ctx) return;

        if (syncsChart) {
            syncsChart.data.labels = data.labels;
            syncsChart.data.datasets[0].data = data.syncs;
            syncsChart.data.datasets[1].data = data.updated;
            syncsChart.update();
            return;
        }

        syncsChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: 'Синхронизации',
                        data: data.syncs,
                        backgroundColor: 'rgba(13, 110, 253, 0.6)',
                        borderColor: '#0d6efd',
                        borderWidth: 1,
                        order: 2
                    },
                    {
                        label: 'Обновлено товаров',
                        data: data.updated,
                        type: 'line',
                        borderColor: '#198754',
                        backgroundColor: 'rgba(25, 135, 84, 0.1)',
                        fill: false,
                        tension: 0.3,
                        pointRadius: 3,
                        order: 1
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom' }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { precision: 0 }
                    }
                }
            }
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        // Initial chart load
        fetchChartData(14);

        // Period selector
        var select = document.getElementById('chartPeriodSelect');
        if (select) {
            select.addEventListener('change', function () {
                fetchChartData(parseInt(this.value, 10));
            });
        }
    });
})();
