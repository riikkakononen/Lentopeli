CREATE DATABASE IF NOT EXISTS lentopeli;
USE lentopeli;

-- Lentokenttien taulu
CREATE TABLE airports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nimi VARCHAR(100) NOT NULL,
    maa VARCHAR(50) NOT NULL UNIQUE
);

-- Kysymysten taulu
CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    maa VARCHAR(50) NOT NULL,
    kysymys TEXT NOT NULL,
    vaihtoehdot JSON NOT NULL,
    oikea_vastaus CHAR(1) NOT NULL,
    FOREIGN KEY (maa) REFERENCES airports(maa) ON DELETE CASCADE
);

-- Pelaajan tilan taulu (vain yksi rivi per sessio)
CREATE TABLE player_state (
    id INT PRIMARY KEY DEFAULT 1,
    nykyinen_maa VARCHAR(50) NOT NULL,
    tähdet INT NOT NULL DEFAULT 0,
    vieraillut_maat JSON NOT NULL DEFAULT '[]'
);



INSERT INTO airports (nimi, maa) VALUES
('Stockholm Arlanda Airport', 'Ruotsi'),
('Berlin Brandenburg Airport', 'Saksa'),
('Charles de Gaulle Airport', 'Ranska'),
('Roma Fiumicino Airport', 'Italia'),
('Adolfo Suárez Madrid-Barajas Airport', 'Espanja'),
('London Heathrow Airport', 'Yhdistynyt kuningaskunta'),
('Copenhagen Airport', 'Tanska'),
('Athens International Airport', 'Kreikka'),
('Dublin Airport', 'Irlanti'),
('Amsterdam Schiphol Airport', 'Alankomaat');



INSERT INTO questions (maa, kysymys, vaihtoehdot, oikea_vastaus) VALUES
('Ranska', 'Mikä ei ole Ranskan naapurivaltio?', '{"A": "Espanja", "B": "Andorra", "C": "Belgia"}', 'C'),
('Ranska', 'Missä näistä ei puhuta ranskaa?', '{"A": "Kanada", "B": "Norsunluurannikko", "C": "Kolumbia"}', 'C'),
('Ranska', 'Kuka heistä on ranskalainen?', '{"A": "Albert Einstein", "B": "Jacques Chirac", "C": "Celine Dion"}', 'B'),
('Ranska', 'Mikä näistä on ranskalainen automerkki?', '{"A": "Peugeot", "B": "Toyota", "C": "Honda"}', 'A'),
('Ranska', 'Mikä Kanadan osavalito on ranskankielinen?', '{"A": "Ontario", "B": "Quebec", "C": "Saskatchewan"}', 'B'),
('Ranska', 'Mikä on Ranskan väkiluku?(2023)', '{"A": "noin 68,3 miljoonaa", "B": "noin 52,1 miljoonaa", "C": "noin 52,1 miljoonaa"}', 'A'),

('Espanja', 'Mikä seuraavista on espanjankielinen maa?', '{"A": "Brasilia", "B": "Portugali", "C": "Argentiina"}', 'C'),
('Espanja', 'Mikä seuraavista on "sininen" espanjaksi?', '{"A": "Gato", "B": "Azul", "C": "Rápido"}', 'B'),
('Espanja', 'Mikä seuraavista on espanjalainen juhlapyhä?', '{"A": "Día de la Hispanidad", "B": "Oktoberfest", "C": "Hanami"}', 'A'),
('Espanja', 'Kuka on kuuluisa espanjalainen taidemaalari?', '{"A": "Pablo Picasso", "B": "Vincent van Gogh", "C": "Leonardo da Vinci"}', 'A'),
('Espanja', 'Mikä on Espanjan suurin saari?', '{"A": "Ibiza", "B": "Mallorca", "C": "Gran Canaria"}', 'B'),
('Espanja', 'Mikä seuraavista on espanjalainen tanssi?', '{"A": "Tango", "B": "Salsa", "C": "Flamenco"}', 'C'),

