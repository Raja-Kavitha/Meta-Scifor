const quotes = [
    { quote: "The only way to do great work is to love what you do", author: "Steve Jobs" },
    { quote: "The best way to predict your future is to create it", author: "Abraham Lincoln" },
    { quote: "Everything you can imagine is real", author: "Pablo Picasso" },
    { quote: "Believe you can and you are halfway there", author: "Theodore Roosevelt" },
    { quote: "A small leak will sink a great ship", author: " Benjamin Franklin" },
    {quote:'Thinking is the capital, Enterprise is the way, Hard Work is the solution', author:'APJ Abdul Kalam'},
    {quote:'A big shot is a little shot who keeps on shooting, so keep trying',author:'APJ Abdul Kalam'},
    {quote:'What we think, we become.',author:'Puddha'}
];

const quoteDisplay = document.getElementById('quoteDisplay');
const newQuoteBtn = document.getElementById('newQuoteBtn');

function getRandomQuote() {
    const randomIndex = Math.floor(Math.random() * quotes.length);
    return quotes[randomIndex];
}

function displayQuote() {
    const { quote, author } = getRandomQuote();
    quoteDisplay.textContent = `"${quote}" - ${author}`;
}

// Display a quote when the page loads
displayQuote();

// Display a new quote when the button is clicked
newQuoteBtn.addEventListener('click', displayQuote);
