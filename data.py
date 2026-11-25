"""Seed data. Edit this file to add papers, topics and opportunities, then redeploy."""
PAPERS = [
 ("SciBERT: A Pretrained Language Model for Scientific Text","Beltagy, Lo, Cohan",2019,"BERT pretraining","research","language model scientific text NLP","BERT-based language model pretrained on scientific text. Improves understanding of scientific text. Limitation: it is only a language model; it does not suggest topics, summarise for beginners or find research gaps.","https://arxiv.org/abs/1903.10676"),
 ("SPECTER: Document-level Representation Learning using Citation-informed Transformers","Cohan et al.",2020,"transformer embeddings","research","embeddings paper similarity citation","Transformer embeddings trained on citation links to find similar papers. Limitation: does not extract methods, datasets or limitations and gives no guidance on choosing a topic.","https://arxiv.org/abs/2004.07180"),
 ("S2ORC: The Semantic Scholar Open Research Corpus","Lo et al.",2020,"corpus","dataset","corpus scholarly papers dataset","Large corpus of scholarly papers. Limitation: provides the data but no tools to turn papers into a topic, gap or research roadmap for a beginner.","https://arxiv.org/abs/1911.02782"),
 ("TLDR: Extreme Summarization of Scientific Documents","Cachola et al.",2020,"extreme summarisation","research","summarisation scientific documents","One-sentence summarisation model for scientific papers. Limitation: one-sentence summaries lose dataset, metrics, results and limitations.","https://arxiv.org/abs/2004.15011"),
 ("A Discourse-Aware Attention Model for Abstractive Summarization of Long Documents","Cohan et al.",2018,"attention summarisation","research","abstractive summarisation long documents","Discourse-aware attention for abstractive summarisation of long papers. Limitation: does not compare papers or find limitations repeated across them.","https://arxiv.org/abs/1804.05685"),
 ("Multi-Task Identification of Entities, Relations, and Coreference for Scientific Knowledge Graph Construction","Luan et al.",2018,"multi-task extraction","research","information extraction knowledge graph scientific","Multi-task information extraction of tasks, methods, metrics and relations into a scientific knowledge graph. Limitation: does not use them to suggest research gaps.","https://arxiv.org/abs/1808.09602"),
 ("Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks","Lewis et al.",2020,"RAG","research","retrieval generation RAG question answering","Retriever plus generator grounds answers in retrieved text. Limitation: not designed for scholarly paper analysis or source links for students.","https://arxiv.org/abs/2005.11401"),
]
TOPICS = [
 ("CSE/AIML","Automatic summarisation of scientific papers","summarisation NLP transformers papers","Python, NLP basics, scikit-learn","beginner"),
 ("CSE/AIML","Research gap detection from literature using NLP","gap extraction embeddings knowledge graph","Python, embeddings, information extraction","advanced"),
 ("CSE/AIML","Retrieval-augmented question answering over papers","RAG retrieval vector database","Python, embeddings, LLM APIs","advanced"),
 ("CSE/AIML","TF-IDF based paper recommendation for students","TF-IDF cosine similarity recommendation","Python, scikit-learn","beginner"),
 ("CSE/AIML","Crop disease detection using CNN","deep learning CNN image classification agriculture","Python, PyTorch/Keras","intermediate"),
 ("ECE","Low-power IoT sensor networks for smart farming","IoT sensors LoRa energy agriculture","Embedded C, sensors","intermediate"),
 ("Mechanical","Topology optimisation for lightweight parts","topology optimisation FEA lightweight","CAD, FEA","intermediate"),
 ("Civil","Recycled aggregate concrete strength","recycled aggregate concrete strength sustainability","Material testing","beginner"),
]
# verified=0 -> shown with a warning. Set to 1 only after you check the official site.
OPPORTUNITIES = [
 ("Summer Research Fellowship Programme (Indian Academies of Sciences)","fellowship","UG/PG students, see official page","Check official site","Stipend/guidance, see official page","https://www.ias.ac.in",0),
 ("NPTEL online courses","learning","Open to all","Rolling, see official page","Free courses; paid certification","https://nptel.ac.in",0),
 ("VTU Research and Innovation","institution","VTU-affiliated students","Check official site","See official page","https://vtu.ac.in",0),
]
