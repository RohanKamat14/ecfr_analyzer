// Fetch eCFR data
async function fetchECFRData() {
    const response = await fetch('https://www.ecfr.gov/api/1.1/document', {
        method: 'GET',
    });

    if (response.ok) {
        const data = await response.json();
        return data;
    } else {
        console.error('Error fetching eCFR data:', response.status);
    }
}

// Function to analyze word count per agency
function analyzeWordCount(data) {
    const wordCounts = {};

    data.forEach(item => {
        const agency = item.agency;
        const content = item.content; // Assuming 'content' contains the text of the regulation

        // Count words in content
        const wordCount = content.split(' ').length;

        // Add to the agency's word count
        if (wordCounts[agency]) {
            wordCounts[agency] += wordCount;
        } else {
            wordCounts[agency] = wordCount;
        }
    });

    return wordCounts;
}

// Function to analyze word count per agency
function analyzeWordCount(data) {
    const wordCounts = {};

    data.forEach(item => {
        const agency = item.agency;
        const content = item.content; // Assuming 'content' contains the text of the regulation

        // Count words in content
        const wordCount = content.split(' ').length;

        // Add to the agency's word count
        if (wordCounts[agency]) {
            wordCounts[agency] += wordCount;
        } else {
            wordCounts[agency] = wordCount;
        }
    });

    return wordCounts;
}
document.addEventListener('DOMContentLoaded', async () => {
    // Fetch eCFR data
    const data = await fetchECFRData();

    // Analyze the word count per agency
    const wordCounts = analyzeWordCount(data);

    // Prepare data for visualization (chart.js)
    const agencies = Object.keys(wordCounts);
    const counts = Object.values(wordCounts);

    // Create a bar chart
    const ctx = document.getElementById('wordCountChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: agencies,
            datasets: [{
                label: 'Word Count',
                data: counts,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});

