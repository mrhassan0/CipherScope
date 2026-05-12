function showSection(sectionId) {
  var pages = document.querySelectorAll(".page");

  for (var i = 0; i < pages.length; i++) {
    pages[i].classList.remove("active");
  }

  document.getElementById(sectionId).classList.add("active");
}


function valueOf(id) {
  return document.getElementById(id).value;
}


function showResult(id, data) {
  document.getElementById(id).textContent = JSON.stringify(data, null, 2);
}


function hideBox(id) {
  document.getElementById(id).classList.add("hidden");
}


function showBox(id) {
  document.getElementById(id).classList.remove("hidden");
}


async function postData(url, data) {
  var response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });

  return await response.json();
}


function setupForms() {
  updateSubForm();
  updateDoubleForm();
  updateDesForm();
  updateAesForm();
  updateRsaForm();
  updateEccForm();
}


function updateSubForm() {
  var mode = valueOf("subMode");

  if (mode == "encrypt") {
    document.getElementById("subTextLabel").textContent = "Plaintext";
    showBox("subKeyLabel");
    showBox("subKey");
  }

  if (mode == "decrypt") {
    document.getElementById("subTextLabel").textContent = "Ciphertext";
    showBox("subKeyLabel");
    showBox("subKey");
  }

  if (mode == "frequency") {
    document.getElementById("subTextLabel").textContent = "Text for frequency analysis";
    hideBox("subKeyLabel");
    hideBox("subKey");
  }

  if (mode == "frequencyAttack") {
    document.getElementById("subTextLabel").textContent = "Substitution ciphertext for frequency attack";
    hideBox("subKeyLabel");
    hideBox("subKey");
  }

  if (mode == "bruteforce") {
    document.getElementById("subTextLabel").textContent = "Caesar ciphertext";
    hideBox("subKeyLabel");
    hideBox("subKey");
  }
}


async function runSubstitution() {
  var mode = valueOf("subMode");
  var answer;

  if (mode == "encrypt") {
    answer = await postData("/api/substitution/encrypt", {
      plaintext: valueOf("subText"),
      key: valueOf("subKey")
    });
  }

  if (mode == "decrypt") {
    answer = await postData("/api/substitution/decrypt", {
      ciphertext: valueOf("subText"),
      key: valueOf("subKey")
    });
  }

  if (mode == "frequency") {
    answer = await postData("/api/substitution/frequency", {
      text: valueOf("subText")
    });
  }

  if (mode == "frequencyAttack") {
    answer = await postData("/api/substitution/frequency-attack", {
      ciphertext: valueOf("subText")
    });
  }

  if (mode == "bruteforce") {
    answer = await postData("/api/substitution/bruteforce", {
      ciphertext: valueOf("subText")
    });
  }

  showResult("subResult", answer);
}


function updateDoubleForm() {
  var mode = valueOf("doubleMode");

  if (mode == "encrypt") {
    document.getElementById("doubleTextLabel").textContent = "Plaintext";
    document.getElementById("doubleKey1Label").textContent = "Row permutation key";
    document.getElementById("doubleKey2Label").textContent = "Column permutation key";
    showBox("doubleKeyBox");
  }

  if (mode == "decrypt") {
    document.getElementById("doubleTextLabel").textContent = "Ciphertext";
    document.getElementById("doubleKey1Label").textContent = "Row permutation key";
    document.getElementById("doubleKey2Label").textContent = "Column permutation key";
    showBox("doubleKeyBox");
  }

  if (mode == "frequency") {
    document.getElementById("doubleTextLabel").textContent = "Text for frequency analysis";
    hideBox("doubleKeyBox");
  }

  if (mode == "permutationAttack") {
    document.getElementById("doubleTextLabel").textContent = "Double transposition ciphertext for permutation attack";
    hideBox("doubleKeyBox");
  }
}


