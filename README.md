<H1>⭐️ RAKSHISU APP</H1>

Rakshisu is a tool that identifies Personally Identifiable Information (PII) in uploaded documents and provides users with legal guidelines for handling PII, along with actionable recommendations on whether to mask the information or not.

<H2>USPs of Rakshisu:</H2>

1) <b>CSV Compatibility Selection</b>: Users can choose from 9 CSV file types via a dropdown menu
2) <b>Data Preview</b>: Clear presentation of uploaded data in a Pandas dataframe on the user interface
3) <b>Document Selection</b>: Dropdown menu for selecting Document No, If multiple entries share the same document number, users can select a row number from another dropdown menu.
4) <b>Document Details Display</b>: Display of selected document's titles/values, along with PII detection status ("PII Detected"/"PII Not Detected") using Azure AI services giving robust results.
5) <b>Guidelines for PII</b>: Gemini model displays ethical and legal reasons to help police officers in making a decision whether to mask or not mask the information identified as PII
6) <b>Action Menu</b>: Dropdown menu enabling users to choose "Yes" or "No" to mask or not mask detected PII values.
7) <b>PDF Generation</b>: Provides a downloadable PDF link containing sheet name, row number, and corresponding PII detected values (masked/not masked), along with their titles.
8) Our <b>Streamlit app</b> integrated with <b>Gemini Pro</b> is deployed on <b>Google Cloud Run</b>, which uses <b>Docker Container</b>. This makes our app <b>highly scalable</b> across different devices and systems.

<h2>Methodology:</h2>

1. The data from the original CSV is extracted and read using the <b>Pandas library in Python</b>.
2. The data is sent to <b>Azure AI services</b> for PII detection. The detection type and location are returned, and we map this response to our original input. This allows us to identify which keys are PII and set their mask value to true.
3. The PII type detected by Azure AI services is displayed on the UI of our <b>Streamlit app</b>, with options of Yes/No to mask the detected PII. When the police officer clicks "Yes," the information is masked and the PDF generated via the <b>FPDF library</b> can be downloaded from the UI
4. Utilizing <b>Gemini API in Google Cloud Vertex AI</b>, we explore the legal justification for implementing masking protocols.
