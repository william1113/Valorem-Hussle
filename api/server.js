const express = require('express');
const bodyParser = require('body-parser');
const app = express();

const companyNameInput = document.getElementById('companyName');

companyNameInput.addEventListener('input', function(){
    const companyNameValue = companyNameInput.value;

    console.log(companyNameValue);
});

const PORT = 3000
app.listen(PORT,() =>
    console.log(`Listening on port ${PORT}`),
);