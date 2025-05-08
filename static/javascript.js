const { useState, useEffect } = React;

function App() {
  const [showIntro, setShowIntro] = useState(true);
  const [countries, setCountries] = useState([]);
  const [selectedCountry, setSelectedCountry] = useState("");
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [userAnswers, setUserAnswers] = useState([]);
  const [gameWon, setGameWon] = useState(false);
  const [gameState, setGameState] = useState({
    stars: 0,
    co2: 0,
    co2Limit: 3600,
    visitedCountries: [],
    gameOver: false,
  });

  // Haetaan maat
  useEffect(() => {
    fetch("/api/countries")
      .then((res) => res.json())
      .then((data) => setCountries(data))
      .catch((err) => console.error("Virhe maita haettaessa:", err));
  }, []);

  // Maan valinta
  const handleCountrySelect = (country) => {
    setSelectedCountry(country);
    setCurrentQuestionIndex(0);
    setUserAnswers([]);

    fetch(`/api/questions/${country}`)
      .then((res) => res.json())
      .then((data) => setQuestions(data))
      .catch((err) => console.error("Virhe kysymyksiä haettaessa:", err));
  };

  // Pelaajan vastaus
  const handleUserAnswer = (answer) => {
    const currentQuestion = questions[currentQuestionIndex];

    fetch("/api/check_answer", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question_id: currentQuestion.id,
        userAnswer: answer,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        const updatedAnswers = [...userAnswers, data.correct];
        setUserAnswers(updatedAnswers);

        if (currentQuestionIndex < 2) {
          setCurrentQuestionIndex((prev) => prev + 1);
        } else {
          handleQuestionResults(updatedAnswers);
        }
      });
  };

  // Kysymysten jälkeen pelitilan päivitys
const handleQuestionResults = (answers) => {
  const correctCount = answers.filter(Boolean).length;
  const starsEarned = correctCount;
  const passed = correctCount >= 1;

  let newCO2 = gameState.co2 + 300;
  let updatedState = {
    ...gameState,
    co2: newCO2,
  };

  if (passed) {
    updatedState.stars += starsEarned;
    updatedState.visitedCountries.push(selectedCountry);
    setSelectedCountry("");

 if (updatedState.visitedCountries.length === countries.length) {
    alert("Onneksi olkoon! Kävit kaikissa maissa ja voitit pelin! 🎉");
    updatedState.gameOver = true;
    }

  } else {
    fetch(`http://localhost:8000/api/weather/${selectedCountry}`)
      .then((res) => res.json())
      .then((data) => {
        const weather = data.weather;
        if (weather === "huono") {
          alert(`Sää on huono, paluumatka estyy – yritä samaa maata uudelleen.`);
        } else {
          alert(`Vastasit väärin kaikkiin kysymyksiin. Sää on hyvä – voit valita uuden kohteen.`);
          setSelectedCountry("");
        }
      });
  }

  // CO2-rajan tarkistus
  if (updatedState.co2 >= updatedState.co2Limit) {
    if (updatedState.stars >= 1) {
      const useStars = window.confirm("CO₂-raja saavutettu! Haluatko käyttää tähtiäsi rajan nostamiseen?");
      if (useStars) {
        const options = [
          { stars: 1, increase: 300 },
          { stars: 3, increase: 900 },
          { stars: 5, increase: 1500 },
        ].filter(opt => updatedState.stars >= opt.stars);

        const valinta = prompt(
          "Valitse kuinka monta tähteä käytät rajan nostamiseen:\n" +
          options.map(opt => `${opt.stars} tähteä → +${opt.increase} kg`).join("\n")
        );

        const choice = options.find(opt => parseInt(valinta) === opt.stars);

        if (choice) {
          updatedState.stars -= choice.stars;
          updatedState.co2Limit += choice.increase;
          alert(`CO₂-rajaa nostettiin ${choice.increase} kg. Uusi raja: ${updatedState.co2Limit} kg.`);
        } else {
          alert("Virheellinen valinta. Peli päättyy.");
          updatedState.gameOver = true;
        }
      } else {
        updatedState.gameOver = true;
      }
    } else {
      alert("CO₂-raja saavutettu eikä sinulla ole tähtiä. Peli päättyy.");
      updatedState.gameOver = true;
    }
  }

  // Voittotarkistus
  if (Array.isArray(countries) && updatedState.visitedCountries.length === countries.length) {
    setGameWon(true);
    updatedState.gameOver = true;
  }


  setGameState(updatedState);
  setQuestions([]);
  setCurrentQuestionIndex(0);
  setUserAnswers([]);
};



  // Intro -näkymä
  if (showIntro) {
  return (
    <div>
      <h1>Lennä ja tiedä!</h1>
      <p>Tässä pelissä lennät ympäri Eurooppaa vastaten kysymyksiin.</p>
      <p>Vastaa vähintään yhteen kysymykseen oikein per kohde päästäksesi eteenpäin.</p>
      <p>Mutta varo CO₂-päästörajaa – peli päättyy, jos se ylittyy!</p>
      <button onClick={() => setShowIntro(false)}>Aloita peli</button>
    </div>
  );
}

  // Game Won -näkymä
  if (gameWon) {
    return (
      <div className="win-screen">
        <h1>🎉 Onneksi olkoon! 🎉</h1>
        <p>Olet vieraillut kaikissa maissa ja voittanut pelin!</p>
        <p>Kokonaispäästöt: {gameState.co2} kg</p>
        <p>Tähdet: {gameState.stars}</p>
      </div>
    );
  }

  // Game Over -näkymä
  if (gameState.gameOver) {
    return (
      <div className="App">
        <h1>GAME OVER</h1>
        <p>CO2 päästöraja ylitetty.</p>
        <p>Tähdet: {gameState.stars}</p>
      </div>
    );
  }

  // Peli-näkymä

  return (
    <div className="App">
      <h1>Lennä ja tiedä!</h1>
      <p>CO₂: {gameState.co2} / {gameState.co2Limit} kg</p>
      <p>Tähdet: {gameState.stars} / 30</p>

      {selectedCountry === "" ? (
        <div>
          <h2>Valitse maa:</h2>
          <ul>
            {countries
              .filter((c) => !gameState.visitedCountries.includes(c))
              .map((country) => (
                <li key={country}>
                  <button onClick={() => handleCountrySelect(country)}>
                    {country}
                  </button>
                </li>
              ))}
          </ul>
        </div>
      ) : questions.length > 0 ? (
        <div>
          <h2>{selectedCountry}</h2>
          <p>{questions[currentQuestionIndex].text}</p>
          {questions[currentQuestionIndex].options.map((opt, i) => (
            <button key={i} onClick={() => handleUserAnswer(opt)}>
              {opt}
            </button>
          ))}
        </div>
      ) : (
        <p>Ladataan kysymyksiä...</p>
      )}
    </div>
  );
}

// React-sovelluksen renderöinti
ReactDOM.render(<App />, document.getElementById("root"));
