<?php

// Percorso del file HTML da leggere e scrivere
$inputFilePath = 'C:\xampp\htdocs\DCRB\food\Food.html';
$outputFilePath = 'C:\xampp\htdocs\DCRB\food\Food2.html';

// Leggi il contenuto del file HTML
$htmlContent = file_get_contents($inputFilePath);

// Rimuovi tutti i tag HTML mantenendo il testo leggibile
$textContent = strip_tags($htmlContent);

// Rimuovi spazi bianchi multipli e spazi all'inizio/fine del testo
$textContent = preg_replace('/\s+/', ' ', $textContent);

// Rimuovi il contenuto tra parentesi tonde e quadre
$textContent = preg_replace('/\((?:[^()]|(?R))*\)|\[(?:[^\[\]]|(?R))*\]|\{(?:[^{}]|(?R))*\}/', '', $textContent);


$textContent = preg_replace('/\([^)]*\)/', '', $textContent);

// Rimuovi spazi all'inizio/fine del testo, inclusi parentesi tonde e quadre
$textContent = trim($textContent, " \t\n\r\0\x0B()[]");

// Scrivi il contenuto nel nuovo file di testo
file_put_contents($outputFilePath, $textContent);

echo "Testo estratto. È stato scritto nel file: $outputFilePath";

?>