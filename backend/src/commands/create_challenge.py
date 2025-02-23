from mediator import MediatorDTO, mediator
from models.enums import ChallengeCategory, ChallengeDifficulty
from models.entities import Challenge, ChallengeFile
from database.mongo import engine
from typing import Optional
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, ConfigDict, Field
from settings import global_settings
from odmantic import ObjectId
from langchain_core.prompts import PromptTemplate

class CreateChallengeCommand(MediatorDTO):
  category: ChallengeCategory
  difficulty: ChallengeDifficulty
  additional_prompt: Optional[str] = None

class CreateChallengeResponse(MediatorDTO):
  challenge: Challenge

class ChallengeOuptut(BaseModel):
  model_config = ConfigDict(arbitrary_types_allowed=True)

  title: str
  setup_instructions: str = Field(description="List of instructions for the user to setup the challenge on their environment. This will be stored in an README.md file")
  description: str = Field(description="A short one to two sentence description of the challenge")
  flag_solution: str = Field(description="The solution to the challenge")
  files: list[ChallengeFile]


@mediator.register_handler(CreateChallengeCommand)
async def create_challenge(command: CreateChallengeCommand) -> CreateChallengeResponse:
  outline = await create_challenge_outline(command)
  output = await create_challenge_output(outline)

  challenge = Challenge(
    id=ObjectId(),
    category=command.category,
    difficulty=command.difficulty,
    title=output.title,
    setup_instructions=output.setup_instructions,
    description=output.description,
    flag_solution=output.flag_solution,
    files=output.files
  )

  await engine.save(challenge)

  return CreateChallengeResponse(challenge=challenge)

