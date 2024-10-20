document.getElementById('uploadForm').onsubmit = async function (e) {
    e.preventDefault();  // Prevent the form from submitting the default way

    const formData = new FormData();
    const fileInput = document.getElementById('fileInput');

    // Append the file to the FormData object
    formData.append('file', fileInput.files[0]);

    try {
        // Send a POST request with the file to the FastAPI backend
        const response = await fetch('http://127.0.0.1:8000/uploadbook', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        document.getElementById('responseMessage').textContent = result.status;
        document.getElementById('responseMessage').classList.add('text-success');


        // Make a GET request to the API
        const response_ch = await fetch('http://127.0.0.1:8000/book/conversation/chapter/1', {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });

        // Check if the response is okay (status 200)
        if (!response_ch.ok) {
            throw new Error('Network response was not ok');
        }

        // Parse the JSON response
        const data = await response_ch.json();

        // Display the response content
        const responseDiv = document.getElementById('response');
        responseDiv.innerHTML = `
            <h3>${data.bookname} - Chapter ${data.ch_no}</h3>
            <pre>${data.content}</pre>
        `;

        const chapterContent = data.content;
        ////////////////////
        const query = chapterContent +
        '\nTell me the unique characters, their possible genders, and personality attributes in the above conversation.'
        + '\nGive me the response in the following JSON schema:\n'
        + 'Character = {"character_name" : str, "gender": "male/female", "personality": list[str], "dialogues": list[str]}\n'
        + 'Return: list[Character]\n'
        + 'where dialogues is a list of dialogues spoken by respective characters.'


        // Create the request payload
        const requestData = {
            query: query
        };

        try {
            // Make a POST request to the API
            const llm_response = await fetch('http://127.0.0.1:8000/llm-query', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData) // Convert the payload to a JSON string
            });

            // Check if the response is okay (status 200)
            if (!llm_response.ok) {
                throw new Error('Network response was not ok');
            }

            // Parse the JSON response
            const llm_data = await llm_response.json();
            // Extracting the JSON part using regex
            const jsonMatch = llm_data.response.match(/```json\n(.*?)\n```/s);

            // If a match is found, parse the JSON
            if (jsonMatch) {
                const jsonString = jsonMatch[1]; // The matched JSON string
                const characters = JSON.parse(jsonString); // Parse the JSON string into an object

                console.log(JSON.stringify(characters)); // Output the JavaScript object
            } else {
                console.log
                console.error("No JSON found in the response.");
            }


        } catch (error) {
            // Handle errors
            const responseDiv = document.getElementById('response');
            responseDiv.innerHTML = `<p class="text-danger">Error fetching data: ${error.message}</p>`;
        }

    } catch (error) {
        document.getElementById('responseMessage').textContent = 'Error uploading file!';
        document.getElementById('responseMessage').classList.add('text-danger');
    }
}