async function runDoubleTransposition() {
  var mode = valueOf("doubleMode");
  var answer;

  if (mode == "encrypt") {
    answer = await postData("/api/double-transposition/encrypt", {
      plaintext: valueOf("doubleText"),
      first_key: valueOf("doubleKey1"),
      second_key: valueOf("doubleKey2")
    });
  }

  if (mode == "decrypt") {
    answer = await postData("/api/double-transposition/decrypt", {
      ciphertext: valueOf("doubleText"),
      first_key: valueOf("doubleKey1"),
      second_key: valueOf("doubleKey2")
    });
  }

  if (mode == "frequency") {
    answer = await postData("/api/double-transposition/frequency", {
      text: valueOf("doubleText")
    });
  }

  if (mode == "permutationAttack") {
    answer = await postData("/api/double-transposition/permutation-attack", {
      ciphertext: valueOf("doubleText")
    });
  }

  showResult("doubleResult", answer);
}


function updateDesForm() {
  var mode = valueOf("desMode");

  if (mode == "encrypt") {
    document.getElementById("desTextLabel").textContent = "Plaintext";
    hideBox("desKeyBox");
  }

  if (mode == "decrypt") {
    document.getElementById("desTextLabel").textContent = "Ciphertext hex";
    showBox("desKeyBox");
  }
}


async function runDesMode() {
  var mode = valueOf("desMode");
  var answer;

  if (mode == "encrypt") {
    answer = await postData("/api/des/encrypt", {
      plaintext: valueOf("desText")
    });
  }

  if (mode == "decrypt") {
    answer = await postData("/api/des/decrypt", {
      ciphertext_hex: valueOf("desText"),
      key_hex: valueOf("desKeyHex")
    });
  }

  showResult("desResult", answer);
}


function updateAesForm() {
  var mode = valueOf("aesMode");

  if (mode == "encrypt") {
    document.getElementById("aesTextLabel").textContent = "Plaintext";
    hideBox("aesKeyBox");
  }

  if (mode == "decrypt") {
    document.getElementById("aesTextLabel").textContent = "Ciphertext hex";
    showBox("aesKeyBox");
  }
}


async function runAesMode() {
  var mode = valueOf("aesMode");
  var answer;

  if (mode == "encrypt") {
    answer = await postData("/api/aes/encrypt", {
      plaintext: valueOf("aesText")
    });
  }

  if (mode == "decrypt") {
    answer = await postData("/api/aes/decrypt", {
      ciphertext_hex: valueOf("aesText"),
      key_hex: valueOf("aesKeyHex")
    });
  }

  showResult("aesResult", answer);
}


function updateRsaForm() {
  var mode = valueOf("rsaMode");

  hideBox("rsaKeySizeBox");
  hideBox("rsaMessageBox");
  hideBox("rsaEBox");
  hideBox("rsaNBox");
  hideBox("rsaDBox");

  if (mode == "generate") {
    showBox("rsaKeySizeBox");
  }

  if (mode == "encrypt") {
    document.getElementById("rsaMessageLabel").textContent = "Plaintext";
    showBox("rsaMessageBox");
    showBox("rsaEBox");
    showBox("rsaNBox");
  }

  if (mode == "decrypt") {
    document.getElementById("rsaMessageLabel").textContent = "Ciphertext";
    showBox("rsaMessageBox");
    showBox("rsaDBox");
    showBox("rsaNBox");
  }

  if (mode == "attack") {
    showBox("rsaEBox");
    showBox("rsaNBox");
  }
}


async function runRsaMode() {
  var mode = valueOf("rsaMode");
  var answer;

  if (mode == "generate") {
    answer = await postData("/api/rsa/generate-keys", {
      key_size: valueOf("rsaKeySize")
    });
  }

  if (mode == "encrypt") {
    answer = await postData("/api/rsa/encrypt", {
      plaintext: valueOf("rsaMessage"),
      e: valueOf("rsaE"),
      n: valueOf("rsaN")
    });
  }

  if (mode == "decrypt") {
    answer = await postData("/api/rsa/decrypt", {
      ciphertext: valueOf("rsaMessage"),
      d: valueOf("rsaD"),
      n: valueOf("rsaN")
    });
  }

  if (mode == "attack") {
    answer = await postData("/api/rsa/factorization-attack", {
      n: valueOf("rsaN"),
      e: valueOf("rsaE")
    });
  }

  showResult("rsaResult", answer);
}


function eccInputData() {
  return {
    p: valueOf("eccP"),
    a: valueOf("eccA"),
    b: valueOf("eccB"),
    gx: valueOf("eccGx"),
    gy: valueOf("eccGy"),
    n: valueOf("eccN")
  };
}