('Yhdistynyt kuningaskunta', 'Mikä on Yhdistyneen kuningaskunnan suurin saari?', '{"A": "Skotlanti", "B": "Wight", "C": "Iso-Britannia"}', 'C'),
('Yhdistynyt kuningaskunta', 'Mikä on Yhdistyneen kuningaskunnan kansallinen urheilulaji?', '{"A": "Jalkapallo", "B": "Rugby", "C": "Cricket"}', 'A'),
('Yhdistynyt kuningaskunta', 'Missä sijaitsee Yhdistyneen kuningaskunnan kuuluisin muistomerkki, Stonehenge?', '{"A": "Wales", "B": "Englanti", "C": "Skotlanti"}', 'B'),
('Yhdistynyt kuningaskunta', 'Kuka oli Yhdistyneen kuningaskunnan pääministeri vuonna 2023?', '{"A": "Theresa May", "B": "Rishi Sunak", "C": "Boris Johnson"}', 'B'),
('Yhdistynyt kuningaskunta', 'Mikä on Lontoon jälkeen Yhdistyneen kuningaskunnan suurin kaupunki?', '{"A": "Birmingham", "B": "Manchester", "C": "Glasgow"}', 'A'),
('Yhdistynyt kuningaskunta', 'Minkä tunntetun kirjailijan syntymäpaikka on Yhdistyneessä kuningaskunnassa?', '{"A": "Charles Dickens", "B": "Mark Twain", "C": "William Shakespeare"}', 'C'),

('Alankomaat', 'Mikä on Alankomaiden suurin kaupunki?', '{"A": "Rotterdam", "B": "Amsterdam", "C": "Haag"}', 'B'),
('Alankomaat', 'Mitä värejä on Alankomaiden lipussa?', '{"A": "Punaista, valkoista ja sinistä", "B": "Oranssia, valkoista ja mustaa", "C": "Punaista, vihreää ja valkoista"}', 'A'),
('Alankomaat', 'Minä vuonna päättyi Alankomaiden itsenäisyyssota?', '{"A": "1648", "B": "1789", "C": "1492"}', 'A'),
('Alankomaat', 'Kuka tunnettu hollantilainen taiteilija on kuuluisa "Tähtikirkas yö" -maalauksestaan?', '{"A": "Rembrandt", "B": "Vincent van Gogh", "C": "Pieter Bruegel"}', 'B'),
('Alankomaat', 'Missä on Alankomaidensuurin satama?', '{"A": "Haag", "B": "Amsterdam", "C": "Rotterdam"}', 'C'),
('Alankomaat', 'Mikä on Alankomaiden kuninkaallisen perheen virallinen väri?', '{"A": "Sininen", "B": "Punainen", "C": "Oranssi"}', 'C'),

('Saksa', 'Mikä on Saksan suurin kaupunki väkiluvultaan?', '{"A": "München", "B": "Berliini", "C": "Frankfurt"}', 'B'),
('Saksa', 'Mikä vuosi oli Saksan yhdistymisvuosi?', '{"A": "1989", "B": "1990", "C": "2000"}', 'B'),
('Saksa', 'Mikä on Saksan pisin joki?', '{"A": "Rein", "B": "Elbe", "C": "Tonava"}', 'A'),
('Saksa', 'Mitkä ovat Saksan lipun värit järjestyksessä ylhäältä alas?', '{"A": "Musta, punainen, keltainen", "B": "Punainen, musta, keltainen", "C": "Musta, keltainen, punainen"}', 'A'),
('Saksa', 'Minkä tunnetun saksalaisen säveltäjän teos on "Oodi ilolle"?', '{"A": "Johann Sebastian Bach", "B": "Richard Wagner", "C": "Ludwig van Beethoven"}', 'C'),
('Saksa', 'Mikä on Saksan tunnetuin festivaali, joka pidetään Münchenissä?', '{"A": "Berlinale", "B": "Carnival of Cultures", "C": "Oktoberfest"}', 'C'),

('Italia', 'Mikä on Italian asutuin kaupunki?', '{"A": "Rooma", "B": "Milano", "C": "Napoli"}', 'A'),
('Italia', 'Kuka on Italian nykyinen presidentti (2025)?', '{"A": "Giorgio Meloni", "B": "Sergio Mattarella", "C": "Giorgio Napolitano"}', 'B'),
('Italia', 'Mikä on Italian pinta-ala (km^2)?', '{"A": "302 073", "B": "100 557", "C": "204 077"}', 'A'),
('Italia', 'Milloin on Italian itsenäisyyspäivä?', '{"A": "20.10", "B": "17.3", "C": "13.6"}', 'B'),
('Italia', 'Mikä näistä EI ole Italian naapurivaltio?', '{"A": "Ranska", "B": "Sveitsi", "C": "Slovakia"}', 'C'),
('Italia', 'Minkä Italian kaupungin sanotaan olevan Renessanssin synnyinpaikka?', '{"A": "Rooma", "B": "Venetsia", "C": "Firenze"}', 'C'),

