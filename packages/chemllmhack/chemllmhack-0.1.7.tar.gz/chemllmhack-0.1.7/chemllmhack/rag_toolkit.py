# -*- coding: utf-8 -*-
"""
File name: rag_tools.py
Author: Bowen
Date created: 24/7/2024
Description: This Python file provides toolkit for RAG research.

Copyright information: © 2024 QDX
"""

import json
import os
from langchain import hub
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.load import dumps, loads
from operator import itemgetter

from langchain_core.prompts import FewShotChatMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnableWithMessageHistory

os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

def reciprocal_rank_fusion(results: list[list], k=60, max_docs=20):
    """
    Reciprocal_rank_fusion that takes multiple lists of ranked documents
    and an optional parameter k used in the RRF formula

    Args:
        results: list of lists of ranked documents
        k: optional parameter used in the RRF formula

    Returns: list of reranked documents

    """

    fused_scores = {}

    for docs in results:
        for rank, doc in enumerate(docs):
            doc_str = dumps(doc)
            if doc_str not in fused_scores:
                fused_scores[doc_str] = 0

            previous_score = fused_scores[doc_str]

            fused_scores[doc_str] += 1 / (rank + k)

    reranked_results = [
        (loads(doc), score)
        for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    ]

    reranked_results = reranked_results[:max_docs]

    return reranked_results


def get_unique_union(documents: list[list]):
    """
    Get the unique union of retrieved documents.
    Args:
        documents: documents retrieved from the vector database in a list of lists.

    Returns: flattened The list of unique documents.

    """

    # Flatten list of lists, and convert each Document to string
    flattened_docs = [dumps(doc) for sublist in documents for doc in sublist]
    # Get unique documents
    unique_docs = list(set(flattened_docs))
    # Return
    return [loads(doc) for doc in unique_docs]


def multi_query_rag(question, module_name, vectordb_path):
    """
    Query the RAG model with multiple questions.
    Args:
        experiment_context: Your experiment process
        module_name: the module name you want the RAG to focus on.
        vectordb_path: the path to the vector database.
    Returns: the list of answers from the RAG model.
    """

    embedding_function = OpenAIEmbeddings()

    keyword = module_name
    vectorstore = Chroma(persist_directory=vectordb_path,
                         embedding_function=embedding_function, collection_name=keyword)

    retriever = vectorstore.as_retriever()

    # Multi Query: Different Perspectives
    template = """You are an AI language model assistant. Your task is to generate five 
    different versions of the given user question to retrieve relevant documents from a vector 
    database. By generating multiple perspectives on the user question, your goal is to help
    the user overcome some of the limitations of the distance-based similarity search. 
    Provide these alternative questions separated by newlines. 

    Original question: {question}"""


    template = template

    prompt_perspectives = ChatPromptTemplate.from_template(template)

    from langchain_openai import ChatOpenAI

    generate_queries = (
            prompt_perspectives
            | ChatOpenAI(temperature=0, model="gpt-4-turbo")
            | StrOutputParser()
            | (lambda x: x.split("\n"))
    )


    retrieval_chain_fusion = generate_queries | retriever.map() | reciprocal_rank_fusion
    docs = retrieval_chain_fusion.invoke({"question": question})

    # RAG
    template = """Answer the following question based on this context:

    {context}

    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatOpenAI(temperature=0, model="gpt-4-turbo")

    final_rag_chain = (
            {"context": retrieval_chain_fusion,
             "question": itemgetter("question")}
            | prompt
            | llm
            | StrOutputParser()
    )

    ans = final_rag_chain.invoke({"question": question})

    return ans


def format_qa_pair_recursive(question, answer):
    """
    Format the question and answer pair.
    Args:
        question:  the input question.
        answer:  the input answer.

    Returns: the formatted question and answer pair.

    """

    formatted_string = ""
    formatted_string += f"Question: {question}\nAnswer: {answer}\n\n"
    return formatted_string.strip()


def format_qa_pairs_individual(questions, answers):
    """Format Q and A pairs"""

    formatted_string = ""
    for i, (question, answer) in enumerate(zip(questions, answers), start=1):
        formatted_string += f"Question {i}: {question}\nAnswer {i}: {answer}\n\n"
    return formatted_string.strip()


def decompose_query_rag(question, module_name, vectordb_path):
    """
    Decompose the query and retrieve the documents using the RAG model.
    Args:
        question: the input question.
        module_name: the module name you want the RAG to focus on.
        vectordb_path: the path to the vector database.
    Returns:

    """
    from langchain_openai import ChatOpenAI

    embedding_function = OpenAIEmbeddings()

    keyword = module_name
    vectorstore = Chroma(persist_directory=vectordb_path,
                         embedding_function=embedding_function, collection_name=keyword)

    retriever = vectorstore.as_retriever()

    # Multi Query: Different Perspectives
    template = """You are a helpful assistant that generates multiple sub-questions related to an input question. \n
    The goal is to break down the input into a set of sub-problems / sub-questions that can be answers in isolation. \n
    Generate multiple search queries related to: {question} \n
    Output (3 queries): """

    template = template

    prompt_decomposition = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI(temperature=0, model="gpt-4-turbo")

    generate_queries_decomposition = (prompt_decomposition | llm | StrOutputParser() | (lambda x: x.split("\n")))

    questions = generate_queries_decomposition.invoke({"question": question})

    # Prompt
    template = """Here is the question you need to answer:

    \n --- \n {question} \n --- \n

    Here is any available background question + answer pairs:

    \n --- \n {q_a_pairs} \n --- \n

    Here is additional context relevant to the question: 

    \n --- \n {context} \n --- \n

    Use the above context and any background question + answer pairs to answer the question: \n {question}
    """

    decomposition_prompt = ChatPromptTemplate.from_template(template)

    # llm
    llm = ChatOpenAI(model_name="gpt-4-turbo", temperature=0)

    q_a_pairs = ""
    for q in questions:
        rag_chain = (
                {"context": itemgetter("question") | retriever,
                 "question": itemgetter("question"),
                 "q_a_pairs": itemgetter("q_a_pairs")}
                | decomposition_prompt
                | llm
                | StrOutputParser())

        answer = rag_chain.invoke({"question": q, "q_a_pairs": q_a_pairs})
        q_a_pair = format_qa_pair_recursive(q, answer)
        q_a_pairs = q_a_pairs + "\n---\n" + q_a_pair

    template = """Here is a set of Q+A pairs:

    {context}

    Use these to synthesize an answer to the question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    final_rag_chain = (
            prompt
            | llm
            | StrOutputParser()
    )

    ans = final_rag_chain.invoke({"context": q_a_pairs, "question": question})

    return ans

