---
title: Evaluations and Approval
---

## Purpose of Evaluations

Evaluating GenAi pipelines is key to making sure they generate reliable, high-quality responses. Without a solid evaluation process, it is hard to tell if changes—like tweaking prompts, removing LLMs, adjusting parameters, or refining retrieval steps—are actually improving performance or breaking something. By measuring factors like relevance, hallucination rates, and latency, teams can make informed decisions about how to optimize their pipelines. Integrating evaluations into CI/CD pipelines ensures that every update is tested, so performance stays consistent and issues are caught early.

The quality of an evaluation depends on having a well-rounded dataset and metrics. If test cases are too limited, models might appear to perform well but fail in real-world scenarios. A diverse dataset ensures that evaluation metrics truly reflect how the model will behave in production. At the end of the day, evaluations help build trust, keeping LLM applications accurate, scalable, and dependable across different use cases.

## Choosing the Right Evaluation Method

There are two main types of evaluators for assessing LLM performance: **automated evaluation** (using LLMs or code) and **human annotations**. Each method serves a different purpose depending on the type of assessment needed.

| Method                            | How it Works                                                                                        | Best For                                                                                                                                                       |
| --------------------------------- | --------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Automated (LLM or Code-Based)** | Uses an LLM to evaluate another LLM’s output or code to measure accuracy, performance, or behavior. | - Fast, scalable qualitative evaluation. <br> - Reducing cost and latency. <br> - Automating evaluations with hard-coded criteria (e.g., code generation).     |
| **Human Annotations**             | Experts manually review and label LLM outputs.                                                      | - Evaluating automated evaluation methods. <br> - Applying subject matter expertise for nuanced assessments. <br> - Providing real-world application feedback. |

Automated evaluation is efficient for objective assessments and large-scale testing, while human annotations provide deeper insights at a higher cost. Combining both methods can ensure a balanced and reliable evaluation process.

## GenAi Evaluation Framework

Gen AI pipelines can introduce significant risks, making a robust evaluation framework essential for comprehensive testing and validation. Follow these structured steps to ensure effective evaluation:

| Step                                         | Description                                                                                                                                                                                  |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Identify Risks & Define Evaluation Scope** | - Assess potential risks across the pipeline. <br> - Create a comprehensive list of necessary evaluations.                                                                                   |
| **Define Evaluation Metrics**                | - Align metrics with business objectives, MRM, and FL requirements. <br> - Implement custom metrics as needed. <br> - Use GGX evaluation reports curated by GenAI and risk experts.          |
| **Prepare Evaluation Datasets**              | - Ensure datasets accurately represent the use case. <br> - Cover all critical business scenarios for thorough validation. <br> - Utilize GGX datasets curated by experts to evaluate risks. |
| **Run Evaluations**                          | - Use standard/custom reports and dashboards for structured testing. <br> - Interpret evaluation results to refine and enhance the pipeline.                                                 |
| **Compare with Challengers**                 | - Establish alternative components and pipelines for comparison.                                                                                                                             |

By following these steps, teams can systematically evaluate their Gen AI pipelines, mitigate risks, and enhance performance with data-driven insights.  
Corridor provides the ability to **Run Evaluation Jobs** for registered GenAi components.

## Introduction to Jobs

Corridor provides the ability to perform evaluations by running jobs on the registered objects and generating standardised and customized reports/metrics. Evaluations are controlled by Corridor - and run in a dedicated locked environment to ensure reproducibility of results.

The platform supports batch evaluation of objects through **simulation jobs** or **comparisons with similar objects** on given datasets. Reports and metrics for these evaluations can be customized within Corridor under **Resources → Reports Section**. For more details, refer to the [Reporting](./reporting.md) section.

Once the job is completed, Corridor records all the details about specific steps of the jobs, logs resource usages and publishes the dashboard containing all the selected reports which can be shared across the team on Corridor for feedback and approval process. The results can be exported outside Corridor or used for automated documentation.

## Approvals post Evaluations

The approval process is a key governance capability of the platform. After the object is fully evaluated using automated dashboard or manual tests, all the evaluation results can be shared with predefined roles within an Approval Workflow, ensuring structured reviews, feedback, and approvals for production use.

Once approved, the object is locked, preventing any modifications within the system. This guarantees the artifact remains unchanged before being exported directly to the production system.

## Standardized GGX Reports

Apart from the ability to create customized reports, Corridor already has a battery of tests registered for evaluation and validation of different components of Corridor. GGX Reports are crafted by a team of generative AI risk experts following thorough research and analysis. The list of reports is expanding with all the latest developments in the GenAi Industry. All these reports can be used if applicable and can be maintained or forked for a specific use case.