('Irlanti', 'Mikä on Irlannin kansallissymboli?', '{"A": "Apila", "B": "Ruusu", "C": "Ohdake"}', 'A'),
('Irlanti', 'Mikä on Irlannin virallinen valuutta?', '{"A": "Englannin punta", "B": "Euro", "C": "Dollari"}', 'B'),
('Irlanti', 'Mikä juhlapäivä on saanut alkunsa Irlannista?', '{"A": "Halloween", "B": "Joulu", "C": "Pääsiäinen"}', 'A'),
('Irlanti', 'Mikä on Irlannin lempinimi?', '{"A": "Kultamaa", "B": "Smaragdisaari", "C": "Safiirimaa"}', 'B'),
('Irlanti', 'Minkä valtameren rannalla Irlanti sijaitsee?', '{"A": "Tyyni valtameri", "B": "Jäämeri", "C": "Atlantin valtameri"}', 'C'),
('Irlanti', 'Mikä on tunnettu perinteinen Irlantilainen soitin?', '{"A": "Viulu", "B": "Harmonikka", "C": "Harppu"}', 'C'),

('Kreikka', 'Mikä on Kreikan pääuskonto?', '{"A": "Katolisuus", "B": "Ortodoksinen kristinusko", "C": "Islam"}', 'B'),
('Kreikka', 'Mikä meri ympäröi suurimman osan Kreikkaa?', '{"A": "Välimeri", "B": "Punainen meri", "C": "Mustameri"}', 'A'),
('Kreikka', 'Mikä tunnettu rakennus sijaitsee Kreikassa Akropoliksella?', '{"A": "Colosseum", "B": "Partheneon", "C": "Riemukaari"}', 'B'),
('Kreikka', 'Mikä kreikkalaisen mytologian jumala hallitsi Olymposta?', '{"A": "Poseidon", "B": "Hades", "C": "Zeus"}', 'C'),
('Kreikka', 'Mikä on tyypillinen Kreikkalainen ruokalaji?', '{"A": "Moussaka", "B": "Sushi", "C": "Paella"}', 'A'),
('Kreikka', 'Mikä on Kreikan virallinen valuutta?', '{"A": "Drachma", "B": "Punta", "C": "Euro"}', 'C'),

('Tanska', 'Mikä Tanskalainen kirjailija on tunnetuin maailmalla?', '{"A": "H. C. Andersen", "B": "Soren Kierkegrd", "C": "Niels Bohr"}', 'A'),
('Tanska', 'Mikä on Tanskan kansallisruoka?', '{"A": "Smörrebröd", "B": "Frikadeller", "C": "Stegtfläsk"}', 'C'),
('Tanska', 'Mikä on Tanskan suurin saari?', '{"A": "Själland", "B": "Fyn", "C": "Bornholm"}', 'A'),
('Tanska', 'Kuka on Tanskan nykyinen kuningas (2025)?', '{"A": "Frederik V", "B": "Frederik XI", "C": "Frederik X"}', 'C'),
('Tanska', 'Onko Kööpenhamina Tanskan asutuin kaupunki?', '{"Ei": "", "B": "Kyllä", "C": "Sillä on sama väkiluku, kuin Aarhusilla"}', 'B'),
('Tanska', 'Mikä on Tanskan valtiomuoto?', '{"A": "Demokraattinen tasavalta", "B": "Parlamentaarinen perustuslaillinen monarkia", "C": "Parlamentaarinen perustuslaillinen tasavalta"}', 'B'),

('Ruotsi', 'Mikä näistä EI ole Ruotsin vähemmistökieli?', '{"A": "Suomi", "B": "Romani", "C": "Saksa"}', 'C'),
('Ruotsi', 'Mikä on Ruotsin pinta-ala (km^2)?', '{"A": "450 295", "B": "300 566", "C": "841 786"}', 'A'),
('Ruotsi', 'Mikä on ruotsin kuninkaallinen vaalilause?', '{"A": "Ruotsi eteenpäin ruhtinaallisesti", "B": "Ruotsi eteenpäin prinsessan nimeen", "C": "Ruotsin hyväksi ajan hengessä"}', 'C'),
('Ruotsi', 'Kuka on Ruotsin nykyinen kuningas (2025)?', '{"A": "Ulf Kristensson V", "B": "Kaarle XVI Kustaa", "C": "Kaarle X Kustaa"}', 'B'),
('Ruotsi', 'Mikä on Ruotsin valtiomuoto?', '{"A": "Perustuslaillinen monarkia", "B": "Demokraattinen monarkia", "C": "Parlamentaarinen perustuslaillinen monarkia"}', 'A'),
('Ruotsi', 'Mikä näistä on Ruotsalainen yritys?', '{"A": "Prada", "B": "Skanska", "C": "Cubus"}', 'B');