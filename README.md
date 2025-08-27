# Overview

- Original BKEE data can be found at https://github.com/nhungnt7/BKEE
- The model used for predicting data: https://arxiv.org/abs/2103.09330

```
├── assets
├── final_data # processed data
│   ├── processed # processed from original to match the code
│   ├── processed_enriched # enrichment attemp 1
│   ├── processed_enriched_2 # enrichment attemp 2
│   └── processed_enriched_3 # enrichment attemp 3
├── generate_silver_corpus.py # The file to generate silver corpus
├── raw # raw texts, crawled from BaoMoi
├── README.md
├── Report.pdf
├── result # the data obtained after predicting using FourIE model
├── schema_augment.py # schema augmentation code
├── trend_detection.py # trend detection code
```