| **Component** | **Test Name**                      | **Risk Attribute**                               | **Description**                                                                                                                                              | **Type**           | **Classification** | **Response** |
| ------------- | ---------------------------------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------ | ------------------ | ------------ |
| **Pipeline**  | Accuracy                           | Inaccurate Classification or Response            | Evaluate ability to correctly classify utterances or provide accurate responses to user queries.                                                             | MRM                | Yes                | Yes          |
| **Pipeline**  | Stability Repeated Utterances      | Output Variability                               | Evaluate the ability to produce the same classification or nearly similar responses for repetitions of the same utterance.                                   | MRM                | Yes                | Yes          |
| **Pipeline**  | Stability Perturbed Utterances     | Output Variability                               | Evaluate the ability to produce the same classification or similar responses across minor variations of an utterance (e.g., synonyms, grammatical mistakes). | MRM                | Yes                | Yes          |
| **Pipeline**  | Bias (Comparative Prompt Analysis) | Implicit / Explicit Bias                         | Evaluate bias in outputs (e.g., classification accuracy or response accuracy) based on inferred segments for gender, race, and age.                          | Fair Lending       | Yes                | Yes          |
| **Pipeline**  | Vulnerability                      | Prompt Injection & Prompt Leakage                | Evaluate the LLM pipeline’s resilience against jailbreak methods for out-of-context or ambiguous inputs.                                                     | MRM / Fair Lending | No                 | Yes          |
| **Pipeline**  | Toxicity                           | Hate Speech, Toxic Language, Sarcasm             | Evaluate the LLM’s avoidance of generating or repeating toxic language (e.g., inappropriate, offensive, or harmful language).                                | MRM / Fair Lending | No                 | Yes          |
| **Pipeline**  | Faithfulness                       | Hallucination, Inaccurate Facts                  | Evaluate adherence to provided context without hallucination.                                                                                                | MRM / Fair Lending | No                 | Yes          |
| **Prompt**    | Prompt Trust Score                 | Prompt Quality, Prompt Vulnerability and Leakage | Evaluate the prompt quality in different dimensions like Grammar, Logical Coherence, Toxicity, Bias, etc., and generate a Trust Score.                       | MRM / Fair Lending | N/A                | N/A          |
| **Prompt**    | Prompt Classification Accuracy     | Inaccurate Classification                        | Evaluate the classification accuracy of the prompt on sample data to help in the hill-climbing process.                                                      | MRM / Fair Lending | Yes                | No           |
| **LLM**       | Vocabulary Understanding           | Misinterpretation, Lack of Context Awareness     | Determine which LLM is best at defining financial services-specific terminology across seven context categories.                                             | MRM / Fair Lending | N/A                | N/A          |
| **LLM**       | Subject Understanding              | Context Misalignment, Incorrect Reasoning        | General subject understanding across Math, Science, etc.                                                                                                     | MRM / Fair Lending | N/A                | N/A          |
| **LLM**       | Reasoning Capability               | Logical Fallacies, Incorrect Inferences          | Assess LLM's capabilities such as complex reasoning, knowledge utilization, language generation, etc.                                                        | MRM / Fair Lending | N/A                | N/A          |
| **LLM**       | Toxicity Understanding             | Failure to Detect Harmful Requests               | Evaluate a model's ability to identify and classify text statements that could be considered toxic across six toxicity labels.                               | MRM / Fair Lending | N/A                | N/A          |
| **LLM**       | Toxicity Evaluation                | Hate Speech, Toxic Language, Sarcasm             | Evaluating the tendency of LLM generating toxic replies.                                                                                                     | MRM / Fair Lending | N/A                | N/A          |
| **LLM**       | Dialect Bias                       | Underrepresentation of Linguistic Variants       | Assess which LLM responds most consistently to general queries phrased in different language dialects.                                                       | MRM / Fair Lending | N/A                | N/A          |
| **LLM**       | Gender Bias with Income as Proxy   | Fair Lending Risk                                | Evaluation focuses on understanding if there is any systematic bias in assigning job titles to different genders and profiles.                               | MRM / Fair Lending | N/A                | N/A          |
| **LLM**       | Model Latency                      | Scalability Issues, User Frustration             | Determine which LLM has the best response latency performance when varying prompt and response length.                                                       | Business / Tech    | N/A                | N/A          |
| **RAG**       | Retrieval Accuracy                 | Incorrect context retrieval, hallucination       | Accuracy of the retrieved documents by the RAG system.                                                                                                       | MRM                | N/A                | N/A          |
| **RAG**       | Knowledge Evaluation               | Lack of Coverage                                 | Coverage of different scenarios and business flows in Knowledge Data.                                                                                        | Business           | N/A                | N/A          |
| **RAG**       | Validation Data Evaluation         | Lack of Coverage, Lack of Potential Scenarios    | Coverage of different scenarios and business flows in Evaluation Data.                                                                                       | MRM                | N/A                | N/A          |
