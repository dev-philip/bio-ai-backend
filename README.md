# 📚 Utilizing Knowledge Graphs for the Detection of Potential Null Results

## 🧠 Problem Statement

The **"null result bias"** in scientific publishing leads to the underreporting of experiments that fail to reject the null hypothesis. This lack of transparency contributes to:

- Wasted research efforts
- Redundant experimentation
- Slowed scientific progress

> _Read more about this issue in the [File Drawer Problem](https://ai-docs.bio.xyz/vision-and-mission/the-problems-in-science#the-file-drawer-problem)._

While direct evidence of null results is rare, subtle contextual clues within manuscripts and **patterns in knowledge graphs** may hint at areas where hypotheses were tested but not validated.

---

## 🚧 Challenge

**Develop a system** capable of analyzing scientific literature and identifying likely cases where null results exist, even if they are not explicitly published.

---

## 🔍 Detailed Description

### 📝 Manuscript Analysis

Use Natural Language Processing (NLP) techniques to identify contextual clues that may suggest null or inconclusive results, such as:

- Failed replication attempts
- Inconclusive or negative outcomes
- Experimental design limitations
- Contradictory findings
- Uncertainty or cautious language

### 🌐 Knowledge Graph Analysis

Leverage or build knowledge graphs to identify patterns such as:

- Frequently tested hypotheses lacking evidence
- Conflicting or contradictory relationships
- High research activity with low conclusiveness
- Concept clusters with weak validation

### 🎯 Hypothesis Validation Probability

Assign confidence scores indicating the likelihood that a hypothesis yielded null results, based on:

- Mention frequency in literature
- Strength or absence of supporting evidence
- Detected contextual clues
- Conflicts with known scientific facts

---

## 📤 Output

- A **list of hypotheses** likely to have null results
- **Justifications** including text evidence and knowledge graph insights
- A **confidence score** for each hypothesis
- **Visualizations** of knowledge graph patterns

---

## 🛠️ Potential Technologies

- **Natural Language Processing (NLP)** – e.g., spaCy, NLTK, transformers
- **Knowledge Graphs** – e.g., Neo4j, RDF, NetworkX
- **Machine Learning** – for classification, scoring, and pattern detection
- **Data Visualization** – e.g., D3.js, matplotlib, Cytoscape

---

## 📏 Evaluation Metrics

- Accuracy (compared to expert/human judgment)
- Clarity and relevance of justifications
- Usefulness of confidence scores
- Effectiveness in visualizing relationships

---

## 🎯 Desired Outcomes

- A working system to detect potential null results
- A dataset of flagged hypotheses and justifications
- New insights into null result indicators in text and graphs
- A tool to help **reduce null result bias** in scientific research

---

## 📌 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Contributions

Pull requests and contributions are welcome! Please open an issue first to discuss changes or new features.

---

## How to run the project

1. Create a New Conda Environment
   `conda create -n ai-bio-app python=3.11`
2. Create a New Conda Environment
   `conda activate ai-bio-app`

3. Install pip inside the conda environment (optional, but safe to check)
   `conda install pip`

4. Install your dependencies from requirements.txt
   `pip install -r requirements.txt`

5. Verify Installed Packages
   `pip list`

6. If you want to save the exact environment for others to use with Conda, you can later export:
   `conda env export > environment.yml`
   OR recreate it using:
7. `conda env create -f environment.yml`

8. Use pip install and add package to requirement.txt file
   `pip install pydantic-settings`
   `echo pydantic-settings >> requirements.txt`
   OR Option 2: Re-freeze your environment. After installing the package, run:
   `pip freeze > requirements.txt`
   Note : This overwrites requirements.txt with everything currently installed in your environment — good for syncing it all, but might include extras you don’t want.

9. Start Project Server :
   `uvicorn app.main:app --reload`

## Some endpoint to check

http://127.0.0.1:8000 → Welcome message
http://127.0.0.1:8000/docs → Swagger UI

## Example of git workflow

# 1. Create and switch to the new branch

git checkout -b nlp-pipeline

# 2. Now you're on nlp-pipeline branch. Just add and commit your changes:

git add .
git commit -m "Initial commit for NLP pipeline"

# 3. Push the branch to remote

git push origin nlp-pipeline

# 4. Switch back to the main branch

git checkout main

# 5. Pull latest changes from remote (optional, to sync)

git pull origin main

# 6. Merge the changes from nlp-pipeline into main

git merge nlp-pipeline

# 7.

git push origin main