async def create_challenge_outline(command: CreateChallengeCommand) -> str:
  """
  Create a challenge outline for a given challenge category and difficulty.

  Args:
    command: CreateChallengeCommand

  Returns:
    str
  """

  model = ChatOpenAI(model="o3-mini-2025-01-31", api_key=global_settings.OPENAI_API_KEY, max_completion_tokens=4096)
  prompt = PromptTemplate.from_template("""
    You are an Instant CTF Agent Generator responsible for creating a custom outline for a CTF challenge. Your output is a structured outline that will later be used to generate the final output files (challenge instructions and setup instructions). This outline must clearly determine:
1. What kind of challenge within the given category should be developed.
2. What code components and technical steps are needed to implement this challenge.

User Request Details:
- Category: {category}
    *Example values: "Web Exploitation", "Reverse Engineering", "SQL Injection"*
- Difficulty: {difficulty}
    *Example values: "Easy", "Medium", "Hard", "Impossible"*
- Additional Information (Optional): {additional_prompt}
    *This field may contain extra guidelines or specific elements to incorporate.*

Instructions:
1. **Outline Creation:**  
   Based on the provided `[challenge_category]`, `[difficulty_level]`, and optional `[additional_info]`, generate a comprehensive outline that includes:
   - A clear description of the specific type of challenge to be developed. Explain why this challenge fits the selected category and difficulty.
   - A detailed list or explanation of the code components, scripts, frameworks, and configurations needed to build the challenge.
   
2. **Jurassic World Theme:**  
   Infuse the outline with language and design cues inspired by Jurassic World. Your challenge description and technical implementation should evoke prehistoric landscapes, dinosaur motifs, and adventurous exploration—imagine challenges set within a digital dinosaur park where every vulnerability is another wild creature to outsmart.

3. **Preparation for Output Files:**  
   Remember that the outline you generate will be used to create:
   - **Challenge Instructions:** A detailed description of the challenge that guides the user.
   - **Setup Instructions:** Clear, step-by-step instructions on how to deploy and interact with the challenge.
   Your outline must be actionable, logically organized, and serve as a robust blueprint for both.

4. **Clarity and Detail:**  
   Structure your outline using headers and bullet points as needed. Clearly separate the challenge description from the technical/code requirements. Provide as much detail as possible to ensure the next generation step has all the information required to build and verify the challenge.

----------------------------------------
Example Structure:
----------------------------------------
Title: Jurassic CTF Challenge Outline

I. Challenge Description
   - Detailed explanation of the challenge type, how it fits within `[challenge_category]`, and why it is appropriate for a `[difficulty_level]` challenge.
   - Integration of any extra details from `[additional_info]`.
   - Immersive, thematic language that evokes a Jurassic World setting. For example: “Imagine a digital landscape where every click takes you deeper into a forgotten park filled with ancient secrets and lurking dangers…”
   
II. Technical Implementation
   - A thorough list of code components, libraries, frameworks, scripts, and configurations required.
   - An explanation of how these technical elements combine to deliver the challenge. Include any specific instructions that might help with debugging or iterative testing.
   
III. Additional Considerations
   - Any extra guidelines or creative directions based on `[additional_info]`.
   - Suggestions for potential pitfalls or hints for users that align with the Jurassic theme.

----------------------------------------
Detailed Examples:
----------------------------------------

**A. Web Exploitation Examples (PicoCTF–style):**

1. *Easy – “Jurassic Safari’s Secret”*  
   - **Challenge Description:**  
     In this introductory challenge, users encounter a seemingly simple dinosaur-themed webpage. The page contains hidden HTML comments and a poorly secured source code. The challenge is to inspect the webpage’s source code to find a hidden string resembling a flag.  
   - **What the User Must Do:**  
     The user is expected to open the browser’s developer tools, inspect the page’s HTML, and discover a commented section with a flag (e.g., `FLAG...`). Detailed hints may point to checking the `<head>` or `<footer>` for any “secret” code.  
   - **Technical Implementation:**  
     The outline should include instructions for creating a static webpage with embedded comments, ensuring the flag is visible only in the source code, and integrating a Jurassic background image and dinosaur icons.

2. *Medium – “Raptor’s Roost Vulnerability”*  
   - **Challenge Description:**  
     This challenge raises the stakes by presenting a web application that is vulnerable to reflected Cross-Site Scripting (XSS). The page, styled as a raptor observation log, accepts user input and echoes it back unsanitized.  
   - **What the User Must Do:**  
     The user must discover the vulnerability by inputting malicious scripts into a search field, triggering the execution of JavaScript that reveals a hidden flag. They are expected to use browser developer tools and a basic understanding of XSS to craft a payload that exposes the flag (e.g., `FLAG...`).  
   - **Technical Implementation:**  
     The outline should detail the setup of a simple web server (using Flask or Node.js) with an input field, deliberately omitting sanitization. It should also specify how to integrate Jurassic-themed elements such as fossilized logs and raptor silhouettes.

3. *Hard – “Dilophosaurus Denial”*  
   - **Challenge Description:**  
     In this challenge, users face a more complex web application where a combination of URL manipulation and hidden parameters lead to a sensitive endpoint. The site, designed as a digital replica of a dinosaur research facility, hides its flag behind a misconfigured access control.  
   - **What the User Must Do:**  
     The challenge requires the user to manipulate URL parameters, analyze network traffic using tools like Burp Suite, and piece together clues from server responses. The flag may be split across multiple responses (e.g., `FLAG...` in one response and `phosaurus` in another), requiring the user to combine these pieces correctly.  
   - **Technical Implementation:**  
     Outline the code components for the vulnerable endpoint, including instructions for setting up routing and session handling. Detail how the misconfiguration (such as improper validation of session tokens) is embedded intentionally and provide guidelines for integrating detailed Jurassic UI elements like lab environments and digital fossils.

4. *Impossible – “Tyrannosaurus Terminal Takeover”*  
   - **Challenge Description:**  
     The ultimate web exploitation challenge involves a multi-layered vulnerability chain. In this scenario, the user navigates a complex dinosaur park management system that is protected by advanced security measures. The challenge combines SQL injection, file inclusion, and cross-site scripting, all hidden within a futuristic Jurassic World interface.  
   - **What the User Must Do:**  
     The user must identify the chain of vulnerabilities, starting with an obfuscated parameter that leads to a SQL injection, then leverage the data retrieved to execute a file inclusion attack that eventually reveals a heavily encoded flag. This flag might be spread across multiple modules and require decoding.  
   - **Technical Implementation:**  
     The outline should specify a modular code structure where each vulnerability is isolated but interconnected. Include detailed instructions on how to simulate secure coding practices with intentional flaws and how to design a rich, cinematic Jurassic interface that includes elements like interactive maps of a dinosaur park and advanced error logging.

**B. Reverse Engineering Examples:**

1. *Easy – “Dino Egg Decoder”*  
   - **Challenge Description:**  
     This challenge features a small binary (or obfuscated script) that, when executed, prints a scrambled message. Set in a Jurassic laboratory, the task is to decode a reversed string to reveal the flag.  
   - **What the User Must Do:**  
     The user should use tools such as the `strings` command or a simple disassembler to extract the hidden flag (e.g., `FLAG...`) from the binary’s output.  
   - **Technical Implementation:**  
     The outline should include instructions to compile a simple C program or package a Python script that intentionally reverses a known string. Ensure the code includes dinosaur-themed comments and imagery in its output.

2. *Medium – “Triceratops Lock”*  
   - **Challenge Description:**  
     Here, a binary mimics a digital lock system for a dinosaur enclosure. The program checks for a specific input password using a hard-coded algorithm.  
   - **What the User Must Do:**  
     The user must analyze the binary with tools like Ghidra or IDA Pro to understand the password-checking algorithm. Once they deduce the logic, they must determine the correct password (e.g., `FLAG...`) to unlock the “dino gate.”  
   - **Technical Implementation:**  
     Outline the process for creating a binary that uses a simple, custom algorithm for password verification. Include comments in the code referencing dinosaur traits (e.g., “as sturdy as a triceratops”) and instructions for debugging.

3. *Hard – “Velociraptor Vault”*  
   - **Challenge Description:**  
     This challenge presents a heavily obfuscated binary designed to simulate a secure vault inside a velociraptor habitat. The binary employs anti-debugging techniques and encrypted routines.  
   - **What the User Must Do:**  
     The user must perform both static and dynamic analysis to bypass anti-debugging measures, decrypt critical routines, and ultimately extract the flag (e.g., `FLAG...`).  
   - **Technical Implementation:**  
     Provide a detailed list of technical steps including the use of debuggers, runtime analysis, and deobfuscation techniques. The outline should mention the integration of Jurassic elements by including dinosaur roar sound effects or graphics in the UI when certain conditions are met.

4. *Impossible – “Mosasaurus Matrix”*  
   - **Challenge Description:**  
     The most challenging reverse engineering task, this binary is deliberately engineered to be nearly impenetrable. Featuring virtualization or heavy obfuscation techniques, it simulates the complexity of a Mesolithic predator’s behavior.  
   - **What the User Must Do:**  
     The user must combine advanced disassembly, dynamic analysis, and creative problem-solving to understand a layered virtual machine or obfuscated control flow, and then reconstruct the logic to extract the flag (e.g., `FLAG...`).  
   - **Technical Implementation:**  
     The outline should detail an advanced build process that employs multiple layers of obfuscation, anti-tampering checks, and custom encryption routines. Emphasize the need for an in-depth guide on debugging and overcoming virtualized code, with the interface featuring high-detail Jurassic-themed graphics and animations.

**C. SQL Injection Examples:**

1. *Easy – “Jurassic Login”*  
   - **Challenge Description:**  
     In this basic challenge, users encounter a login page for a dinosaur park management system. The login form is vulnerable to a simple SQL injection where a classic payload (e.g., `1' OR '1'='1`) bypasses authentication.  
   - **What the User Must Do:**  
     The user must identify the injection point, craft the correct payload, and log in to reveal a hidden page that contains the flag (e.g., `FLAG...`).  
   - **Technical Implementation:**  
     The outline should include instructions for creating a basic web form with SQL query vulnerabilities, along with tips for integrating a Jurassic-themed login page complete with park maps and dinosaur silhouettes.

2. *Medium – “Fossilized Database”*  
   - **Challenge Description:**  
     This challenge simulates a scenario where users must extract data from a dinosaur fossil database. The SQL injection vulnerability is not immediately apparent and requires union-based injection to enumerate the database schema.  
   - **What the User Must Do:**  
     The user must perform a union-based SQL injection to list table names and column data, then piece together fragmented data that form the flag (e.g., `FLAG...`).  
   - **Technical Implementation:**  
     Provide detailed steps for setting up a database with multiple tables and intentional injection points. The outline should emphasize clear instructions on how to use union queries, and reference Jurassic-themed data (e.g., fossil records, excavation logs).

3. *Hard – “Prehistoric Pulse”*  
   - **Challenge Description:**  
     In this scenario, the SQL injection vulnerability is hidden behind a time-based blind SQL injection mechanism. The challenge is set in a prehistoric data center where timing differences are the only clue.  
   - **What the User Must Do:**  
     The user must use time delays in SQL queries to extract information one bit at a time. They must infer the flag (e.g., `FLAG...`) by analyzing the response delays and reconstructing the hidden string.  
   - **Technical Implementation:**  
     The outline should detail how to create a backend with blind SQL injection vulnerabilities, including instructions for simulating time delays. It should also incorporate Jurassic aesthetics—such as an interface resembling an ancient, crumbling data archive.

4. *Impossible – “Cretaceous Conundrum”*  
   - **Challenge Description:**  
     The ultimate SQL injection challenge combines multiple advanced techniques. The vulnerable application employs out-of-band injection and second-order SQL injection methods. The flag is obfuscated in a multi-step process within an intricately designed dinosaur research database.  
   - **What the User Must Do:**  
     The user must identify the initial injection point, exploit out-of-band channels to retrieve intermediate data, and then perform a second-order injection to reveal the final, encrypted flag (e.g., `FLAG...`). This challenge requires a deep understanding of database behavior and advanced SQL injection techniques.  
   - **Technical Implementation:**  
     The outline should include a comprehensive list of the necessary SQL commands, the design of a multi-layered database schema, and instructions for simulating out-of-band communication. Emphasize integration with a Jurassic-themed dashboard, complete with interactive dinosaur exhibit panels and animated prehistoric graphics.

----------------------------------------
Your goal is to produce an outline that is creative, technically detailed, and immersive. Each section of your outline must:
- Incorporate the user’s selected `[challenge_category]` and `[difficulty_level]`.
- Leverage additional context from `[additional_info]` when provided.
- Clearly delineate between the narrative (challenge description) and the technical blueprint (implementation steps).
- Reflect a rich, Jurassic World–themed experience throughout every element.

By following this template and including these detailed examples, you will provide a robust blueprint that guides subsequent steps in generating fully functional CTF output files—challenge instructions and setup instructions—and ultimately deliver an engaging, multi-modal, and thematic CTF challenge experience.""")

  prompt = PromptTemplate.from_template("""
OVERVIEW: You are an Instant CTF Agent Generator. Your sole task is to produce a fully detailed and explicit outline for a custom CTF challenge. This outline will be used as the definitive blueprint to generate two sets of output files: Challenge Instructions – a document explaining the challenge narrative and step-by-step tasks for the user, and Setup Instructions – a guide describing every step required to configure, deploy, and test the challenge environment. Every element must be fully explained with no assumption of prior knowledge. Every instruction, step, component, and rationale is included so that each directive can be executed without ambiguity.

USER INPUT PARAMETERS:
Category: {category}
Difficulty: {difficulty}
Additional Information: {additional_prompt}

Challenge Category: Acceptable values are Web Exploitation, Reverse Engineering, or SQL Injection. This parameter determines the type of vulnerability or challenge approach. If the challenge category is Web Exploitation, then all narrative and technical details must focus on vulnerabilities in web applications. If it is Reverse Engineering, the focus is on binary analysis and disassembly. If it is SQL Injection, the details must center on database query vulnerabilities.
Difficulty Level: Acceptable values are Easy, Medium, Hard, or Impossible. This parameter influences every element of the challenge. "Easy" challenges require simple vulnerabilities, clear hints, and minimal technical complexity. "Medium" challenges require a moderate level of technical analysis and more intermediate steps. "Hard" challenges involve multiple stages of reasoning and several layers of vulnerabilities. "Impossible" challenges incorporate advanced techniques, multi-step exploitation chains, and may involve several combined vulnerabilities.
Additional Information (Optional): This field can contain any extra instructions, specific requirements, or creative guidelines. Every word in the additional information must be integrated verbatim into the outline wherever it is relevant.
THEMES AND TONE: All output must be immersed in a Jurassic World theme. Use explicit language that references dinosaurs, prehistoric landscapes, and Jurassic environments. Every technical component and narrative must incorporate elements such as dinosaur park, prehistoric secrets, fossilized data, and raptor tactics. All aesthetic design details like background images, fonts, and icons must mimic Jurassic elements. For instance, if specifying CSS details, include instructions such as "use a background image of a dense jungle-like dinosaur park" or "set fonts to mimic ancient, weathered stone inscriptions."

INSTRUCTIONS TO GENERATE THE OUTLINE: The generated outline must be divided into the following main sections, with exhaustive details and explicit instructions:

I. CHALLENGE DESCRIPTION A. Overview: Explain in complete detail what type of challenge is being developed based on the challenge category. For example, state: "This challenge presents a hidden vulnerability in a dinosaur-themed web page" if the category is Web Exploitation. Clearly justify why the challenge is classified as Easy, Medium, Hard, or Impossible by including the technical complexity (such as multiple vulnerability layers or obfuscation techniques) and the expected level of expertise. Explicitly state how prehistoric and dinosaur elements are woven into the narrative. Include a detailed checklist that introduces the scenario, explains the environment (for example, a digital dinosaur park), states the goal (for example, find a hidden flag), and mentions any background story or setting details.

B. Detailed Narrative: Provide a step-by-step description of the user journey from start to finish. Explain exactly what the user will experience and every action they must perform. For example, if the challenge involves inspecting a webpage's source code, instruct: "Right-click on the webpage, select 'Inspect', then scroll to the footer section." Provide minute details about which tool to use (for example, browser developer tools available in Chrome or Firefox), where to click, what to look for, and what output to expect.

C. PicoCTF-Inspired Examples: For each challenge category and difficulty level, include a fully detailed example that contains:

Title: A concise, Jurassic-themed title.
Narrative Description: A comprehensive narrative that explains the setting, user role, and goal. Describe the environment in detail (for example, "Imagine you are in a high-security dinosaur park control room") and the challenge objective.
User Tasks: List every step the user must follow, including which tools to use (for example, "open developer tools" or "run the command strings filename"), the expected intermediate outputs (for example, a pop-up alert showing FLAG_dino_found), and the exact locations where information is hidden (for example, "in the HTML comment of the footer").
Flag Format: Specify the flag using underscores. For example, use FLAG_dino_found, FLAG_raptor_script, FLAG_dilo_phosaurus, FLAG_tyra_part1 (and similar) instead of curly brackets.
Every example must be complete and cover every detail from navigation to exploitation.

II. TECHNICAL IMPLEMENTATION A. Code Components: List every file and component required. Specify file names, programming languages, frameworks, libraries, and exact code segments where necessary. For example, "Create an index.html file for the web page, a styles.css file for styling, and a script.js file for dynamic behavior." Explain the purpose of each code block and state where to insert dinosaur-themed comments (for example, "Begin dinosaur park initialization"). Provide explicit instructions for embedding the flag, such as "Insert the string FLAG_dino_found inside an HTML comment in the footer section."

B. Technical Steps: Provide a step-by-step process, starting with initializing the project structure by listing directories and files exactly. Describe writing boilerplate code including HTML, CSS, JavaScript, or backend language specifics. Explain how to configure the server or environment by specifying commands (for example, "Run 'python -m http.server 8000' for a basic Python server") and list all dependencies and installation steps. Instruct how to insert deliberate vulnerabilities, such as unsanitized user input for web challenges, compilation instructions using gcc for binary challenges, or details of SQL query strings with injection flaws for SQL challenges. Include a detailed testing and debugging checklist, explaining how to use tools like Burp Suite, Ghidra, or SQL injection testing tools and state the expected results at each step.

C. Integration of Jurassic Theme: List specific assets to be included, such as dinosaur_park_background.jpg, raptor_icon.png, or prehistoric_font.ttf. Explain in detail how to apply the theme using CSS instructions like "Set the body background to the dinosaur park image, ensure the font is styled with a prehistoric appearance, and use a color palette inspired by earthy tones." Specify where to place these assets in the file structure and include multimedia enhancements if sound effects are used, with file names and trigger conditions (for example, "Play dino_roar.mp3 when the user submits the form").

III. ADDITIONAL CONSIDERATIONS A. Extra Guidelines: Detail how to integrate every word from the additional information into both the narrative and technical sections. For example, if the additional information includes "time limit", then add a countdown timer feature with Jurassic-themed animations. List every potential error the user might encounter and provide explicit hints for each step (for example, "If the flag does not appear, double-check the footer section in the HTML source").

B. Verification Steps: Provide a step-by-step verification process. Explain how to simulate user interaction using explicit test cases with commands and expected outputs. Describe how to verify that each code component is functioning, for example by instructing "Access http://localhost:8000 and verify the page loads with the dinosaur background" for web applications or "Run the binary and confirm that the output is scrambled as described" for binary challenges. Include detailed debugging checklists with expected logs and outputs.

C. User Guidance: Write a complete user manual that explains every tool to install and where to obtain them, how to access developer tools, and how to use disassemblers or SQL injection tools with explicit command examples. Include troubleshooting steps for common issues and explain every piece of technical jargon in simple terms so that no step is left ambiguous.

DETAILED EXAMPLES PER CATEGORY AND DIFFICULTY

A. WEB EXPLOITATION EXAMPLES

Easy – "Jurassic Safari’s Secret" CHALLENGE DESCRIPTION: Title: Jurassic Safari’s Secret Narrative: The user is presented with a static, dinosaur-themed webpage titled "Jurassic Safari’s Secret" that displays a lush, prehistoric jungle background. Hidden within the HTML source code in the footer is an HTML comment that contains the flag. User Instructions: Step 1: Open the webpage in a modern browser such as Chrome or Firefox. Step 2: Right-click on the webpage and select "Inspect" or "View Page Source." Step 3: Scroll to the footer section in the HTML. Step 4: Identify the HTML comment that contains the string formatted as FLAG_dino_found. Step 5: Record the flag exactly as it appears. TECHNICAL IMPLEMENTATION: Components: File: index.html containing standard HTML5 boilerplate code, a head section with a link to an external CSS file named styles.css, and a body with a dinosaur-themed header and footer. File: styles.css that specifies a background image URL such as "images/dinosaur_park.jpg" and defines prehistoric fonts and color palettes. HTML Comment: In the footer section, include an HTML comment that reads: Optional JavaScript: A small script file, script.js, to ensure dynamic loading of images if necessary. Step-by-Step:

Create index.html with the standard HTML tags including html, head, and body.
In the head, link to styles.css using a link tag.
In index.html, inside the footer, insert the HTML comment:
Test by opening index.html in a browser, then inspect the source to verify the comment is visible. JURASSIC THEME: Design Elements: Use prehistoric fonts, earthy color palettes, dinosaur icons, and subtle animations that mimic a natural environment. The narrative should repeatedly reference exploring an ancient digital jungle.
Medium – "Raptor’s Roost Vulnerability" CHALLENGE DESCRIPTION: Title: Raptor’s Roost Vulnerability Narrative: The webpage is styled as a raptor observation log for a dinosaur sanctuary. It features a search input field that directly echoes user input into the page without sanitization. The flag is embedded within a JavaScript alert that is triggered if a malicious payload is injected. User Instructions: Step 1: Navigate to the Raptor’s Roost page. Step 2: Locate the search input field. Step 3: Type the following payload exactly: alert('FLAG_raptor_script') Step 4: Submit the form. Step 5: Observe that an alert box pops up displaying the flag. TECHNICAL IMPLEMENTATION: Components: Backend: Use a simple web server built with Flask in Python or Node.js. Endpoint: /search that accepts GET or POST requests. HTML File: Contains a search form with an input field and a submit button. Server Code: Directly echoes the unsanitized user input back into the HTML response. CSS/Design: Jurassic-themed styling with fossil textures and raptor icons. Step-by-Step:

Set up a basic Flask application with an endpoint /search.
Develop an HTML form that sends a parameter named query to the /search endpoint.
In the backend, output the user input directly into the HTML response.
Integrate Jurassic-themed CSS in the HTML template.
Run the Flask app and test the payload in a web browser. JURASSIC THEME: Design Elements: Include a header image of a raptor silhouette, rugged fossil-inspired textures, and narrative text such as "Unleash your inner raptor and hunt for secrets."
Hard – "Dilophosaurus Denial" CHALLENGE DESCRIPTION: Title: Dilophosaurus Denial Narrative: The challenge is set in a digital replica of a dinosaur research facility. Multiple endpoints expose different fragments of a hidden flag. The flag is split across various responses, requiring manipulation of URL parameters to piece together the final answer. User Instructions: Step 1: Visit the primary endpoint, for example, /info. Step 2: Observe that the page returns partial data with obfuscated URL parameters. Step 3: Use a network analysis tool such as Burp Suite to capture HTTP requests and responses. Step 4: Manipulate the URL parameters by adding query strings such as token=raptorKey to reveal hidden fragments. Step 5: Collect each fragment (for example, FLAG_dilo and FLAG_phosaurus) and concatenate them in the correct order. TECHNICAL IMPLEMENTATION: Components: Backend: Use a Flask or Node.js server with multiple endpoints such as /info, /data, and /flag. Each endpoint returns a specific fragment of the flag based on secret URL parameters. Code: Implement session handling with intentional misconfigurations and include conditional statements that check for precise parameter values. HTML/CSS: Build a front-end interface that simulates a high-tech research lab with dinosaur-themed graphics. Step-by-Step:

Create endpoints in the server code: /info returns basic information with hidden parameter instructions; /data returns part of the flag if the correct parameter is detected; /flag returns the remaining fragment.
Write explicit conditions in the server code to check for the parameter value, for example, if the token equals raptorKey.
Embed detailed debugging logs (for internal testing) explaining the expected parameter values.
Build the front-end with Jurassic-themed images such as laboratory fossils and digital dinosaur skeletons.
Test the entire chain by simulating HTTP requests and verifying each fragment is returned. JURASSIC THEME: Design Elements: Use imagery such as a digital lab with dinosaur bone charts, aged parchment color schemes, and narrative text like "unlock the ancient secrets of the Dilophosaurus."
Impossible – "Tyrannosaurus Terminal Takeover" CHALLENGE DESCRIPTION: Title: Tyrannosaurus Terminal Takeover Narrative: This is the most advanced web exploitation challenge. The system is a multi-layered dinosaur park management platform with a cascade of vulnerabilities including SQL injection, file inclusion, and cross-site scripting (XSS). The flag is deliberately fragmented across various modules and requires the user to exploit each vulnerability in sequence. User Instructions: Step 1: Identify the SQL injection vulnerability in a specific URL parameter. Step 2: Exploit the SQL injection to retrieve a list of files or data pointers. Step 3: Use the retrieved data to perform a file inclusion attack on another endpoint. Step 4: Finally, trigger an XSS vulnerability that decodes the obfuscated flag segments. Step 5: Collect all fragments (for example, FLAG_tyra_part1, FLAG_tyra_part2, FLAG_tyra_part3) and concatenate them to reveal the final flag. TECHNICAL IMPLEMENTATION: Components: Backend: Use a modular codebase with a framework such as Node.js with Express, where each module simulates one vulnerability. Database: Design a multi-table schema with interlinked data where one or more tables contain parts of the flag. Code: Provide detailed SQL queries with intentional injection points, file inclusion code that dynamically loads file contents based on input, and XSS payload injection code. Frontend: Develop a dashboard that displays dinosaur park management elements like interactive maps and security logs. Step-by-Step:

Design the database schema with at least three interrelated tables.
Write the Node.js backend code with separate modules: Module A implements the SQL injection vulnerability with explicit SQL query strings. Module B uses the output from Module A to allow file inclusion, documenting the expected file paths such as ./data/tyranno.txt. Module C contains the XSS vulnerability with a detailed JavaScript snippet to decode the flag.
Insert detailed, step-by-step comments in the code explaining each vulnerability and expected inputs/outputs.
Build the front-end dashboard integrating Jurassic-themed assets such as animated dinosaur icons and interactive maps.
Test the entire chain by simulating a multi-step exploitation process and verifying that the final concatenated flag is correct. JURASSIC THEME: Design Elements: The user interface should mimic a high-security dinosaur park control room with error messages styled as "dinosaur warnings." Use cinematic visual effects representing a takeover by prehistoric forces, and narrative text emphasizing the intricate nature of unlocking ancient secrets.
B. REVERSE ENGINEERING EXAMPLES

Easy – "Dino Egg Decoder" CHALLENGE DESCRIPTION: Title: Dino Egg Decoder Narrative: The challenge involves a small executable binary or obfuscated script. When executed, the program outputs a scrambled or reversed string. The setting is a Jurassic laboratory where dinosaur eggs contain secret messages. User Instructions: Step 1: Download and execute the binary or script from a secure location. Step 2: Use a command-line tool (for example, run the command strings filename in a terminal) to extract all human-readable text. Step 3: Identify the scrambled or reversed string that is not immediately clear. Step 4: Reverse or decode the string to reveal the flag, formatted as FLAG_egg_cracked. TECHNICAL IMPLEMENTATION: Components: Source Code File such as dino_decoder.c or dino_decoder.py that defines a string variable holding "FLAG_egg_cracked". A function that scrambles, reverses, or encodes the string. Clear inline comments referencing dinosaur eggs and incubation. Step-by-Step:

Write the source code that assigns a known string to a variable.
Apply a reversal algorithm or a simple encoding method.
Compile the C source using gcc -o dino_decoder dino_decoder.c or run the Python script.
Provide detailed instructions in a README file on how to run the executable and extract the flag. JURASSIC THEME: Design Elements: Include laboratory-themed comments such as "egg incubation initiated" and dinosaur egg graphics in any GUI output.
Medium – "Triceratops Lock" CHALLENGE DESCRIPTION: Title: Triceratops Lock Narrative: A binary simulating a secure digital lock for a dinosaur enclosure. The program verifies a hard-coded password using a custom algorithm. The setting is a high-security dinosaur park with a reinforced digital lock. User Instructions: Step 1: Load the binary into a reverse-engineering tool such as Ghidra or IDA Pro. Step 2: Navigate through the disassembled code to locate the password-checking function. Step 3: Analyze the custom algorithm, such as a series of arithmetic or bitwise operations. Step 4: Determine the correct password that the program expects, output as FLAG_tri_secure. TECHNICAL IMPLEMENTATION: Components: Source Code File such as triceratops_lock.c containing a function that compares user input to a hard-coded password. Use obfuscation techniques like variable renaming and dinosaur-themed inline comments. Clear markers indicating the beginning and end of the password verification routine. Step-by-Step:

Write the password verification function with explicit comparison logic.
Slightly obfuscate the function by renaming variables (for example, use dinoPass instead of password).
Compile the code and provide a disassembly guide in the documentation.
Include detailed comments in the source code to indicate where testers should focus their reverse-engineering efforts. JURASSIC THEME: Design Elements: Use variable names and comments referencing dinosaur strength, such as "as sturdy as a triceratops," and design the output with dinosaur silhouettes.
Hard – "Velociraptor Vault" CHALLENGE DESCRIPTION: Title: Velociraptor Vault Narrative: This challenge presents a heavily obfuscated binary simulating a secure vault within a velociraptor habitat. The binary employs multiple anti-debugging measures and encrypts portions of the flag. The narrative suggests that only the swift and cunning, like a velociraptor, can bypass these defenses. User Instructions: Step 1: Load the binary into advanced analysis tools such as OllyDbg or Ghidra. Step 2: Bypass the anti-debugging routines by identifying explicit checks as described in the code comments. Step 3: Locate the encrypted segments in the code by carefully following the control flow. Step 4: Use standard deobfuscation techniques to decrypt these segments. Step 5: Concatenate the decrypted segments to form the final flag, formatted as FLAG_raptor_unleashed. TECHNICAL IMPLEMENTATION: Components: Source Code File such as velociraptor_vault.c containing functions for anti-debugging, encryption, and decryption. Explicit inline comments marking sections like "Begin anti-debugging" and "Encryption routine starts here." Compile the binary with obfuscation flags enabled. Step-by-Step:

Write functions that implement anti-debugging techniques (for example, checking for debugger signatures).
Create an encryption routine that splits the flag into multiple parts.
Embed detailed inline documentation explaining each section and what to analyze.
Compile the binary ensuring that obfuscation techniques are active.
Test using both static analysis and runtime debugging to confirm that each layer functions correctly. JURASSIC THEME: Design Elements: Include code comments with phrases like "swift raptor maneuvers" and refer to the secure vault as "the raptor’s lair" in the narrative.
Impossible – "Mosasaurus Matrix" CHALLENGE DESCRIPTION: Title: Mosasaurus Matrix Narrative: This is the ultimate reverse-engineering challenge, presenting a binary with multiple layers of virtualization and heavy obfuscation. It simulates a complex system reminiscent of the behavior of a Mesolithic predator. The flag is deeply hidden behind layers of encrypted, virtualized code that require sequential unraveling. User Instructions: Step 1: Load the binary into multiple advanced disassemblers and debuggers. Step 2: Identify all sections that are virtualized or heavily obfuscated. Step 3: Methodically analyze the control flow and document every discovered branch. Step 4: Extract and piece together intermediate data that, when combined, decode to form the final flag, formatted as FLAG_mosasaurus_master. Step 5: Follow the precise, step-by-step deobfuscation process as documented in the internal comments. TECHNICAL IMPLEMENTATION: Components: Source Code File such as mosasaurus_matrix.c incorporating multiple layers of virtualization, conditional anti-tampering checks, and encryption loops. Each layer must be clearly delineated in the source code with explicit comments such as "Layer 1: Virtualization start." Advanced obfuscation methods like control flow flattening and dummy code insertion must be used. Step-by-Step:

Write the source code with at least three layers of obfuscation.
Insert explicit inline documentation for each layer, including header comments that describe its purpose and the expected analysis method.
Compile with advanced obfuscation tools ensuring that each layer is bypassed sequentially.
Provide a detailed deobfuscation guide as part of the internal documentation.
Test extensively with multiple tools and document every expected output. JURASSIC THEME: Design Elements: Integrate narrative elements such as "the labyrinthine mind of a mosasaur" and use dinosaur-inspired variable names like "mosaLayer1" and "mosaKey" throughout the code. The final output should reflect a prehistoric fortress with an emphasis on the impenetrable nature of the ancient beast.
C. SQL INJECTION EXAMPLES

Easy – "Jurassic Login" CHALLENGE DESCRIPTION: Title: Jurassic Login Narrative: The user is presented with a login page for a dinosaur park management system. The login form is intentionally vulnerable to a simple SQL injection. The flag is stored in the backend database and is revealed upon successful injection. User Instructions: Step 1: Access the login page. Step 2: Notice that the login form accepts raw input for both username and password. Step 3: Input a known SQL injection payload such as 1' OR '1'='1 in either the username or password field. Step 4: Submit the form and verify that the login bypasses authentication. Step 5: Once logged in, navigate to the hidden page where the flag is displayed as FLAG_login_unlocked. TECHNICAL IMPLEMENTATION: Components: HTML File: login.html with form elements for username and password. Backend Script: Written in PHP, Python, or Node.js to process the login credentials. Database: A table, for example named users, that stores user data including an entry for the flag. Vulnerability: The script constructs an SQL query using unsanitized user input. Step-by-Step:

Create login.html with input fields such as and , plus a submit button.
Develop the backend script that constructs an SQL query like: "SELECT * FROM users WHERE username = '" + user_input + "' AND password = '" + pass_input + "'" without using parameterized queries.
Create the database table with at least one user entry where the flag is stored.
Insert Jurassic-themed comments in both the HTML and backend code.
Test by entering the SQL injection payload and verify that the flag is returned. JURASSIC THEME: Design Elements: The login page should display images of dinosaur park gates and fossil footprints, use a color scheme reminiscent of weathered stone and ancient parchment, and include text such as "Unlock the secrets of the ancient park."
Medium – "Fossilized Database" CHALLENGE DESCRIPTION: Title: Fossilized Database Narrative: This challenge simulates a fossil database containing records of dinosaur excavations. The SQL injection vulnerability allows the user to execute union-based queries. The flag is stored within one of the tables, for example in a table named excavation_logs, and must be extracted. User Instructions: Step 1: Identify the query input field that fetches fossil records. Step 2: Craft a union-based SQL injection payload that appends a query to enumerate table names and columns. Step 3: Identify the table and column where the flag is stored, such as excavation_logs. Step 4: Execute the payload to extract the flag formatted as FLAG_fossil_found. TECHNICAL IMPLEMENTATION: Components: Web Interface: A page that displays fossil data from a database. Backend: A script that builds SQL queries dynamically using unsanitized input. Database Schema: Multiple tables such as fossils, excavation_logs, and park_data with interrelated data. Step-by-Step:

Design the fossil database with at least three tables.
Create the web page that includes a search form for fossil records.
In the backend, construct a query such as "SELECT * FROM fossils WHERE name LIKE '%" + user_input + "%'" that allows modification via a UNION operator.
Ensure that one table, for example excavation_logs, includes a column where the flag is stored.
Insert detailed debugging instructions on how to use UNION queries. JURASSIC THEME: Design Elements: Use images of excavation sites, fossil sketches, and style the page with textures reminiscent of sedimentary rock. Include narrative phrases like "dig deep into the layers of time."
Hard – "Prehistoric Pulse" CHALLENGE DESCRIPTION: Title: Prehistoric Pulse Narrative: The challenge involves a login system for a prehistoric data center that employs time-based blind SQL injection. The system introduces deliberate time delays on incorrect inputs. The flag, formatted as FLAG_pulse_detected, is reconstructed one character at a time by analyzing these response delays. User Instructions: Step 1: Recognize that the login system uses time delays in its responses. Step 2: Craft SQL injection payloads that incorporate time delay functions such as sleep(). Step 3: Measure the delay differences to deduce each character of the flag. Step 4: Repeat the process iteratively until the complete flag is assembled. TECHNICAL IMPLEMENTATION: Components: Web Form: A login page with username and password fields. Backend: A script that processes SQL queries and introduces a time delay (for example, using sleep()) if conditions are not met. Database: A hidden table storing the flag with a documented delay mechanism. Step-by-Step:

Create the login endpoint with unsanitized SQL query construction.
Insert a condition such that if the SQL condition is false, the query executes a delay function like SLEEP(5).
Write detailed instructions on how to measure response times using tools such as curl or a web proxy.
Document the iterative process: "Inject payloads character by character and record the delay differences."
Test and verify that each character of the flag is retrievable through the time-based responses. JURASSIC THEME: Design Elements: Use design elements such as ancient clocks, crumbling digital archives, and incorporate dinosaur icons alongside timer animations. The narrative should include phrases like "the pulse of the prehistoric server."
Impossible – "Cretaceous Conundrum" CHALLENGE DESCRIPTION: Title: Cretaceous Conundrum Narrative: This is the most advanced SQL injection challenge. The system uses a multi-layered vulnerability including out-of-band injection and second-order SQL injection. The flag, formatted as FLAG_cretaceous_unlocked, is obfuscated through several stages and must be retrieved by exploiting multiple vectors. User Instructions: Step 1: Identify the initial injection point in a complex query. Step 2: Exploit the vulnerability to trigger an out-of-band data retrieval mechanism. Step 3: Use the retrieved data to execute a second-order injection. Step 4: Decode the obfuscated output by following the multi-stage extraction process. Step 5: Combine all retrieved fragments in the correct order to reveal the complete flag. TECHNICAL IMPLEMENTATION: Components: Database: A complex schema with interlinked tables requiring multiple injection vectors. Backend: Code written in a language that supports advanced SQL manipulations, for example using Node.js with MySQL. Detailed configuration of each injection stage, including an initial SQL injection module, out-of-band data channel configuration (for example, setting up a DNS server that listens for callbacks), and a second-order injection module that processes intermediate data. Code comments must include explicit instructions with line numbers where vulnerabilities exist. Step-by-Step:

Design a multi-table database schema with intentional flaws in query construction.
Write backend code exposing several endpoints with different injection vulnerabilities.
For the initial injection, document the exact SQL query construction and point out where user input is concatenated.
For the out-of-band channel, specify the necessary configuration, such as setting up a DNS server for callback requests.
For the second-order injection, provide a precise algorithm detailing how data from the first stage triggers the second vulnerability.
Insert detailed internal documentation with step numbers and expected outputs explaining how to piece together the flag fragments.
Test the entire chain in a controlled environment and document every expected intermediate output. JURASSIC THEME: Design Elements: The interface should mimic a state-of-the-art dinosaur research facility with interactive dinosaur skeletons and animated exhibits. Use high-detail graphics representing the evolution of security measures in a prehistoric context, and emphasize in the narrative the intricate nature of unlocking ancient, locked-away secrets.
ADDITIONAL GUIDANCE FOR OUTPUT FORMATTING:

Section Headers: Each main section (I, II, III) must be clearly labeled with bold headers. Use sub-headers (A, B, C) to organize content.
Lists and Bullet Points: Use numbered lists for step-by-step instructions and bullet points for checklists and component descriptions.
Code Snippets: When including code, provide complete code blocks with language tags (for example, using triple backticks with the language specified) and include inline comments to explain each line.
Explicit Descriptions: Do not omit any step. Every action must be explained in detail, for example: "Click the Submit button, wait 5 seconds for the server response, then observe the network log in the developer console." Provide expected outputs for each step and instructions on what to do if the output differs.
Consistency: Ensure that every mention of the challenge category and difficulty level is consistently reflected in both narrative and technical sections. Cross-reference instructions when necessary.
FINAL REMINDER: Every minute detail of the challenge narrative and technical implementation must be included. Do not assume any prior background or reasoning ability. Each instruction is fully spelled out so that another system or robot can execute the steps without any additional interpretation. This output serves as a definitive, unambiguous blueprint for building both the challenge instructions and the setup instructions.
""")

  response = model.invoke(prompt.invoke({
    "category": command.category.value, 
    "difficulty": command.difficulty.value,
    "additional_prompt": command.additional_prompt
  }))

  return response.content

async def create_challenge_output(outline: str) -> ChallengeOuptut:
  model = ChatOpenAI(model="o3-mini-2025-01-31", api_key=global_settings.OPENAI_API_KEY, max_completion_tokens=4096)
  structured_model = model.with_structured_output(ChallengeOuptut)

  response = structured_model.invoke(outline)

  return response