def step_back_query_rag(question, module_name, vectordb_path):
    embedding_function = OpenAIEmbeddings()

    keyword = module_name

    vectorstore = Chroma(persist_directory=vectordb_path,
                         embedding_function=embedding_function, collection_name=keyword)

    retriever = vectorstore.as_retriever()

    examples = [
        {
            "input": "Could the members of The Police perform lawful arrests?",
            "output": "what can the members of The Police do?",
        },
        {
            "input": "Jan Sindel’s was born in what country?",
            "output": "what is Jan Sindel’s personal history?",
        },
    ]

    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            ("ai", "{output}"),
        ]
    )
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
        input_variables=["question"]
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert at world knowledge. Your task is to step back and paraphrase a question to a more generic step-back question, which is easier to answer. Here are a few examples:""",
            ),
            # Few shot examples
            few_shot_prompt,
            # New question
            ("user", "{question}"),
        ]
    )

    generate_queries_step_back = prompt | ChatOpenAI(temperature=0, model="gpt-4-turbo") | StrOutputParser()
    generate_queries_step_back.invoke({"question": question})

    # Response prompt
    response_prompt_template = """You are an expert of world knowledge. I am going to ask you a question. Your response should be comprehensive and not contradicted with the following context if they are relevant. Otherwise, ignore them if they are not relevant.

    # {normal_context}
    # {step_back_context}

    # Original Question: {question}
    # Answer:"""
    response_prompt = ChatPromptTemplate.from_template(response_prompt_template)

    chain = (
            {
                # Retrieve context using the normal question
                "normal_context": RunnableLambda(lambda x: x["question"]) | retriever,
                # Retrieve context using the step-back question
                "step_back_context": generate_queries_step_back | retriever,
                # Pass on the question
                "question": lambda x: x["question"],
            }
            | response_prompt
            | ChatOpenAI(temperature=0, model="gpt-4-turbo")
            | StrOutputParser()
    )

    ans = chain.invoke({"question": question})

    return ans