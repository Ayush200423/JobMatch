const replaceInputValues = {
    'fname': 'fname',
    'lname': 'lname',
    'phone': 'phone',
    'degree': 'degree',
    'skills': 'skills',
    'role': 'role',
    'location': 'location'
}

function getEntsData() {
    fetch('/api/resume-data')
    .then((res) => res.json())
    .then((data) => {
        for (const [input_id, data_key] of Object.entries(replaceInputValues)) {
            document.querySelector(`#${input_id}`).value = data[data_key];
        }
    });
}

function sendResumeUpdates(e) {
    e.preventDefault();
    const boxName = e.target.getAttribute("id");
    const boxValue = e.target.value;
    fetch('/api/resume-data', {
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

function getJobPostings(callback) {
    fetch('/api/relevant-postings')
    .then((res) => res.json())
    .then((data) => {
        let isPosting = false;
        for (posting_name of Object.keys(data)) {
            isPosting = true;
            createPosting(data[posting_name]);
        }
        removeLoader();
        if (isPosting == false) {
            document.getElementById('no-jobs').style.display = 'block';
        } else {
            document.getElementById('submit-form').style.display = 'block';
            document.getElementById('select-label').style.display = 'block';
            document.getElementById('select-all').style.display = 'block';
            callback();
        }
        return
    })
}

function sendCheckboxState(e) {
    let checkboxLink;
    if (e.target.getAttribute('id') != "select-all") {
        checkboxLink = [e.target.getAttribute('id')];
    } else {
        checkboxLink = Array.prototype.map.call(document.querySelectorAll('.select-checkbox'), el => el.getAttribute('id'));
    }
    
    let state = "remove"
    if (e.target.checked) {
        state = "append"
    }
    fetch('/api/relevant-postings', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({[state]:checkboxLink}),
    })
    .then((response) => response.json())
    .then((data) => {
        console.log('Success:', data)
    })
    .catch((error) => {
        console.error('Error:', error)
    })
}