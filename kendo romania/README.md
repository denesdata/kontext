# Romania Kendo Stats  
#### 25 years of Kendo Competition History in Romania, visualized  
Created by **[Dénes Csala](//csaladen.es)** | 2019 | MIT License 
  
For any improvement suggestions and spotted processing mistakes drop me a message on [Facebook](//facebook.com/csaladenes).  
If you would like to have your country/club data visualized in a similar manner, or any other data visualization and analytics consultancy inquiries contact me at [mail@csaladen.es](mailto:mail@csaladen.es)

The general structure of the repository is the following:  
 - `/data`
   - `/raw`: this where you place the downloaded data from the official data source, sorted by years and competitions, only keep those that have relevant data for matches only
   - `/ocr`: this is where the data gets saved after an [OCR](https://en.wikipedia.org/wiki/Optical_character_recognition) has been performed - this is necessary for some older files in image format 
   - `/manual`: this is where manually extracted matches from old image files get placed - they should follow the `2018 CN` format, i.e. all matches in one sheet
   - `/export`: this is where we save the dataformatted for loading into the viz
   - `/clean`: this is where all the processed, cleaned data ends up - they should follow the `2018 CN` format, i.e. all matches in one sheet
 - `/scripts`: this is the main code repository for all data processing scripts
 - `/viz`: this is where the visualization files get saved - they are created using PowerBI and load data from `/data/clean`