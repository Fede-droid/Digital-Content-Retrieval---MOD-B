from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_content = []
        self.skip_tags = {'script', 'style'}  # Lista dei tag da saltare
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag

    def handle_endtag(self, tag):
        self.current_tag = None

    def handle_data(self, data):
        if self.current_tag not in self.skip_tags:
            self.text_content.append(data.strip())

def extract_text_from_html(html_file, output_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

        # Inizializza il parser HTML e analizza il contenuto HTML
        parser = TextExtractor()
        parser.feed(html_content)

    # Scrivi il testo estratto nel nuovo file di output
    with open(output_file, 'w', encoding='utf-8') as f:
        for text in parser.text_content:
            if text:
                f.write(text + '\n')

    print("Testo estratto. È stato scritto nel file:", output_file)

# Percorsi dei file HTML da leggere e del file di output
input_html_file = r'C:\xampp\htdocs\DCRB\food\Food.html'
output_text_file = r'C:\xampp\htdocs\DCRB\food\Food3.html'

# Esegui la funzione per estrarre il testo dal file HTML
extract_text_from_html(input_html_file, output_text_file)
