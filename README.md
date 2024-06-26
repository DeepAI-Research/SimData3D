# SimData3D Dataset

<img src="simdatalogo.jpeg" />

A filtered down dataset of the [cap3d](https://cap3d-um.github.io/) dataset, now containing only the most simple and quality of objects.

## Overview

This project provides a script to filter captions from the `cap3d` dataset to remove verbose captions with too many objects. The filtered dataset can be used for various machine learning tasks where simpler captions are preferred.

## Requirements

This `install.sh` script will install spaCy and download the `en_core_web_sm` model. Make sure the script has executable permissions. You can set executable permissions with:

```bash
chmod +x install.sh
./install.sh
```

## Clone

1. Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/RaccoonResearch/simdata
cd simdata
```
