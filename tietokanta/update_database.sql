ALTER TABLE player_state ADD COLUMN co2_paastot INT DEFAULT 0;

UPDATE questions
SET vaihtoehdot = '{"A": "noin 68,3 miljoonaa", "B": "noin 52,1 miljoonaa", "C": "noin 45,0 miljoonaa"}'
WHERE id = 6;

UPDATE questions
SET vaihtoehdot = '{"A": "Ei", "B": "Kyllä", "C": "Sillä on sama väkiluku, kuin Aarhusilla"}'
WHERE id = 53;

UPDATE questions
SET kysymys = 'Minkä tunnetun kirjailijan syntymäpaikka on Yhdistyneessä kuningaskunnassa?'
WHERE id = 18;