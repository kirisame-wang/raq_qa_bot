import os

import runpod
import streamlit as st


runpod.api_key = os.getenv("API_KEY")
endpoint = runpod.Endpoint(os.getenv("ENDPOINT_ID"))
timeout = int(os.getenv("API_KEY", 60))

with st.sidebar:
    st.header("About")
    st.markdown(
        """
        This chatbot interfaces with a
        [LangChain](https://python.langchain.com/docs/get_started/introduction)
        agent designed to answer questions about the papers authored by 
        Amos Tversky and Daniel Kahneman on the topic of decision-making.
        The agent uses retrieval-augment generation (RAG) over unstructured 
        data that has been synthetically generated.
        """
    )

    st.header("Example Questions")
    st.markdown("- What is availability heuristic?")
    st.markdown("- What is representativeness heuristic?")
    st.markdown(
        """- How might reliance on the representativeness heuristic explain 
        why people tend to neglect base-rate frequencies?"""
    )
    st.markdown(
        """- Why might the availability heuristic lead individuals to 
        overestimate the frequency of events like traffic accidents 
        immediately after they witness one?"""
    )
    st.markdown(
        "- How can anchoring explain the overestimation of the probability of conjunctive events?"
    )
    st.markdown(
        """- Why might someone who believes in the gambler's fallacy predict that a coin is more 
        likely to land on tails after a series of consecutive heads?"""
    )
    st.markdown(
        """- How might the law of small numbers lead researchers to have an exaggerated belief 
        in the likelihood of successfully replicating an obtained finding?"""
    )
    st.markdown(
        """- What is a hypothetical example of a situation where conservatism might lead to an 
        inaccurate judgment or prediction?""")
    st.markdown(
        """- What are some ways that reliance on the illusion of validity could have negative 
        consequences for real-world decision-making?"""
    )
    st.markdown(
        """- How can regression to the mean be applied to explain why students' test scores 
        might improve after being punished for performing poorly on a previous test?""")
    st.markdown(
        """- Why is someone more likely to perceive an illusory correlation between memorable 
        or distinctive events?"""
    )
    st.markdown(
        """- What are the two main ways that probability distributions can be elicited, and why 
        might they yield different levels of calibration?"""
    )


st.title("RAG Bot")
st.info(
    """Ask me questions about the papers authored by 
    Amos Tversky and Daniel Kahneman on the topic of decision-making!"""
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "output" in message.keys():
            st.markdown(message["output"])

        # if "explanation" in message.keys():
        #     with st.status("How was this generated", state="complete"):
        #         st.info(message["explanation"])

if prompt := st.chat_input("What do you want to know?"):
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({"role": "user", "output": prompt})

    data = {"input": {"query": prompt}}

    with st.spinner("Searching for an answer..."):
        try:
            output_text = endpoint.run_sync(
                data,
                timeout=timeout,  # Timeout in seconds.
            )
        except TimeoutError:
            output_text = """An error occurred while processing your message.
            Please try again or rephrase your message."""

    st.chat_message("assistant").markdown(output_text)
    # st.status("How was this generated?", state="complete").info(explanation)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": output_text,
            # "explanation": explanation,
        }
    )
