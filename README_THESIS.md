# Thesis guide 


## Files and their content 
direct_citations.json                         final_citation_data.json  id2title.json  not_found_errors.json  sample.json    title_found.json      valid_ids.json
directly_cited_articles_not_in_metadata.json  hard_negatives.json       metadata.json  not_found.json         title2id.json  title_not_found.json

### direct_citations.json
```json
 "566609": {
    "1237": {
      "count": 5
    },
    "31554": {
      "count": 5
    },
    "10875": {
      "count": 5
    },
    "13201": {
      "count": 5
    },
    "54396": {
      "count": 5
    },
    "7120": {
      "count": 5
    }
  },
```
- Parent keys are article ids
- Child keys are articles ids which are cited by parent (count=5) represents direct citation.


### directly_cited_articles_not_in_metadata.json
- Type is list of integers
- Articles which are cited by some article but are not found from the metadata. 
```json
[
  "1893",
  "758882",
  "1470",
  "1667107",
  "430028",
  "510523",
  "491833",
  "519312",
  "519114",
  "1861"
]

```
### hard_negatives.json
- similar structure than direct_citations but now count = 1 represents hard negative.


1. Query paper cites papers A B and C 
2. Paper A cites paper D
3. Paper D cites paper A 

=> This can be denoted as "hard negatives" since Paper D cites query paper but query paper does not cite paper D
but cites a paper that cites paper A.

```json
{
  "529035": {
    "642528": {
      "count": 1
    },
    "234660": {
      "count": 1
    },
    "175": {
      "count": 1
    },
    "65255": {
      "count": 1
    },
    "270": {
      "count": 1
    }
  }
}

```


### final_citation_data.json

### id2title.json
- Mapping data where each wikipedia article id is mapped to textual title. 
```json
{
  "273141": "dohan kansainvälinen lentoasema",
  "273153": "galilein luku",
  "273154": "galileon luku",
  "273157": "delta force",
  "273158": "1st sfod-d",
  "273161": "symkaria",
  "273162": "möyly"

}
```
### title2id.json
- Mapping data from title to id 
```json
{
  "luokka:animaatiostudiot": "239045",
  "alphaville (yhtye)": "239046",
  "akatemialainen skeptisismi": "239052",
  "pontocho": "239053",
  "arimatti jutila": "239070"

}
```

### metadata.json
- The basis data for everything. Abstract, title and paper_id. The parent key is the corresponding wikipedia article id.
```json
{
  "535535": {
    "abstract": "Estadio La Rosaleda on jalkapallostadion, joka sijaitsee Málagassa Espanjassa. Se toimii Espanjan pääsarjajoukkueen Málaga Club de Fútbolin kotikenttänä. Ensimmäinen ottelu stadionilla pelattiin CD Malacitanon ja AD Ferroviarian välillä.  Stadion toimi yhtenä pelipaikkana Espanjan jalkapallon maailmanmestaruuskilpailuissa vuonna 1982.",
    "title": "La Rosaleda",
    "paper_id": "535535"
  },
  "535536": {
    "abstract": "Esko Johannes Oikarinen (s. 13. kesäkuuta 1949 Kajaani) on suomalainen lakimies, joka toimi Rovaniemen hovioikeuden presidenttinä. Esko Oikarinen syntyi kirvesmies Lauri Oikarisen ja Linnea Kemppaisen perheeseen. Hänen puolisonsa vuodesta 1970 on toimialajohtaja Kerttu Pyykkönen. Oikarinen tuli ylioppilaaksi 1968 ja valmistui oikeustieteen kandidaatiksi Helsingin yliopistosta 1971, varatuomarin arvon hän sai 1974. Oikarinen oli Kajaanin tuomiokunnan notaari 1973, käräjätuomari 1976–1981, kihlakuntatuomari 1990–1993 ja käräjäoikeuden laamanni 1993–1997. Itä-Suomen hovioikeuden esittelijänä Oikarinen toimi 1973–1975, Pieksämäen tuomiokunnan käräjätuomarina 1975–1976 ja Rovaniemen hovioikeuden hovioikeusneuvoksena 1981–1989. Hovioikeuden presidentiksi hänet nimitettiin 1997. Oikarinen jäi eläkkeelle vuonna 2013, hänen seuraajakseen valittiin 1.1.2014 alkaen Marianne Wagner-Prenner.",
    "title": "Esko Oikarinen",
    "paper_id": "535536"
  }
}

```


### not_found_errors.json
### not_found.json
### sample.json
### title_found.json
### title_not_found.json
### valid_ids.json


## Scripts 

## 7-validate-data.sh 
- Checks if metadata.json and final_citation_data.json are ok. 
- Basicly - if all the keys in final_citation_data.json are found from metadata. 
- 