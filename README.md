# Galaxy Morphology Classification

Automated galaxy morphology classification using deep learning on the Galaxy Zoo 2 dataset, leveraging Azure for scalable storage and retrieval.

---

## 🚀 Features

* **Multiple Architectures**: Compare a custom CNN, EfficientNet‑B0, ResNet‑18, ResNet‑50, and Vision Transformer (ViT).
* **Azure Integration**: Load high-resolution galaxy images from Azure Blob Storage and labels from Azure SQL Database.
* **Extensive Augmentation**: Scale jittering, random rotations, flips, color jitter, and normalization to combat class imbalance.
* **Modular Design**: Separate scripts for data ingestion, augmentation, model definitions, training, and exports.
* **End‑to‑End Pipeline**: CLI (`main.py`) and Jupyter notebooks for exploration, training, evaluation, and visualization.

---

## 📋 Prerequisites

* Python 3.8+
* PyTorch 1.9+
* torchvision 0.10+
* azure-storage-blob 12.x
* pyodbc 4.x
* scikit-learn 1.x
* matplotlib 3.x, seaborn 0.11+

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## 🔧 Setup & Configuration

1. **Azure Credentials**

   * Export your Azure Blob Storage and SQL connection strings as environment variables:

     ```bash
     export AZURE_STORAGE_CONNECTION_STRING="<your_connection_string>"
     export AZURE_SQL_CONN_STR="Driver={ODBC Driver 17 for SQL Server};Server=<server>;Database=<db>;UID=<user>;PWD=<pass>"
     ```
2. **Download Labels**

   * Run the Kaggle API or your own script to download the GZ2 CSV labels locally.
   * Upload labels to your Azure SQL table if not already present.

---

## 📂 Project Structure

```text
├── azure_blob_dataset.py    # Custom PyTorch Dataset loading from Azure Blob & SQL
├── data_import.py           # Image file ingestion, preprocessing, label mapping
├── rotate.py                # Data augmentation transforms (random rotations)
├── dl_models.py             # CNN, EfficientNet, ResNet, and ViT definitions
├── dl_proj_TEST.py          # Quick training & evaluation harness
├── dl_project_main.ipynb    # EDA, training loops, and result visualization
├── main.py                  # CLI wrapper for training, evaluation, checkpointing
├── blob_export.py           # Push processed outputs back to Azure Blob Storage
├── sql_export.py            # Insert metrics/predictions into Azure SQL Database
├── system_check.ipynb       # Environment and hardware verification
├── best_model.pt            # Checkpoint of top-performing model
├── efficientnet_B0_model_checkpoint.pt
├── requirements.txt         # Project dependencies
├── SYSC_5108_Final_Report.pdf # Detailed methodology and results
└── README.md                # This file
```

---

## 💡 Quick Start

### 1. Inspect Environment

```bash
python system_check.ipynb  # or run as script to verify GPU/CPU, library versions
```

### 2. Data Pipeline

```bash
python data_import.py --source-folder ./images --label-csv ./labels.csv --output-dir ./processed
```

Loads raw images from local or Azure Blob, preprocesses, and saves ready-to-train data.

### 3. Train a Model

```bash
python main.py \
  --arch efficientnet_b0 \
  --train-dir ./processed/train \
  --val-dir ./processed/val \
  --epochs 20 \
  --batch-size 32 \
  --lr 1e-4
```

### 4. Evaluate & Visualize

* Use `dl_proj_TEST.py` for quick back-to-back runs.
* Open `dl_project_main.ipynb` to view loss curves, scatter plots, and metric summaries.

---

## 📈 Results

* **Best Model**: ResNet‑50 achieved lowest test RMSE and MAE across 37 morphology outputs.
* **Metrics**: MSE, RMSE, MAE, training & validation loss curves, and per-channel scatter plots included in the final report.
* **Report**: See `dl_project_main.ipynb` for detailed tables, figures, and comparative analysis.

---

## 🔮 Future Work

* **Self‑Supervised Learning**: Explore SimCLR or MoCo pretraining on unlabeled galaxy images.
* **Multi‑Task Learning**: Jointly predict multiple morphology labels for richer representations.
* **Synthetic Data Generation**: Use GANs to augment rare classes and improve model robustness.
* **Explainability**: Integrate Grad‑CAM or SHAP to visualize model attention on galaxy features.

---

## 📄 License

This project is licensed under the [GPL‑3.0 License](LICENSE) as stated in the repository.

---

## 🙏 Contributing

Feel free to open issues or submit pull requests to improve data pipelines, add new models,
or extend visualizations. Please adhere to the existing code style and include tests where
applicable.
