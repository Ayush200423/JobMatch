const replaceInputValues = {
    'fname': 'fname',
    'lname': 'lname',
    'email': 'email address',
    'phone': 'phone',
    'school': 'college name',
    'certifications': 'degree',
    'graduation-year': 'graduation year',
    'years-of-experience': 'years of experience',
    'skills': 'skills',
    'company': 'company',
    'role': 'role',
    'location': 'location'
}

function getEntsData() {
    fetch('/api/fetch_ents')
    .then((res) => res.json())
    .then((data) => {
        for (const [input_id, data_key] of Object.entries(replaceInputValues)) {
            document.querySelector(`#${input_id}`).value = data[data_key];
        }
    });
}

function sendUpdates(e) {
    e.preventDefault();
    const boxName = e.target.getAttribute("id");
    const boxValue = e.target.value;
    fetch('/api/upload_resume_data', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({[boxName]:boxValue}),
    })
    .then((response) => response.json())
    .then((data) => {
    console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}