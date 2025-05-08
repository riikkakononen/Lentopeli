import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [countries, setCountries] = useState([]);
  const [selectedCountry, setSelectedCountry] = useState("");
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [userAnswers, setUserAnswers] = useState([]);
  const [gameState, setGameState] = useState({
    stars: 0,
    co2: 0,
    visitedCountries: [],
    gameOver: false,
  });

  // Haetaan maat, kun sovellus käynnistyy
  useEffect(() => {
    const fetchCountries = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/countries");
        if (!response.ok) throw new Error("Maita ei saatu haettua");
        const data = await response.json();
        setCountries(data);
      } catch (error) {
        console.error("Virhe haettaessa maita:", error);
      }
    };
    fetchCountries();
  }, []);

  // Kun maa valitaan
  const handleCountrySelect = (country) => {
    setSelectedCountry(country);
    setCurrentQuestionIndex(0);
    setUserAnswers([]);

    fetch(`http://localhost:8000/api/questions/${country}`)
      .then((res) => res.json())
      .then((data) => setQuestions(data))
      .catch((err) => console.error("Virhe kysymyksien haussa:", err));
  };

  // Kun pelaaja vastaa yhteen kysymykseen
  const handleUserAnswer = (userAnswer) => {
    const currentQuestion = questions[currentQuestionIndex];

    fetch("http://localhost:8000/api/check_answer", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question_id: currentQuestion.id,
        userAnswer: userAnswer,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        const newAnswers = [...userAnswers, data.correct];
        setUserAnswers(newAnswers);

        if (currentQuestionIndex < 2) {
          setCurrentQuestionIndex((prev) => prev + 1);
        } else {
          handleQuestionResults(newAnswers);
        }
      })
      .catch((err) => {
        console.error("Virhe vastauksen tarkistuksessa:", err);
      });
  };

  // Kun 3 kysymykseen on vastattu
  const handleQuestionResults = (answers) => {
    const correctCount = answers.filter(Boolean).length;
    const starsEarned = correctCount;
    const passed = correctCount >= 1;

    let newCO2 = gameState.co2 + 300; // Yksi lento = 300kg
    let updatedState = {
      ...gameState,
      co2: newCO2,
    };

    if (passed) {
      updatedState.stars += starsEarned;
      updatedState.visitedCountries.push(selectedCountry);
    }

    if (newCO2 > 3600 && updatedState.stars === 0) {
      updatedState.gameOver = true;
    }

    setGameState(updatedState);
    setSelectedCountry("");
    setQuestions([]);
    setCurrentQuestionIndex(0);
    setUserAnswers([]);
  };

  // GAME OVER -näkymä
  if (gameState.gameOver) {
    return (
      <div className="App">
        <h1>GAME OVER</h1>
        <p>CO₂-raja ylitetty. Et voi jatkaa peliä.</p>
        <p>Tähdet: {gameState.stars}</p>
        <p>CO₂: {gameState.co2} / 3600 kg</p>
      </div>
    );
  }

  // Normaalin pelinäkymän palautus
  return (
    <div className="App">
      <h1>Lennä ja tiedä!</h1>
      <p>CO₂: {gameState.co2} / 3600 kg</p>
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

export default App;
