// static/js/main.js

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('qa-form');
    const submitBtn = document.getElementById('submit-btn');
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');
    const answerP = document.getElementById('answer');
    const sourcesUl = document.getElementById('sources');
    const fileInput = document.getElementById('file-upload');
    const fileNameP = document.getElementById('file-name');

    // Update the file name display when a file is selected
    fileInput.addEventListener('change', (event) => {
        const fileName = event.target.files[0]?.name;
        if (fileName) {
            fileNameP.innerHTML = `<span class="font-semibold text-indigo-600">${fileName}</span> is selected.`;
        } else {
            fileNameP.innerHTML = '<span class="font-semibold">Click to upload</span> or drag and drop';
        }
    });

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const questionInput = document.getElementById('question');
        
        if (fileInput.files.length === 0) {
            alert('Please select a file to upload.');
            return;
        }

        // Show loading state
        submitBtn.disabled = true;
        submitBtn.classList.add('opacity-50', 'cursor-not-allowed');
        loadingDiv.classList.remove('hidden');
        resultsDiv.classList.add('hidden');

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        formData.append('question', questionInput.value);

        try {
            const response = await fetch('/ask', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || `Server error: ${response.status}`);
            }

            // Display results
            answerP.textContent = data.answer;
            sourcesUl.innerHTML = ''; // Clear previous sources
            
            if (data.sources && data.sources.length > 0) {
                data.sources.forEach(source => {
                    const li = document.createElement('li');
                    li.className = 'flex items-start';
                    // Add a small icon for each source
                    li.innerHTML = `
                        <svg class="w-5 h-5 mr-2 text-purple-500 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.293l-3-3a1 1 0 00-1.414 1.414L10.586 9.5H7a1 1 0 100 2h3.586l-1.293 1.293a1 1 0 101.414 1.414l3-3a1 1 0 000-1.414z" clip-rule="evenodd"></path></svg>
                        <span>${source}</span>
                    `;
                    sourcesUl.appendChild(li);
                });
            } else {
                sourcesUl.innerHTML = '<li class="text-gray-500">No specific sources cited.</li>';
            }
            
            resultsDiv.classList.remove('hidden');
            resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        } catch (error) {
            console.error('Error:', error);
            // Display a more user-friendly error message in the UI
            answerP.textContent = `An error occurred: ${error.message}`;
            sourcesUl.innerHTML = '';
            resultsDiv.classList.remove('hidden');
        } finally {
            // Hide loading state
            submitBtn.disabled = false;
            submitBtn.classList.remove('opacity-50', 'cursor-not-allowed');
            loadingDiv.classList.add('hidden');
        }
    });
});