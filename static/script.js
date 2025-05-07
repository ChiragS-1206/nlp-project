const form = document.getElementById("uploadForm");

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData();
    const resumefile = document.querySelector(".resume").files[0];
    const descfile = document.querySelector(".jobdescription").value;

    if (!resumefile || !descfile.trim()) {
        document.querySelector(".result").innerHTML = `<strong class="error">Error:</strong> Please upload a resume and provide a job description.`;
        return;
    }

    formData.append("resume", resumefile);
    formData.append("job_description", descfile);

    const resultDiv = document.querySelector(".result");

    try {
        const response = await fetch('/upload_resume', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            resultDiv.innerHTML = `<strong class="error">Error:</strong> ${data.error}`;
        } else {
            resultDiv.innerHTML =
                `<strong>Match Score:</strong> ${data.score}%<br>
                 <strong>Suggestions:</strong> ${data.feedback.join(', ') || 'No suggestions available'}`;
        }
    } catch (err) {
        resultDiv.innerHTML = `<strong class="error">Client Error:</strong> ${err.message}`;
    }
});