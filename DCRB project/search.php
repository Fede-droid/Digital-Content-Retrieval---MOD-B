<?php

error_reporting(E_ALL);
ini_set('display_errors', 1);

// Funzione per eseguire la ricerca all'interno dei file
function searchInFiles($directory, $searchString) {
    // Inizializza l'array per memorizzare i risultati
    $results = array();

    // Verifica se il percorso fornito è una directory
    if (is_dir($directory)) {
        // Apre la directory
        $handle = opendir($directory);

        // Itera su tutti gli elementi nella directory
        while (($item = readdir($handle)) !== false) {
            // Ignora le directory speciali
            if ($item != "." && $item != "..") {
                // Costruisci il percorso completo dell'elemento
                $path = $directory . "/" . $item;

                // Verifica se l'elemento è una directory
                if (is_dir($path)) {
                    // Se è una directory, esegui la ricerca ricorsivamente
                    $subResults = searchInFiles($path, $searchString);
                    // Unisci i risultati della ricerca ricorsiva con i risultati correnti
                    $results = array_merge($results, $subResults);
                } else {
                    // Se l'elemento è un file, cerca la stringa al suo interno
                    $content = file_get_contents($path);
                    $occurrences = substr_count($content, $searchString);
                    // Aggiungi i risultati al risultato finale
                    $results[] = array(
                        'path' => $path,
                        'type' => 'file',
                        'occurrences' => $occurrences
                    );
                }
            }
        }

        // Chiudi la directory
        closedir($handle);
    }

    // Restituisci i risultati
    return $results;
}

// Directory radice da cui iniziare la ricerca
$rootDirectory = "C:\xampp\htdocs\DCRB";

// Stringa da cercare nei file
$searchString = "food";

// Esegui la ricerca
$searchResults = searchInFiles($rootDirectory, $searchString);

// Visualizza i risultati
foreach ($searchResults as $result) {
    echo "Path: " . $result['path'] . "<br>";
    echo "Type: " . $result['type'] . "<br>";
    if ($result['type'] == 'file') {
        echo "Occurrences: " . $result['occurrences'] . "<br>";
    }
    echo "<br>";
}

?>
