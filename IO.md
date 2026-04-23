# Dataset I/O Format Reference

## Input Formats (Raw Source Data)

### 1. <DATASET_1> — `<file format>`

<Plain language description: what this data is, where it comes from, how it is structured.>

<N> samples, stored as `<format>`. Each sample contains `<key fields>`.

```
<Paste an actual data example here — abbreviated if large>
```

| Field | Type | Shape / Range | Description |
|-------|------|---------------|-------------|
| `<field_name>` | `<type>` | `<shape or value range>` | `<what it represents>` |
| `<field_name>` | `<type>` | `<shape or value range>` | `<what it represents>` |

### 2. <DATASET_2> — `<file format>`

<Same structure as above.>

---

## Feature Engineering Output

### <METHOD_NAME> — `<output format>`

<Description of how raw input is transformed by this feature engineering method.>

- **Input:** `<description of what goes in>`
- **Output:** `<description of what comes out>`
- **Config:** `configs/feature/<method>.yaml`
- **Cache:** `data/processed/<method>/`

```
<Paste an actual example of engineered features>
```

| Field | Type | Shape | Description |
|-------|------|-------|-------------|
| `<field>` | `<type>` | `<shape>` | `<description>` |

---

## Model Input Format

<Description of the final tensor/array that goes into the model after all preprocessing.>

```
<Actual example with shapes and dtypes>
```

| Tensor | Shape | Dtype | Description |
|--------|-------|-------|-------------|
| `input` | `<shape>` | `<dtype>` | `<what it represents>` |
| `target` | `<shape>` | `<dtype>` | `<ground truth>` |

---

## Model Output Format

<Description of what the model produces.>

```
<Actual example>
```

| Output | Shape | Dtype | Description |
|--------|-------|-------|-------------|
| `prediction` | `<shape>` | `<dtype>` | `<what it represents>` |

---

## Pipeline Overview

```
<RAW_FORMAT> (raw source data)
    │
    ▼
Feature Engineering (configs/feature/<method>.yaml)
    │
    ▼
<PROCESSED_FORMAT> (data/processed/<method>/)
    │
    ▼
Model Input: <TENSOR_SHAPE>
    │
    ▼
<MODEL_ARCHITECTURE>
    │
    ▼
Model Output: <OUTPUT_SHAPE>
```
