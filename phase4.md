# Phase 4

- Dataset Preparation Pipeline
- Dataset Cleaning
- URL Validation
- URL Normalization
- Duplicate Removal
- Invalid URL Removal
- Label Assignment
- Dataset Balancing
- Feature Matrix Generation
- Train/Test Split
- Logging Support
- Progress Tracking (tqdm)
- Benchmark Support
- ML-Ready CSV Generation
- Phase 1 Feature Extractor Integration
- Scikit-Learn Integration
- Pandas-Based Processing
- Error Handling
- Automated Dataset Processing Pipeline

Datasets:

- Phishing Dataset (65,213 URLs)
- Legitimate Dataset (50,000 URLs)

Pipeline:

- Load Datasets
- Clean Data
- Remove Duplicates
- Remove Invalid URLs
- Assign Labels
- Balance Dataset
- Extract Features
- Generate Feature Matrix
- Split Train/Test Data

Generated Files:

- cleaned.csv
- balanced.csv
- feature_matrix.csv
- train.csv
- test.csv

Scripts:

- clean.py
- balance.py
- build_features.py
- split.py
- common.py

Dataset Statistics:

- Initial Dataset Size: 115,213 URLs
- Duplicates Removed: 4
- Invalid URLs Removed: 2
- Cleaned Dataset: 115,207 URLs
- Balanced Dataset: 99,996 URLs
- Training Dataset: 79,996 URLs
- Testing Dataset: 20,000 URLs

Folder Structure:

- datasets/raw/
- datasets/processed/
- datasets/features/
- datasets/splits/
- datasets/scripts/
- datasets/tests/

Tests:

- Phase 4: 24/24 Passed
- Total Project Tests: 134/134 Passed

Status:

COMPLETED