function updateEccForm() {
  var mode = valueOf("eccMode");

  hideBox("eccPrivateBox");
  hideBox("eccEcdhBox");

  if (mode == "key") {
    showBox("eccPrivateBox");
  }

  if (mode == "ecdh") {
    showBox("eccEcdhBox");
  }
}


async function runEccMode() {
  var mode = valueOf("eccMode");
  var data = eccInputData();
  var answer;

  if (mode == "points") {
    answer = await postData("/api/ecc/points", data);
  }

  if (mode == "key") {
    data.private_key = valueOf("eccPrivate");
    answer = await postData("/api/ecc/generate-key", data);
  }

  if (mode == "ecdh") {
    data.alice_private = valueOf("alicePrivate");
    data.bob_private = valueOf("bobPrivate");
    answer = await postData("/api/ecc/ecdh", data);
  }

  showResult("eccResult", answer);
}


async function loadComparison() {
  var response = await fetch("/api/comparison");
  var answer = await response.json();

  if (answer.success == false) {
    document.getElementById("comparisonResult").textContent = JSON.stringify(answer, null, 2);
    return;
  }

  var rows = answer.result;
  var html = "";

  html = html + "<table>";
  html = html + "<tr>";
  html = html + "<th>Algorithm</th>";
  html = html + "<th>Category</th>";
  html = html + "<th>Key Type</th>";
  html = html + "<th>Security Note</th>";
  html = html + "<th>Analysis</th>";
  html = html + "</tr>";

  for (var i = 0; i < rows.length; i++) {
    html = html + "<tr>";
    html = html + "<td>" + rows[i].algorithm + "</td>";
    html = html + "<td>" + rows[i].category + "</td>";
    html = html + "<td>" + rows[i].key_type + "</td>";
    html = html + "<td>" + rows[i].security_note + "</td>";
    html = html + "<td>" + rows[i].analysis + "</td>";
    html = html + "</tr>";
  }

  html = html + "</table>";
  document.getElementById("comparisonResult").innerHTML = html;
}


async function loadPerformanceComparison() {
  document.getElementById("performanceResult").innerHTML = "<p>Running live comparison...</p>";

  var response = await fetch("/api/performance-comparison");
  var answer = await response.json();

  if (answer.success == false) {
    document.getElementById("performanceResult").textContent = JSON.stringify(answer, null, 2);
    return;
  }

  var rows = answer.result.rows;
  var html = "";

  html = html + "<p>" + answer.result.message + "</p>";
  html = html + "<table>";
  html = html + "<tr>";
  html = html + "<th>Algorithm</th>";
  html = html + "<th>Category</th>";
  html = html + "<th>Sample</th>";
  html = html + "<th>Key / Parameters</th>";
  html = html + "<th>Key Gen Time</th>";
  html = html + "<th>Encrypt Time</th>";
  html = html + "<th>Decrypt / ECDH Time</th>";
  html = html + "<th>Analysis / Attack Time</th>";
  html = html + "<th>Extra Output</th>";
  html = html + "<th>Security Note</th>";
  html = html + "<th>Check</th>";
  html = html + "</tr>";

  for (var i = 0; i < rows.length; i++) {
    html = html + "<tr>";
    html = html + "<td>" + rows[i].algorithm + "</td>";
    html = html + "<td>" + rows[i].category + "</td>";
    html = html + "<td>" + rows[i].sample_input + "</td>";
    html = html + "<td>" + rows[i].key_or_parameters + "</td>";
    html = html + "<td>" + rows[i].key_generation_time_seconds + "</td>";
    html = html + "<td>" + rows[i].encryption_time_seconds + "</td>";
    html = html + "<td>" + rows[i].decryption_time_seconds + "</td>";
    html = html + "<td>" + rows[i].analysis_or_attack_time_seconds + "</td>";
    html = html + "<td>" + rows[i].extra_output + "</td>";
    html = html + "<td>" + rows[i].security_note + "</td>";
    html = html + "<td>" + rows[i].correctness_check + "</td>";
    html = html + "</tr>";
  }

  html = html + "</table>";

  document.getElementById("performanceResult").innerHTML = html;
}
