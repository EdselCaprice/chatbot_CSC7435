# Chatbot Project

## Overview
 The Tax Research Chatbot will be a retrieval augmented generation (RAG) solution built on top of OpenAI’s GPT-5 Large Language Model. This tool will be specifically aimed at public accounting professionals who specialize in state and local corporate income tax. The scope of this tool will not provide support for federal income tax topics or topics related to the taxation of passthrough entities such as partnerships, Limited Liability Companies, or entities who have elected S-Corporation status. The focus of this tool will include, but is not limited to, state apportionment methodologies as defined by state and local tax laws, state corporate income tax rates, allowable carry forward periods of net operating losses, state economic nexus thresholds, and limitations regarding the utilization of net operating losses as it relates to tax law changes introduced by the 2017 CARES Act.

##  Key features of the application include:
- A web-based interface that can be accessed on both desktop and mobile browsers
- A retrieval augmented generation solution that leverages domain specific research documentation pre-compiled by a domain expert.
- Limit the scope of questions that the Tax Research Chatbot will provide responses to in order to prevent hallucinations and limit responses to questions that are outside the domain of the research provided.

## Technology Stack
- Frontend: React
- Backend: Python-Flask
