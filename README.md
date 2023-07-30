# Music Album Similarity 

## File Descriptions 


### Repository Structure
![Repository Structure](/data/File%20Structure.drawio.png)




### Order of Running Files 
![Order of Running Files](/data/Order%20of%20Running%20Files.drawio.png)

### Root 


<b>summary.pdf</b> - Final Report about the observations and findings 

<b>requirements.txt</b>  - File containing list of packages required to run the source code 

<b>web_scrapper.py</b>- Web Scrapper for scrapping data from the link

```bash
python web_scrapper.py https://www.pastemagazine.com/music/best-selling-albums/the-best-selling-albums-of-all-time/ data/music_album_data.csv
```

<b>preprocessor.py</b> - File for preprocessing the descriptions collected 

```bash
python preprocessor.py data/music_album_data.csv data/preprocessed.csv 
```


### Notebooks


<b>Correlation Analysis.ipynb</b> - Result Analysis from Correlation Coefficient calculations 

<b>Entity Recognition.ipynb</b> - Analysis of Entity Recognition performed using SpaCy 

<b>similarity_analysis_jaccard.ipynb</b> - Analysis of results of similarity obtained by using Jaccard Similarity 


<b>similarity_analysis_cosine.ipynb</b> - Analysis of results of similarity obtained by using Cosine Similarity + Word2Vec


<b>similarity_analysis_sentence_transformer.ipynb</b> - Analysis of results of similarity obtained by using Cosine Similarity + Sentence Transformers 


<b>faiss_implementation.ipynb</b> - Analysis of results of runtime using Faiss along with Sentence Transformers 


<b>knowledge_graph.ipynb</b> - knowledge graph mapping of the dataset. 


### Data Files 


<b>music_album_data.csv</b> - The CSV file that contains the web scrapped information. 

<b>preprocessed.csv</b> - The CSV file that contains the preprocessed description data 

<b>entity_dictionary.pickle</b> - Pickle file for storing description and their entites 

<b>music_album_similarity</b> - Stored FAISS Index

<b>network_graph.html</b> - A More elastic visualization of the knowledge graph that was created. 



