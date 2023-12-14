{% comment %} /*const readFile = require('fs').readFileSync;
const data = readFile('data.txt', 'utf8');

// Parse the data and extract author and paper names
const authors = [];
const papers = [];


const lines = data.split('\n');
for (let line of lines) {
    const [author, paper] = line.split(',');
    authors.push(author);
    papers.push(paper);
}

// Replace placeholder data with actual data
const authorElements = document.querySelectorAll('.panel-heading');
const paperElements = document.querySelectorAll('.panel-body');

for (let i = 0; i < authorElements.length; i++) {
    authorElements[i].textContent = authors[i];
    paperElements[i].textContent = papers[i];
} */

const dataFileUrl = 'data.txt';

fetch(dataFileUrl)
    .then(response => response.text())
    .then(data => {
        const authorPaperPairs = data.split('\n');
        const panels = document.querySelectorAll('.panel');

        for (let i = 0; i < panels.length; i++) {
            const panel = panels[i];
            const authorPaperPair = authorPaperPairs[i].split(',');
            const author = authorPaperPair[0];
            const paper = authorPaperPair[1];

            const panelHeading = panel.querySelector('.panel-heading');
            const panelBody = panel.querySelector('.panel-body');

            panelHeading.textContent = paper;
            panelBody.textContent = author + '<br>Publication, Year';
        }
    }); {% endcomment %}
    