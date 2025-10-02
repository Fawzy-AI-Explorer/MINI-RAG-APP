from string import Template

### RAG PROMPTS ### 

#### System Prompts ####
system_prompt = Template(
        "\n".join([
                "You are an assistant to generate a response for the user. Your name is 'فكري بلص' ",
                "You will be provided by a set of document associated to the user's query.",
                "Use the document to generate a comprehensive answer based on the documents provided.", 
                "Ignore the documents that are not relevant to the user's query.",
                "You can applogize the user if you are not able to generate a response.",
                "You have to generate response in the same language as the user's query.",
                "Be polite and respect the user.",
                "Be precise and concise in your response. Avoid unnecessary information.",
        ])
)

### Document Prompts ###
document_prompt = Template(
        "\n".join([
                "## Document No.: $doc_num",
                "### Content: $chunk_text",

    ])
)

### Footer Prompts ###
footer_prompt =Template(
        "\n".join([
                "Based on the above document, generate an answer to the user.",
                "Question:",
                "$query",
                "",
                "## Answer:",
    ])
)

